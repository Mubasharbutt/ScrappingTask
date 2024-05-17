import asyncio
import websockets
import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url1 = 'https://www.trendyol.com/formeya/mikro-fitted-full-kenar-su-sivi-gecirmez-yatak-koruyucu-alez-carsaf-tek-cift-battal-13-farkli-ebat-p-43257286?boutiqueId=61&merchantId=323918'
url2 = "https://www.trendyol.com/formeya/pamukkale-gri-alez-mikro-fitted-su-sivi-gecirmez-yatak-koruyucu-alez-10-farkli-ebat-p-474689611"
url3 = "https://www.trendyol.com/formeya/pamukkale-pudra-alez-mikro-fitted-su-sivi-gecirmez-yatak-koruyucu-alez-10-farkli-ebat-p-474695616"
url4 = "https://www.trendyol.com/formeya/pamukkale-kahverengi-alez-mikro-fitted-su-sivi-gecirmez-yatak-koruyucu-alez-10-farkli-ebat-p-474686159"


async def scrape_data():
    url = 'https://www.trendyol.com/formeya/mikro-fitted-full-kenar-su-sivi-gecirmez-yatak-koruyucu-alez-carsaf-tek-cift-battal-13-farkli-ebat-p-43257286?boutiqueId=61&merchantId=323918'
    response1 = requests.get(url1)
    if response1.status_code == 200:
        soup = BeautifulSoup(response1.text, 'html.parser')    
        product_name = soup.find(class_='pr-new-br').text
        product_size = soup.find(class_='size-variant-attr-value').text
        all_sizes = soup.find_all(class_='sp-itm')
        all_sizes = [size.text for size in all_sizes]
        # color
        color = soup.find('span', {'title': 'Beyaz'}).text
        # category
        category = soup.find(class_='product-description-market-place').text
        # image 1
        div = soup.find('div', {'class': 'gallery-container'})
        inner_div = div.find('div', {'class': 'gallery-modal-content'})
        image = inner_div.find('img').attrs['src']
        # product image color
        color = soup.find('span',{'title': 'Beyaz'}).text
        # image 2
        response2 = requests.get(url2)
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        inner_div=soup2.find('div', {'class': 'gallery-container'})
        inner_div = inner_div.find('div', {'class': 'gallery-modal-content'})
        image2 = inner_div.find('img').attrs['src']
        # image2 color
        color2 = soup2.find('span',{'title': 'Gri'}).text
        # image3
        response3 = requests.get(url3)
        soup3 = BeautifulSoup(response3.text, 'html.parser')
        inner_div=soup3.find('div', {'class': 'gallery-container'})
        inner_div = inner_div.find('div', {'class': 'gallery-modal-content'})
        image3 = inner_div.find('img').attrs['src']
        # image3 color
        # color3 = soup3.find('span',{'title': 'Açık Pembe'}).text
        # image4
        response4 = requests.get(url4)
        soup4 = BeautifulSoup(response4.text, 'html.parser')
        inner_div4=soup4.find('div', {'class': 'gallery-container'})
        inner_div4= inner_div4.find('div', {'class': 'gallery-modal-content'})
        image4 = inner_div4.find('img').attrs['src']
        # image4 color
        color4 = soup4.find('span',{'title': "Kahverengi"}).text

        data = {
            "product_name": product_name,
            "product_size": product_size,
            "all_sizes": all_sizes,
            "color": color,
            "category": category,
            "image": image,
            "other_images": [image2,image3,image4],
            "other_colors": [color2,color4]
        }
        return data
    else:
        return {"error": "Failed to retrieve webpage."}

async def send_updates(websocket, path):
    while True:
        data = await scrape_data()
        await websocket.send(str(data))
        await asyncio.sleep(10)  # Scrape the data every 10 seconds

start_server = websockets.serve(send_updates, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
