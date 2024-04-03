import requests
from fake_headers import Headers
import bs4
import pprint
import json

def resp_in_list(URL):
    headers = Headers(browser='firefox', os='win')
    headers_data = headers.generate()


    response = requests.get(URL, headers=headers_data)
    html_date = response.text
    soup = bs4.BeautifulSoup(html_date, 'lxml')
    profession_list = soup.find_all(class_ = 'vacancy-serp-item__layout')
    vacancy_list = []

    for item in profession_list:
        link_tag = item.find("a")["href"]
        salary = item.find("span", class_= "bloko-header-section-2")
        if salary is None:
            salary = ""
        else:
            salary = salary.text
        city = item.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).text
        company = item.find("a", class_ = "bloko-link bloko-link_kind-tertiary").text

        vacancy_list.append({
            "Ссылка": link_tag,
            "Зарплата": salary.replace("\u202f",''),
            "Компания": company.replace("\xa0", ' '),
            "Город": city.replace("\xa0", '')
        })
    return vacancy_list


def save_in_json(vac_list):
    with open("vacancy_list.json", "w", encoding="utf8") as file:
        json.dump(vac_list, file, ensure_ascii=False, indent=2)

def main():
    URL = "https://spb.hh.ru/search/vacancy?text=python,django,flask&area=1&area=2"
    cod_prog = resp_in_list(URL)
    save_in_json(cod_prog)

if __name__ == '__main__':
    main()