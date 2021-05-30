import tkinter
import tkinter.ttk
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random

global cbVariables
global cp
global possible_type
global place_name
global place_type

cbVariables = {}
cb = {}

possible_type = []
place_name = []
place_type = []

def read_new_data():
    JMT_list = open("./list.txt",'w')
    cnt = 1

    button_yes.destroy()
    button_no.destroy()

    button_buffer = tkinter.Button(window, text="YES", overrelief="solid", width=15, command=select_type, repeatdelay=1000, repeatinterval=100)
    
    while True:
        try:
            label.config(text="{}번째 페이지 검색 중...".format(cnt))
            window.update()
            url = "https://www.mangoplate.com/search/%EC%8B%A0%EC%B4%8C?keyword=%EC%8B%A0%EC%B4%8C&page=" + str(cnt)
            driver.get(url)

            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            
            store = soup.find_all('h2', {'class': 'title'})
            data = soup.find_all('div', {'class': 'info'})

            _name = []
            _type = []

            print("ok")

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
            label.config(text="검색 완료!")
            window.update()
            button_buffer.invoke()
            break

def select_type():
    JMT_list = open("./list.txt", 'r')

    button_yes.destroy()
    button_no.destroy()

    button_next.pack()

    label.config(text="음식 종류를 고르세요")

    while True:
        line = JMT_list.readline()
        
        if not line: 
            break
        
        place_name.append(line.split("-")[0])
        place_type.append(line.split("-")[1].replace("\n", ""))

    JMT_list.close()

    for item in place_type:
        if item not in possible_type:
            possible_type.append(item)

    for indx, _type in enumerate(possible_type):
        cbVariables[indx] = tkinter.IntVar()
        cb[indx] = tkinter.Checkbutton(window, variable=cbVariables[indx], text=_type, activebackground="blue")
        cb[indx].pack()
        window.update()
    

def get_check_list(cbVariables, possible_type, place_name, place_type):
    for widget in window.winfo_children():
        widget.destroy()

    target_type = []

    for i in range(len(cbVariables)):
        if cbVariables[i].get() == 1:
            target_type.append(possible_type[i])

    result_name = []
    result_type = []

    for i in range(len(place_type)):
        for target in target_type:
            if target in place_type[i]:
                result_name.append(place_name[i])
                result_type.append(place_type[i])

    if len(result_name) == 0:
        label = tkinter.Label(window)
        label.config(text="검색 결과가 없습니다")
        label.pack()
        window.update()

        assert False

    result = list(zip(result_name, result_type))
    random.shuffle(result)

    result_name, result_type = zip(*result)

    label = tkinter.Label(window)
    label.config(text="검색 추천 :")
    label.pack()
    window.update()

    for i in range(len(result_name)):
        text = result_name[i] + " --- " + result_type[i]
        label = tkinter.Label(window)
        label.config(text=text)
        label.pack()
        window.update()

        if i >= 4:
            break

window = tkinter.Tk()
window.title("JMT-Crawler V2.0")
window.geometry("640x400+100+100")
window.resizable(False, True)

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome('./chromedriver', options=options)
driver.implicitly_wait(0.5)

label = tkinter.Label(window, text="저장된 파일을 불러올까요?")
label.pack()

button_next = tkinter.Button(window, text="NEXT", overrelief="solid", width=15, command=lambda: get_check_list(cbVariables, possible_type, place_name, place_type), repeatdelay=1000, repeatinterval=100)

button_yes = tkinter.Button(window, text="YES", overrelief="solid", width=15, command=select_type, repeatdelay=1000, repeatinterval=100)
button_yes.pack()
button_no = tkinter.Button(window, text="NO", overrelief="solid", width=15, command=read_new_data, repeatdelay=1000, repeatinterval=100)
button_no.pack()

window.mainloop()