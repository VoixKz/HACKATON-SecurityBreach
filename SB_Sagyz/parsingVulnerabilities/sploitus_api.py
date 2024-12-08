import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class SploitusAPI:
    def __init__(self, query, qtype='exploits', sort='default'):
        self.query = query
        self.type = qtype
        self.sort = sort
        self.offset = 0
        self.url = f'https://sploitus.com/?query={query}#exploits'

    def _init_header(self):
        headers = {
            'authority': 'sploitus.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        return headers

    def _make_get_request(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}")
        except Exception as e:
            print(f"Произошла неожиданная ошибка: {e}")
        return None

    def _get_data_total(self):
        headers = self._init_header()

        response = self._make_get_request(url=self.url, headers=headers)

        if response is not None and response.status_code == 200:
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Пример парсинга данных из HTML
                total_exploits = 10
                print("total = ", total_exploits)
                return int(total_exploits)
            except Exception as e:
                print(f"Ошибка парсинга HTML: {e}")

        return 0

    def _parse_exploits(self, html_content):
        edge = webdriver.ChromiumEdge()
        edge.get(self.url)
        time.sleep(5)
        sort_date_element = edge.find_element(By.CSS_SELECTOR, '[data-id="date"]')
        sort_date_element.click()
        time.sleep(5)
        soup = BeautifulSoup(edge.page_source, 'html.parser')
        exploits = []
        exploit_elements = soup.find_all('div', {'class': 'accordion'})

        for element in exploit_elements:
            exploit_id_element = element.find('button', {'class': 'btn', 'data-action': 'goto'})
            name_element = element.find('div', {'class': 'accordion-header'})
            date_element = element.find('div', {'class': 'tile-subtitle'})
            description_element = element.find('pre', {'class': 'centered code'})

            goto_id = element.find('button', {'class': 'btn', 'data-action': 'goto'})['data-id']
            link = f'https://sploitus.com/exploit?id={goto_id}'
            
            # with open('static/exploit_id.txt', mode='a+') as f:
            #     f.write(f"{goto_id}\n")

            # name_element = edge.find_element(By.CSS_SELECTOR, f"label.tile-centered[for='label-{goto_id}']")
            # print("At least I found name")
            # print(name_element.text)
            # repository_url_element = edge.find_element(By.CSS_SELECTOR, "button.btn[data-action='origin']")

            if exploit_id_element and name_element and date_element and description_element:
                
                # name_element.click()
                # time.sleep(5)
                # repository_url_element.click()
                # time.sleep(2) 
                # repository_url = edge.current_url
                # edge.back()  
                # time.sleep(2)
                
                name = name_element.text
                date = date_element.text
                exploit_id = exploit_id_element['data-id']
                description = description_element.text
                
                exploits.append({
                    'exploit_id': exploit_id,
                    'name': name,
                    'date': date,
                    'description': description,
                    'repository_url': link,
                })
            else:
                print("Не удалось найти один из элементов: exploit_id, name, date, description или repository_url")

        edge.quit()
        return exploits