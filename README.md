# amazon_scraping
its a amazon scraper where it take asin numbers from csv and scrape details and store teh output in json , you can just conncet to your mysql database and it can dump the data there
here is the google collab link to run the code https://colab.research.google.com/drive/1G2Ps-RuLV3oChm0n6vrRUNsZi-zQmhHz?usp=sharing


# Bonus task 
my aprroach was to mimic the get request it was sneding to server  i used pillow library with amazon captcha solver to solve the captcha and mimim the url it was sending . it was tricky as  the get url was sending token when was unique and changed as one made a request to amazon captcaha first page  
