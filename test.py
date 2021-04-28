from selenium import webdriver
from bs4 import BeautifulSoup
import re
from art import *
import random

Art=text2art("JMT Crawler V1.0")
print(Art)

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome('./chromedriver', options=options)
driver.implicitly_wait(0.5)

cnt = 1

mode = input("저장된 파일을 불러올까요? [Y/n] : ")

if mode == "n" or mode == "N":
    print("맛집을 새로 검색합니다...")
    
    JMT_list = open("./list.txt",'w')

    while True:
        try:
            url = "https://www.mangoplate.com/search/%EC%8B%A0%EC%B4%8C?keyword=%EC%8B%A0%EC%B4%8C&page=" + str(cnt)
            driver.get(url)

            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            
            store = soup.find_all('h2', {'class': 'title'})
            data = soup.find_all('div', {'class': 'info'})

            _name = []
            _type = []

            for x in data:
                children = x.find_all('span')
                
                for i in range(len(children)):
                    test = str(children[i])
                    
                    if ("title ng-bindin" in test):
                        matches = re.findall(r'<span class="title ng-binding">.+?<!-- ngIf: restaurant.restaurant.branch_name -->', test)
                        matches = matches[0]
                        matches = matches.replace('<span class="title ng-binding">', "").replace('<!-- ngIf: restaurant.restaurant.branch_name -->', "")

                        _name.append(matches)

                    if ("<span>" in test):
                        matches = re.findall(r'<span>.+?</span>', test)
                        matches = matches[0]
                        matches = matches.replace('<span>', "").replace('</span>', "")
                        
                        _type.append(matches)
            
            if (len(_type) != len(_name)) or (len(_name) == 0):
                driver.quit()
                JMT_list.close()
                break

            for i in range(len(_type)):
                data = _name[i] + "-" + _type[i] + "\n"
                JMT_list.write(data)

            cnt += 1
        
        except:
            driver.quit()
            JMT_list.close()
            break


food_type = input("음식 종류 혹은 이름을 입력하세요(,로 구분) ")
food_type = food_type.replace(" ", "").split(",")

JMT_list = open("./list.txt", 'r')

place_name = []
place_type = []

while True:
    line = JMT_list.readline()
    
    if not line: 
        break
    
    place_name.append(line.split("-")[0])
    place_type.append(line.split("-")[1].replace("\n", ""))

JMT_list.close()

result_name = []
result_type = []

for i in range(len(place_type)):
    for target in food_type:
        if target in place_type[i]:
            result_name.append(place_name[i])
            result_type.append(place_type[i])

if len(result_name) == 0:
    print("검색 결과가 없습니다")

    assert False

result = list(zip(result_name, result_type))
random.shuffle(result)

result_name, result_type = zip(*result)

print("")
print("검색 추천 : ")

for i in range(len(result_name)):
    print(result_name[i], "---", result_type[i])

    if i >= 4:
        break