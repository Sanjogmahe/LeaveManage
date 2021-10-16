from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from datetime import date
import time

today = date.today()

# dd/mm/YY
d1 = today.strftime("%m/%d/%Y")


options = Options()
options.binary_location = "C:/TEMP/Applications/ApplicationChrome/Application/chrome.exe"
driver = webdriver.Chrome(options=options, executable_path="C:/TEMP/Applications/chromedriver.exe")
driver.maximize_window()

def url(link):
    driver.get(
        link)

testStep=[]
transactionName=[]
testData=[]

def justCli(Xpath):
    driver.find_element(By.XPATH, Xpath).click()
    driver.implicitly_wait(50)

def cli(Xpath):
    text = driver.find_element(By.XPATH, Xpath).get_attribute('innerHTML')
    driver.find_element(By.XPATH, Xpath).click()
    testStep.append("Click on " + text + ' button')
    transactionName.append("_Claws_CloseSuffix_" + "Click on " + text)
    testData.append("")
    driver.implicitly_wait(50)

def justEnt(Xpath ,details):
    driver.find_element(By.XPATH, Xpath).send_keys(details)
    time.sleep(1)
    #driver.implicitly_wait(70)

def ent(Xpath ,details):
    text = driver.find_element(By.XPATH, Xpath).get_attribute('id')
    driver.find_element(By.XPATH, Xpath).send_keys(details)
    testStep.append("Enter " + details + " in " + text)
    transactionName.append("_Claws_CloseSuffix_" + "enter_" + details)
    testData.append(text+" : "+details)
    time.sleep(1)
    #driver.implicitly_wait(70)

def hover(xpath):
    check = driver.find_element(By.XPATH, xpath)
    hover = ActionChains(driver).move_to_element(check)
    hover.perform()

def clear(xpath):
    driver.find_element(By.XPATH, xpath).clear()

def wait(x):
    driver.implicitly_wait(x)

def iframe(frame):
    ifram = driver.find_element(By.XPATH, frame)
    driver.switch_to.frame(ifram)

def soupContent():
    content = driver.page_source
    soup = BeautifulSoup(content, features="lxml")
    return soup

def quit():
    driver.quit()