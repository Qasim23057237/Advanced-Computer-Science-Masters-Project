import requests
from bs4 import BeautifulSoup

url = "https://www.google.com/"
response = requests.get(url)

data = BeautifulSoup(response.text , "html.parser")

links = data.find_all("a")
images = data.find_all("img")

print(f"Total links on webpage : {len(links)}")

print(f"Total Images on page : {len(images)}")
missing_alt = []
for img in images:
    alt = img.get("alt")
    if not alt or alt.strip() == "":
        missing_alt.append(img)
print(f"Images missing alt : {len(missing_alt)} ")
