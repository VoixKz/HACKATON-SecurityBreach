import math
from .sploitus_api import SploitusAPI

class SploitusSearch(SploitusAPI):
    def __init__(self, query, qtype='exploits', sort='default'):
        super().__init__(query, qtype, sort)

    def exec_query(self):
        headers = self._init_header()

        exploits_total = self._get_data_total()

        if exploits_total > 0:
            total_pages = math.ceil(exploits_total / 10)
            all_results = []

            for page in range(total_pages):
                response = self._make_get_request(url=self.url, headers=headers)

                if response.status_code == 200:
                    try:
                        exploits_on_page = self._parse_exploits(response.content)
                        all_results.extend(exploits_on_page)
                    except Exception as e:
                        print(f"Ошибка парсинга HTML: {e}")
                else:
                    print(f"Запрос завершился с кодом состояния {response.status_code}")

            return all_results[:10]
        else:
            print("Эксплойты не найдены.")
            return []