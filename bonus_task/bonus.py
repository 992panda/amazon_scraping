import requests
from bs4 import BeautifulSoup
from PIL import Image
from amazoncaptcha import AmazonCaptcha
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



session = requests.Session()


captcha_page_response = session.get(captcha_page_url, headers=headers) #sending request to 1st page

if captcha_page_response.status_code == 200:
    
    soup = BeautifulSoup(captcha_page_response.content, 'html.parser')
    
    
    image_tag = soup.select_one('div.a-row.a-text-center img') #get image tag
    if image_tag:
        captcha_image_url = image_tag['src'] #captcha image link
        print('Captcha Image URL:', captcha_image_url) 
    else:
        print('Image not found in the HTML content.')
    # Send a GET request to the captcha image URL using the session
    
    #passing image link to amazon captcha solver
    captcha = AmazonCaptcha.fromlink(captcha_image_url) 
    solution = captcha.solve()
    print(solution)
    input_element = soup.select_one('input[name="amzn"]') # get value which and name from amamzon html page
    if input_element:
        value = input_element['value'] #value to be sentwith captcha solution
        print("Value of 'amzn' parameter:", value)
    else:
        print("Input element with name='amzn' not found.")
url = f"{captcha_page_url}?amzn={value}&amzn-r=/&field-keywords={solution}" #recreating the get request with session for cookies
response = session.get(url, headers=headers)
print(response.status_code)
print("bypassed amazon captcha")



  
        
        
        
    
    


