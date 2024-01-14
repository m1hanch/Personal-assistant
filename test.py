import requests
from bs4 import BeautifulSoup
import json
def get_news():
    url = "https://warsawexpo.eu/kalendarz-targowy/"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    trades = soup.find_all('div', class_='single-callendar-event')
    data = []
    for trade in trades:
        content_link = trade.find('a').get('href')
        response = requests.get(content_link)
        response.encoding = 'utf-8'
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('h1').text
        date = soup.find('div', class_='h5').text
        title = title.split(' - ')
        data.append({
            'title': title[0],
            'description': title[1],
            'date': date
        })
    df = pd.DataFrame(json_data)

    # Save the DataFrame to an Excel file
    excel_path = '/mnt/data/events.xlsx'
    df.to_excel(excel_path, index=False)
    # with open('trades.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

get_news()



