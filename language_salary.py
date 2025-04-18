import requests
import os
from dotenv import load_dotenv
import math
from terminaltables import AsciiTable


MOSCOW_ID_HH = 1
MOSCOW_ID_SJ = 4
PROGRAMMING_CATALOG_ID_SJ = 48


def predict_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        expected_salary = None
    elif not salary_from:
        expected_salary = salary_to * 0.8
    elif not salary_to:
        expected_salary = salary_from * 1.2
    else:
        expected_salary = (salary_from + salary_to) / 2
    return expected_salary


def predict_rub_salary_hh(vacancy):
    salary = vacancy['salary']
    if not salary:
        expected_salary = None
    elif salary['currency'] != 'RUR':
        expected_salary = None
    else:
        expected_salary = predict_salary(salary['from'], salary['to'])
    return expected_salary


def predict_rub_salary_sj(vacancy):
    payment_from = vacancy['payment_from']
    payment_to = vacancy['payment_to']
    if vacancy['currency'] != 'rub':
        expected_salary = None
    else: 
        expected_salary = predict_salary(payment_from, payment_to)
    return expected_salary


def create_statistics_table(salary_statistics, title):
    table_data = []
    table_data.append(['Язык программирования', 'Вакансий найдено ', 'Вакансий обработано ', 'Средняя зарплата'])
    for language, stats in salary_statistics.items():
        raw = [
            language,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary']
        ]
        table_data.append(raw)

    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table
    

def get_average_salary_hh(access_token, programming_languages):
    url = 'https://api.hh.ru/vacancies'
    headers = {
        "Authorization": f'Bearer {access_token}'
    }
    
    salary_statistics = {}
    
    for lang in programming_languages:
        page = 0
        pages_number = 1
        vacancies = []
        
        while page < pages_number:
            payload = {
                'text': f'программист {lang}', 
                'area': MOSCOW_ID_HH, 
                'page': page
            }
            
            page_response = requests.get(url, headers=headers, params=payload)
            page_response.raise_for_status()
            
            page_payload = page_response.json()  
                
            vacancies.extend(page_payload['items'])
            pages_number = page_payload['pages']
            page += 1
        
        processed_vacancies = 0
        salary_sum = 0
        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_hh(vacancy)
            
            if predicted_salary:
                salary_sum += predicted_salary
                processed_vacancies += 1
                    
        average_salary = int(salary_sum / processed_vacancies) if processed_vacancies else 0
        
        salary_statistics[lang] = {
            'vacancies_found': page_payload['found'],
            'vacancies_processed': processed_vacancies,
            'average_salary': average_salary
        }
        
    return salary_statistics
    
    
def get_average_salary_superjob(app_secret_key_sj, programming_languages):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': app_secret_key_sj
    }
    
    salary_statistics = {}
    
    for lang in programming_languages:
        page = 0
        pages_number = 1
        vacancies = []
        
        while page < pages_number:
            payload = {
                'page': page,
                'town': MOSCOW_ID_SJ,
                'catalogues': PROGRAMMING_CATALOG_ID_SJ,
                'keyword': lang
            }  

            page_response = requests.get(url, headers=headers, params=payload)
            page_response.raise_for_status()
                
            page_payload = page_response.json()  
                
            vacancies.extend(page_payload['objects'])
            
            if not page_payload['more']:
                break
            page += 1
        
        processed_vacancies = 0
        salary_sum = 0
        for vacancy in vacancies:
            predicted_salary = predict_rub_salary_sj(vacancy)
            
            if predicted_salary:
                salary_sum += predicted_salary
                processed_vacancies += 1
        
        average_salary = int(salary_sum / processed_vacancies) if processed_vacancies else 0
        
        salary_statistics[lang] = {
            'vacancies_found': page_payload['total'],
            'vacancies_processed': processed_vacancies,
            'average_salary': average_salary
        }
               
    return salary_statistics
    


def main():
    load_dotenv()
    access_token_hh = os.environ['ACESS_TOKEN_HH']
    app_secret_key_sj = os.environ['APP_SECRET_KEY_SUPERJOB']
    
    programming_languages = [
        'Javascript', 
        'Python', 
        'TypeScript', 
        'Java', 
        'C#', 
        'C++', 
        'PHP', 
        'C', 
        'Shell', 
        'Go'
    ]
    
    salary_statistics_hh = get_average_salary_hh(access_token_hh, programming_languages)
    print(create_statistics_table(salary_statistics_hh, 'HeadHunter Moscow'))
    print()
    
    salary_statistics_superjob = get_average_salary_superjob(app_secret_key_sj, programming_languages)
    print(create_statistics_table(salary_statistics_superjob, 'SuperJob Moscow'))
    

if __name__ == '__main__':
    main()