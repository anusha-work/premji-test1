import json

import requests

def get_web_scraping_links(ticker):
    # Web Scrapping  endpoint
    web_url= f"https://backend.finshots.in/backend/search/?q={ticker}"
    # Send GET request
    links_response = requests.get(web_url)
    return links_response

def create_images(web_link):
    # Web Scrapping  endpoint
    image_url= f"https://api.rasterwise.com/v1/get-screenshot?url={web_link}&apikey=Nnrr9aScjU1PPlz3zuZyy9AbKNBtYWur6ubb6DAA&fullpage=true"
    # Send GET request
    img_response = requests.get(image_url)
    print(img_response)
    return img_response

def image_to_text(image_path):
    ocr_url = 'https://api.optiic.dev/process'
    data = {"apiKey": "FGbHvviKoJsKVcsvJ1NoddHGogVPoRwYhy7MEssZLTj4",
            "url": image_path}
    # Send POST request
    text_response = requests.post(ocr_url, json=data)
    return text_response.text



def get_sentimental_score(text_data):

    # Define the API endpoint and the data to send
    sentimental_url = 'http://api.text2data.com/v3/Extract'
    data = {
        'DocumentText': text_data,
        'PrivateKey': 'DC25B913-D461-4CC1-9C7C-09C11B3638CD',
        'Secret': 'test',
        'UserCategoryModelName': '',
        'RequestIdentifier': 'test'
    }

    # Define headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Send the POST request
    response = requests.post(sentimental_url, headers=headers, json=data)

    print(response.text)
    # Print the response (for debugging purposes)
    print('Status Code:', response.status_code)
    print('Response JSON:', response.json())

def main():

    ticker = "HDFC"
    links = get_web_scraping_links(ticker)
    links = links.json()
    for match in links['matches']:
        image = create_images(match['post_url'])
        image_response = image.json()
        screenshot = image_response['screenshotImage']
        ocr_text = image_to_text(screenshot)
        print(ocr_text)
        sentimental_response = get_sentimental_score(ocr_text)
        print(sentimental_response)
        exit()

if __name__ == "__main__":
    main()
