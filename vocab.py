from selenium import webdriver
from getpass import getpass
import requests
import calendar
import time

usr = input("Enter you email student: ")
pwd = getpass("Enter your password: ")
many = int(input("Enter how many : "))

#use your browsermob path

co = webdriver.ChromeOptions()

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
time.sleep(5)

driver.get('https://aliv.lecturer.pens.ac.id/advanced-vocabulary/')
cookies = driver.get_cookies()
time.sleep(5)        

s = requests.Session()
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])


skrip = driver.find_elements_by_xpath("//script[contains(text(), 'H5PIntegration')]")
token = skrip[0].get_property('innerText')[216:226]

headers = {
    'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://aliv.lecturer.pens.ac.id',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://aliv.lecturer.pens.ac.id/advanced-vocabulary/',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8,jv;q=0.7'
}

params = (
            ('token', token),
            ('action', 'h5p_setFinished'),
        )

for i in range(0, many):
    ts = calendar.timegm(time.gmtime())
    finished = ts + 55
    data = {
        'contentId': '28',
        'score': '10',
        'maxScore': '10',
        'opened': str(ts),
        'finished': str(finished)
    }
    response = requests.post('https://aliv.lecturer.pens.ac.id/wp-admin/admin-ajax.php', headers=headers, params=params, cookies=s.cookies.get_dict(), data=data)
    print(response.content)
    print('---------------')
    time.sleep(60)
