
import requests
from bs4 import BeautifulSoup
import csv


def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file, delimiter='/')
        writer.writerow([data['title'], data['descriptions'], data['price'], data['image']])


def get_html(url):
    #возвращает html код стр
    response = requests.get(url)
    return response.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    list_page = soup.find('ul', class_ = 'pagination').find_all('li')
    last_page = list_page[-1]
    total_pages = last_page.find('a').get('href').split('=')
    return int(total_pages[-1])
    




def get_data(html):
    soup = BeautifulSoup(html, 'lxml')                               
    product_list = soup.find_all('div', class_="list-item list-label")
    
    for product in product_list:
        try:
            title = product.find('div', class_ = 'block title').find('h2', class_="name").text.strip()#.find('strong').text
        
        except:
            title = ""
            
        try:
            price = product.find('p').find('strong').text
        
        except:
            price = ''
            
        try:
            descriptions = product.find('div', class_='block info-wrapper item-info-wrapper').find('p', class_="body-type").text.strip()
        except:
            descriptions = ''

        try:
            image = product.find('img').get("data-src")
        except:
            image = ''

        dict_ = {'title':title, 'descriptions': descriptions, 'price':price, 'image':image}
        # print(dict_)
        write_to_csv(dict_)


def main():
    notebooks_url = 'https://www.mashina.kg/search/all/'
    pages ='?page='
    html = get_html(notebooks_url)
    number = get_total_pages(html)
    get_data(html)
    
    for i in range(1, number + 1):
        url_pages = notebooks_url + pages + str(i)
        html = get_html(url_pages)
        get_data(html)

with open('data.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['title','descriptions', 'price', 'image'])

main()




   
    
    
        
