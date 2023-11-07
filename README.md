Amazon Scraper:

The Amazon Scraper is a Python script designed to extract product details from Amazon using ASIN numbers provided in a CSV file. It utilizes Beautiful Soup for parsing HTML content and Unidecode to decode Unicode characters. The scraped data is stored in JSON format. Additionally, the script offers the option to connect to a MySQL database to dump the scraped data.
Usage:

    CSV Input:
        Provide a CSV file containing ASIN numbers as input.

    Scraping Process:
        The script sends requests to Amazon's product pages using the provided ASIN numbers.
        Beautiful Soup parses the HTML content to extract product details.

    Data Storage:
        The scraped product details are stored in a JSON file.

    Database Integration (Optional):
        Connect the script to a MySQL database to directly store scraped data.



Bonus Task: Captcha Solver:

The Bonus Task involves solving Amazon's CAPTCHA challenge. The approach includes mimicking the GET request sent to the server. The solution utilizes the Pillow library for image processing and an Amazon CAPTCHA solver to decode the CAPTCHA image.
Process:

    CAPTCHA Challenge:
        Amazon's CAPTCHA challenge appears during certain interactions on the website.

    Image Processing:
        The CAPTCHA image is processed using the Pillow library to enhance its readability.

    CAPTCHA Solving:
        An Amazon CAPTCHA solver is employed to extract the text from the processed image.

    Mimicking the Request:
        The CAPTCHA text is used to mimic the URL that the original request was sending to the server.

    Challenges Faced:
        The challenge included dealing with changing tokens in the GET request, making the solution tricky to implement.


    Libraries Used:
        Beautiful Soup for HTML parsing.
        Unidecode for decoding Unicode characters.
        Pillow for image processing.
    Important Consideration:
        Ensure compliance with Amazon's terms of service while using this scraper and CAPTCHA solver.
