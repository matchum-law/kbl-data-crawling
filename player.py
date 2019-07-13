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

    divs = soup.findAll('div', {"class": "item"})

    return divs


driver = webdriver.Chrome('/Users/woojeong/Downloads/chromedriver')

driver.get('https://www.kbl.or.kr/stats/team_player_gamerecord.asp')

df = pd.DataFrame()
for i in range(2, 12):
    select_team = driver.find_element_by_xpath('//*[@id="print"]/div[1]/fieldset/form[2]/a[1]/span[2]')
    team_xpath = "/html/body/ul[2]/li["+str(i)+"]/a"
    team = driver.find_element_by_xpath(team_xpath)
    team_name = team.text

    actions = ActionChains(driver).move_to_element(select_team).click(select_team).click(team).perform()

    # 3개의 테이블이 다 들어있는 리스트
    tables = get_table(driver.current_url)

    result = []
    for table in tables:
        temp = []
        # player 리스트에 모든 기록을 담고 있는 태그들을 '선수별로' 담는다.
        player = table.find('tbody').find_all('tr')
        # 선수별로 조회한다.
        for data in player:
            person = []
            # d 리스트에 각각의 기록들을 담는다.
            d = data.find_all('td')
            for txt in d:
                # d 리스트에 있는 기록들은 <td>태그로 감싸져있으므로 text를 이용해 person 리스트에 담는다.
                person.append(txt.text)
            # temp 리스트에 선수별로 담는다.
            temp.append(person)
        # result 리스트에 테이블별로 담는다.
        result.append(temp)
    team_name = driver.find_element_by_xpath('//*[@id="print"]/div[1]/fieldset/form[2]/a[1]/span[1]').text
    first = pd.DataFrame(result[0])
    first.columns = ['배번', '선수', 'G', 'Min', '2P', '2PA', '%', '3P', '3PA', '%', 'FG%', 'FT', 'FTA', '%']
    efg = (first["2P"].astype(int) + first["3P"].astype(int) + 0.5*first["3P"].astype(int)) / (first["2PA"].astype(int) + first["3PA"].astype(int))
    first["eFG%"] = round(efg,3)
    first["팀"] = team_name
    second = pd.DataFrame(result[1])
    second.columns = ['배번', '선수', 'ORB', 'DRB', 'RPG', 'Ast', 'APG', 'w/FT', 'w/oFT']
    third = pd.DataFrame(result[2])
    third.columns = ['배번', '선수', 'STL', 'BS', 'GD', 'TO', 'DK', 'DKA', 'PTS', 'PPG']


    df1 = pd.merge(pd.merge(first, second), third)  # type: object # 조인
    df = pd.concat([df, df1],ignore_index=True)
    #year = driver.find_element_by_xpath('//*[@id="print"]/div[1]/fieldset/form[2]/a[2]/span[1]').text
    #team_name = driver.find_element_by_xpath('//*[@id="print"]/div[1]/fieldset/form[2]/a[1]/span[1]').text


# df.to_csv("모든선수.csv", encoding='cp949')
# df.to_csv("모든선수(utf-8).csv", encoding='utf-8-sig')