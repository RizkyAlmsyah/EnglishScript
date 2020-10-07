from selenium import webdriver
from getpass import getpass
import pprint
import time 
import json
from browsermobproxy import Server

usr = input("Enter you email student: ")
pwd = getpass("Enter your password: ")
many = int(input("Enter how many : "))

daily_dict = input("Daily dication(Yes/No): ")
daily_gramm = input("Daily grammar(Yes/No): ")


#use your browsermob path
server = Server("C:/browsermob-proxy-2.1.4-bin/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

co = webdriver.ChromeOptions()
co.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))

#use you driverchrome
driver = webdriver.Chrome("D:/Disk/chromedriver_win32/chromedriver.exe", options=co)
driver.maximize_window()

driver.get('https://login.pens.ac.id/cas/login?service=https://aliv.lecturer.pens.ac.id/courses/advanced-english/')

username_box = driver.find_element_by_id('username')
username_box.send_keys(usr)

password_box = driver.find_element_by_id('password')
password_box.send_keys(pwd)

login_btn = driver.find_elements_by_xpath("//input[@name='submit' and @value='LOGIN']")[0]
login_btn.click()
time.sleep(3)

proxy.new_har('req',options={'captureHeaders': True,'captureContent':True})
time.sleep(3)

def daily_dictation():
    for i in range(0, many):
        driver.get('https://aliv.lecturer.pens.ac.id/')
        time.sleep(10)
        driver.get('https://aliv.lecturer.pens.ac.id/quizzes/daily-dictation/')
        time.sleep(5)

        start_quiz_dictation = driver.find_elements_by_xpath("//input[@name='startQuiz' and @value='Start Quiz']")[0]
        start_quiz_dictation.click()
        time.sleep(5)
        
        for ent in proxy.har['log']['entries']:
            if(ent['serverIPAddress'] == "202.9.85.28"
                and ent['request']['url'] == "https://aliv.lecturer.pens.ac.id/wp-admin/admin-ajax.php"
                and ent['request']['method'] == "POST"
                and "globalPoints" in ent['response']['content']['text']):
                responseJson = ent['response']['content']['text']

        if responseJson =="":
            print("kosong")
        else:
            responseJson = json.loads(responseJson)
            for key in responseJson['json'].keys():
                for ans in responseJson['json'][key]['correct']:
                    answer = ans[0]

        answer_dictation = driver.find_element_by_xpath("//*[@id='wpProQuiz_27']/div[13]/ol/li/div[2]/ul/li/p/span/input")
        answer_dictation.send_keys(answer)
        time.sleep(5)

        check_btn = driver.find_elements_by_xpath("//input[@name='check' and @value='Check']")[0]
        check_btn.click()
        time.sleep(5)
        
        finish_btn = driver.find_element_by_name('next')
        finish_btn.click()
        time.sleep(5)

def daily_grammar():
    for i in range(0, many):
        driver.get('https://aliv.lecturer.pens.ac.id/')
        time.sleep(10)
        driver.get('https://aliv.lecturer.pens.ac.id/quizzes/daily-grammar-quiz/')
        time.sleep(5)
        
        start_quiz_grammar = driver.find_elements_by_xpath("//input[@name='startQuiz' and @value='Start Quiz']")[0]
        start_quiz_grammar.click()
        time.sleep(5)

        for ent in proxy.har['log']['entries']:
            if (ent['serverIPAddress'] == "202.9.85.28"
                and ent['request']['url'] == "https://aliv.lecturer.pens.ac.id/wp-admin/admin-ajax.php"
                and ent['request']['method'] == "POST"
                and "globalPoints" in ent['response']['content']['text']):
                responseJson = ent['response']['content']['text']

        idx = 0        
        if responseJson == "":
            print("Kosong")
        else:
            responseJson = json.loads(responseJson)
            for key in responseJson['json'].keys():
                for ans in responseJson['json'][key]['correct']:
                    if ans != 1:
                        idx += 1
                    else:
                        break

        liCorrect = driver.find_elements_by_class_name('wpProQuiz_questionListItem')[idx]        
        liCorrect.click()
        time.sleep(5)

        finish_btn = driver.find_element_by_name('next')
        finish_btn.click()
        time.sleep(5)

if( daily_dict.lower() == 'yes' or daily_dict.lower() == 'y'):
    daily_dictation()
                
if (daily_gramm.lower() == 'yes' or daily_gramm.lower() == 'y'):
    daily_grammar()
