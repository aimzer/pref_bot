#!/usr/bin/python
import os
# import schedule
import time
# import unittest
# import smtplib
# import nexmo

#### pip install beautifulsoup4
from bs4 import BeautifulSoup

#### pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

import random

import easygui
import os


minutes = 2

# sms_msg = "YOUR MESSAGE TO BE SENT IN SMS"

search_text1 = "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous."
error_text1 = "No server is available to handle this request"
error_text2 = "The server returned an invalid or incomplete response."

# naturalisation
scrapped_url = "https://www.haute-garonne.gouv.fr/booking/create/7736"

# titre de sejour (test)
# scrapped_url = "https://www.haute-garonne.gouv.fr/booking/create/29739/0"


guichet_ids = [4,2,3]
guichet_names = ["planning36770", "planning14510","planning14520"]

duration = 1  # seconds
freq = 440  # Hz

# driver = webdriver.Chrome()

# options = Options()
# ua = UserAgent()
# user_agent = ua.random
# print(user_agent)
# options.add_argument(f'user-agent=' + user_agent)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
https://github.com/mozilla/geckodriver/releases
# driver = webdriver.Chrome(chrome_options=options)




# profile = webdriver.FirefoxProfile('/home/aimen/.mozilla/firefox/qag02dhs.default-release')
profile = webdriver.FirefoxProfile('./firefox_profile')
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = webdriver.common.desired_capabilities.DesiredCapabilities.FIREFOX

firefox_driver = "./geckodriver"

driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired, executable_path=firefox_driver)

driver.set_page_load_timeout(10)


def send_availability():

    
    driver.get( scrapped_url )    
    
    #### page 1    
    
    html_source = BeautifulSoup(driver.page_source, 'html.parser')
    
    # if search_text1 in html_source.get_text() or error_text1 in html_source.get_text() or error_text2 in html_source.get_text():
    if search_text1 in html_source.get_text() or len(html_source.get_text()) < 200:
        return 0

    elmt = driver.find_element_by_id( "condition" )
    get_button = driver.find_element_by_name( "nextButton" )
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", elmt)
    driver.execute_script("arguments[0].click();", get_button)
    
    #### page 2
    
    time.sleep(3)

    html_source = BeautifulSoup(driver.page_source, 'html.parser')
    
    # if search_text1 in html_source.get_text() or error_text1 in html_source.get_text() or error_text2 in html_source.get_text():
    if search_text1 in html_source.get_text() or len(html_source.get_text()) < 200:
        return 0

    guichets = [
        driver.find_element_by_id( guichet_names[0] ),
        driver.find_element_by_id( guichet_names[1] ),
        driver.find_element_by_id( guichet_names[2] ),
    ]
    time.sleep(1)
    id_guich = random.randint(0,2)
    # guichets = driver.find_elements_by_name('planning')
    # print(len(guichets))
    # id_guich = random.randint(0,len(guichets)-1)
    driver.execute_script("arguments[0].click();", guichets[id_guich])
    
    time.sleep(0.2)
    get_button = driver.find_element_by_name( "nextButton" )
    driver.execute_script("arguments[0].click();", get_button)
    
    #### page 3
    
    time.sleep(3)
    
    html_source = BeautifulSoup(driver.page_source, 'html.parser')
    
    # if search_text1 in html_source.get_text() or error_text1 in html_source.get_text() or error_text2 in html_source.get_text():
    
    if len(html_source.get_text()) < 200:
        return 0

#     if search_text1 in html_source.get_text():
#         return 1
    
    # notification
    print('available')
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    
    get_button = driver.find_element_by_name( "nextButton" )
    driver.execute_script("arguments[0].click();", get_button)
    
    easygui.msgbox('rendez-vous disponible', 'RDV DISPO')

    return 2

iters = 0
while True:
    try:
        a = send_availability()
    except TimeoutException:
        print('timeout')
        a = 0
    iters += 1
    if a == 0:
        msg = 'error'
    elif a == 1:
        msg = 'no rdv'
    elif a == 2:
        msg = 'free'

    print('iteration', iters, msg)
    # time.sleep(minutes*60)

    for i in range(minutes*60):
        time.sleep(1)
        print('waiting %03d\r'%(minutes*60-i), end="")

    

driver.quit()

# send_availability()

