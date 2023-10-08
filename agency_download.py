import requests

agencies_url = 'https://www.netfile.com/Connect2/api/public/campaign/agencies.json'

# Request the agency list from NetFile
def download_agencies():
    global agencies_url
    response = requests.get(agencies_url)

    print(f'AGENCY: Request url: {response.url}')
    return response.json()
