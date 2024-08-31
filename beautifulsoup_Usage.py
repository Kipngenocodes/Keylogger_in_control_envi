from bs4 import BeautifulSoup
import requests

#  Send a GET request to the Webpage
url = "https://accounts.ecitizen.go.ke/en"
response = requests.get(url)

# Creation of a BeautifulSoup
response_soup = BeautifulSoup(response.text, 'html.parser')

# finding all <a> tags and extract their href attributes
tags = [a.get('href') for a in response_soup.find_all('a')]

print(tags)




