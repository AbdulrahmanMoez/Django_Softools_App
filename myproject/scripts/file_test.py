import time
import asyncio
import fileinput




def check_ping():
    file_path = '/home/abdulrahman-moez/Documents/Abdo/other/test.txt'
    with  open(file_path) as file:
        data = file.read()

    lines = data.strip().split('\n')
    latest_ping = lines[-1].split(' ')[-2].split('=')[-1]
    ping = float(latest_ping)
    source = lines[0].split(' ')[1]
            
            
            
    def meter(ping):
        if ping < 20:
            return("Excellent")
        elif 20 <= ping < 50:
            return("Good")
        elif 50 <= ping < 100:
            return("Average")
        elif 100 <= ping < 300:
            return("High")
        else:
            return("Bad")
        
    post = str((f"\nSource: {source} | Ping is: {ping}ms  | Status: { meter(ping).center(5)}\n"))


    lines = open('/home/abdulrahman-moez/Documents/Abdo/other/test2.txt', 'a')
    lines.write(post)

print("\n<<<<<<< Ping Scanning Start >>>>>>>>>\n".center(50))
 
while True:
    try:
        
        check_ping()
        time.sleep(1)
    except ValueError:
        print("\n<<<<<<< Ping Scanning Stopped >>>>>>>>>\n".center(50))
        break
    except FileNotFoundError:
        print("File Not Found. Please Provide a Valid Directory")
        break
    except IndexError:
        print("File is Empty")
        time.sleep(1)
    # except RecursionError:
    #     print("This The End of File.")
    #     print("\n<<<<<<< Ping Scanning Stopped >>>>>>>>>\n".center(50))
    #     break
    
    
