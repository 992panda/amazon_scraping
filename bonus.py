import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from io import BytesIO
import random
import time
import gzip
# URL of the captcha page
captcha_page_url = 'https://www.amazon.com/errors/validateCaptcha'  
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Alt-Used': 'www.amazon.de',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'www.amazon.de',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'TE': 'trailers',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'
}
headers_two =  {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'images-na.ssl-images-amazon.com',
    'If-Modified-Since': 'Wed, 08 Feb 2012 10:23:23 GMT',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'TE': 'trailers',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'}

# Create a session to persist cookies
session = requests.Session()

# Send a GET request to the captcha page using the session
captcha_page_response = session.get(captcha_page_url, headers=headers)

if captcha_page_response.status_code == 200:
    # Parse the HTML content of the page using Beautiful Soup
    soup = BeautifulSoup(captcha_page_response.content, 'html.parser')
    
    # Extract the link from the parsed HTML (modify the selector based on the actual HTML structure)
    image_tag = soup.select_one('div.a-row.a-text-center img')
    if image_tag:
        captcha_image_url = image_tag['src']
        print('Captcha Image URL:', captcha_image_url)
    else:
        print('Image not found in the HTML content.')
    # Send a GET request to the captcha image URL using the session
    delay = random.uniform(1, 5)
    print(f"Waiting for {delay:.2f} seconds before the next request...")
    time.sleep(delay)
    captcha_response = session.get(captcha_image_url, headers=headers_two,allow_redirects=True)

    if captcha_response.status_code == 200:
    # Check if the response is gzipped and decompress if necessary
        if captcha_response.headers.get('content-encoding') == 'gzip':
            captcha_content = gzip.decompress(captcha_response.content)
        else:
            captcha_content = captcha_response.content
        
        # Process the image content
        image_bytes = BytesIO(captcha_content)
        captcha_image = Image.open(image_bytes)
        grayscale_image = captcha_image.convert('L')
        
        
        captcha_text = pytesseract.image_to_string(grayscale_image, config='--psm 11')

        
        # Save the image
        captcha_image.save('captcha_image.jpg')
        print(captcha_text)
        print('Image downloaded and saved successfully.')
    else:
        print('Failed to download captcha image. Status code:', captcha_response.status_code)


