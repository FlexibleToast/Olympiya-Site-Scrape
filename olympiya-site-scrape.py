from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve as uRet
import os

# Get html from site
url = "http://olympiya.com/gallary"
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
	# Make gallery directory
	dest = gallery_url.split("/")[-2]
	if not os.path.exists(dest):
		os.makedirs(dest)
	# Get gallery page source
	uClient = uReq(gallery_url)
	gallery_html = uClient.read()
	uClient.close()
	# Parse gallery html
	gallery_soup = soup(gallery_html, "html.parser")
	# Get urls for images
	images = gallery_soup.findAll("div",{"class":"image_wrapper"})
	# Download each image
	for image in images:
		download = image.img["src"]
		filename = dest+"/"+download.split("/")[-1]
		# Check if already downloaded
		if os.path.exists(filename):
			print("File {} already exists".format(filename))
		else:
			print("Downloading: {}".format(filename))
			uRet(download, filename)
	print("Finished downloading {} images from {} gallery".format(len(images),dest))
# Finished
print("Finished scraping site")
