from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve as uRet
import os

# Variables
SITE = "http://olympiya.com/gallary"

# Get html from site
url = SITE
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

# Parse html
page_soup = soup(page_html, "html.parser")
# Get gallery pages
galleries = page_soup.findAll("div",{"class":"vc-hoverbox-back-inner"})
# Loop through each gallery
for gallery in galleries:
	gallery_url = gallery.p.a["href"]
	# Make directory
	dest = gallery_url.split("/")[-2]
	if not os.path.exists(dest):
		os.makedirs(dest)
	# Get new page source
	uClient = uReq(gallery_url)
	gallery_html = uClient.read()
	uClient.close()
	# Parse gallery
	gallery_soup = soup(gallery_html, "html.parser")
	# Get each picture
	images = gallery_soup.findAll("div",{"class":"image_wrapper"})
	# Download each image
	for image in images:
		download = image.img["src"]
		filename = dest+"/"+download.split("/")[-1]
		if not os.path.exists(filename):
			print("Downloading: %a" % filename)
			uRet(download, filename)
		else:
			print("File %a already exists" % filename)
# Finished
print("Finished scraping")
