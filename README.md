# Programming vacancies compare

Calculate average salaries for some of the most popular programming languages in 2025 based on HeadHunter and SuperJob vacancies.

## Installation

Create a `.env` file in the project directory and add your HH access token and SuperJob app secert key:
```
ACESS_TOKEN_HH=your_hh_access_token
APP_SECRET_KEY_SUPERJOB=your_sj_app_secret_key
```

- To use HH API, you need to [submit a request to create an API application](https://dev.hh.ru/admin) and [receive a token](https://api.hh.ru/openapi/redoc#tag/Avtorizaciya-prilozheniya).
- To use SuperJob API, you need to [register the API application and get its secret key](https://api.superjob.ru/).

Python3 should already be installed. 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

## Example usage

Run the script from the command line. You'll see two tables for HH and SuperJob with average salaries for each programming language.
```
python language_salary.py
```

## Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).
 
