from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
import base64
from io import BytesIO
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import re

data_encode = {
    # Basic text and URL
    'text': lambda data: data,
    'url': lambda data: re.compile(r'^https?://', re.IGNORECASE).sub('', data),
    
    # Email related
    'email': lambda data: 'mailto:' + re.compile(r'^mailto:', re.IGNORECASE).sub('', data),
    'emailmessage': lambda data: f'MATMSG:TO:{data[0]};SUB:{data[1]};BODY:{data[2]};;',
    
    # Phone and messaging
    'telephone': lambda data: 'tel:' + re.compile(r'^tel:', re.IGNORECASE).sub('', data),
    'sms': lambda data: f'SMSTO:{data[0]}:{data[1]}',
    'mms': lambda data: f'MMSTO:{data[0]}:{data[1]}',
    
    # Location
    'geo': lambda data: f'geo:{data[0]},{data[1]}',
    'googlemap': lambda data: f'https://maps.google.com/local?q={data[0]},{data[1]}',
    
    # Bookmarks and contacts
    'bookmark': lambda data: f'MEBKM:TITLE:{data[0]};URL:{data[1]};;',
    'phonebook': lambda data: f"MECARD:{';'.join([':'.join(i) for i in data])};",
    'vcard': lambda data: f"BEGIN:VCARD\nVERSION:3.0\n{''.join([f'{k}:{v}\n' for k,v in data])}\nEND:VCARD",
    
    # Wi-Fi configuration
    'wifi': lambda data: f"WIFI:T:{data.get('type', 'WPA')};S:{data['ssid']};P:{data.get('password', '')};;",
    
    # Calendar events
    'calendar': lambda data: (
        f"BEGIN:VEVENT\n"
        f"SUMMARY:{data['summary']}\n"
        f"DTSTART:{data['start']}\n"
        f"DTEND:{data['end']}\n"
        f"LOCATION:{data.get('location', '')}\n"
        f"DESCRIPTION:{data.get('description', '')}\n"
        f"END:VEVENT"
    ),
    
    # Cryptocurrency payments
    'bitcoin': lambda data: f"bitcoin:{data['address']}?amount={data.get('amount', '')}&label={data.get('label', '')}",
    'ethereum': lambda data: f"ethereum:{data['address']}?value={data.get('value', '')}",
    
    # Social media profiles
    'twitter': lambda data: f"https://twitter.com/{data}",
    'linkedin': lambda data: f"https://linkedin.com/in/{data}",
    'github': lambda data: f"https://github.com/{data}",
    
    # App store links
    'playstore': lambda data: f"market://details?id={data}",
    'appstore': lambda data: f"https://apps.apple.com/app/id{data}"
}

# Usage examples in comments:
"""
Examples of using different data types:

1. WiFi Configuration:
   wifi_data = {
       'type': 'WPA',
       'ssid': 'MyNetwork',
       'password': 'MyPassword'
   }

2. Calendar Event:
   calendar_data = {
       'summary': 'Team Meeting',
       'start': '20240224T140000Z',
       'end': '20240224T150000Z',
       'location': 'Conference Room',
       'description': 'Weekly team sync'
   }

3. VCard Contact:
   vcard_data = [
       ('FN', 'John Doe'),
       ('TEL', '+1234567890'),
       ('EMAIL', 'john@example.com'),
       ('ORG', 'Company Name'),
       ('TITLE', 'Software Engineer')
   ]

4. Cryptocurrency Payment:
   crypto_data = {
       'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
       'amount': '0.001',
       'label': 'Payment for services'
   }
"""

def generate_qr_code(data, fill_color="black", back_color="white"):
    
    qr = QRCode(version=3, error_correction=ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"



def scan_from_camera():
    cap = cv2.VideoCapture(0)
    data_stored = None
    
    while data_stored is None:
        _, frame = cap.read()
        decoded_objects = decode(frame)
        
        # Draw rectangle around QR code
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
            else:
                cv2.polylines(frame, [np.array(points, dtype=np.int32)], True, (0, 255, 0), 2)
            
            # If QR code is detected, store and display the data
            if obj.data:
                data_stored = obj.data.decode('utf-8')
                # Display data on the frame
                cv2.putText(frame, data_stored, (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('QR Code Scanner', frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return data_stored 


def scan_from_file(file_obj=None):
    try:
        if file_obj:
            image = Image.open(file_obj)
        else:
            return "No file provided"
            
        decoded_objects = decode(image)
        
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        return "No QR code found in image"
        
    except Exception as e:
        return f"Error scanning QR code: {str(e)}"
    
