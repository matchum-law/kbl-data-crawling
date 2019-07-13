import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import time


def get_table(url):
    data = []

    req = requests.get(url)
    req.encoding = None
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.findAll('table')

    return tables


driver = webdriver.Chrome('/Users/woojeong/Downloads/chromedriver')

driver.get('https://www.kbl.or.kr/stats/team_statistics.asp')

# 3개의 테이블이 다 들어있는 리스트
team_tables = get_table(driver.current_url)

df = pd.DataFrame()
result = []
for table in team_tables:
    temp = []

    # 테이블을 하나의 원소로 삼는 리스트 1개를 생성. 담기는 것은 <td>태그로 감싼 팀 기록들
    team = table.find('tbody').find_all('tr')
    # print(team)
    # print("--------------------------")

    for data in team:
        team_data = []
        d = data.find_all('td')
        for txt in d:
            team_data.append(txt.text.strip())
        temp.append(team_data)

    result.append(temp)
    # result는 삼중 리스트이고 담겨 있는 데이터의 형식은 다음과 같다.
    # [테이블1,테이블2,테이블3]에서 테이블1 리스트는 ['팀1기록,'팀2기록,','팀3기록,...]으로 구성되어 있고, '팀1기록' 리스트는 ['팀1명','팀1스탯1',...]으로 이루어져있다.
    # [[['팀1명','팀1기록1',;팀1기록2',...],['팀2명','팀2기록1','팀2기록2',...],...],['팀1명','팀1기록x',팀1기록x+1',...],['팀2명','팀2기록x','팀2기록x+1',...],...],]

first = pd.DataFrame(result[0])
first.columns = ['팀명', '1Q', '2Q', '3Q', '4Q', 'EQ', 'Tot.Score', 'G', '2P', '2PA', '2P%', '3P', '3PA', '3P%']
second = pd.DataFrame(result[1])
second.columns = ['팀명', 'FG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'Tot.RB', 'AST', 'w/FT', 'w/oFT', 'Tot.PF', 'TF']
third = pd.DataFrame(result[2])
third.columns = ['팀명', 'STL', 'TO', '팀TO', 'GD', 'BS', '팀FB', 'DK', 'DKA', '교체']

df = pd.merge(pd.merge(first,second),third)
print(df)

df.to_csv('모든팀.csv',encoding='utf-8-sig')