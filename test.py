import requests

url = "https://google-news-api1.p.rapidapi.com/search"

querystring = {"language":"EN"}

headers = {
	"X-RapidAPI-Key": "c8b7db9176msha370ed7096a4a2ep1c8107jsn00bb19bbd515",
	"X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())