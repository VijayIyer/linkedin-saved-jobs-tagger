import requests
from bs4 import BeautifulSoup

email = "vijayiyer7@gmail.com"   ## take from .env
password = "EasyToRemember@1"   ## take from .env

client = requests.Session()

HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'

html = client.get(HOMEPAGE_URL).content
soup = BeautifulSoup(html, "html.parser")
csrf = soup.find('input', {'name': 'loginCsrfParam'}).get('value')

login_information = {
    'session_key': email,
    'session_password': password,
    'loginCsrfParam': csrf,
    'trk': 'guest_homepage-basic_sign-in-submit'
}

client.post(LOGIN_URL, data=login_information)

response = client.get('https://linkedin.com/my-items/saved-jobs')
print(response.content)
