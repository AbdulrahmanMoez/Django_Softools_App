import requests
from bs4 import BeautifulSoup


page = requests.get('https://www.geeksforgeeks.org')
content = page.content
soup = BeautifulSoup(content, "lxml")

data = soup.find("div", {"class": "logo"})


pre = str(data)
final = pre.split('src="')[1].split('"')[0]
file = open(f"file{final}", "+ab")


# <img class="gfg_logo_img" style="height: 30px; width: 80px; max-width: fit-content;" src="https://media.geeksforgeeks.org/gfg-gg-logo.svg" alt="geeksforgeeks">