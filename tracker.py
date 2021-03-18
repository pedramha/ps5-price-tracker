import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from random import randint
import time
import smtplib

AMAZON_URL = "https://www.amazon.de/-/en/dp/B08H98GVK8/ref=sr_1_1?crid=VTPBM6IHH1CY&dchild=1&keywords=ps5+digital+edition&qid=1616099689&sprefix=ps5+digi%2Caps%2C207&sr=8-1"
WAIT_TIME = 5
PRICE = 500.00
GMAIL_USERNAME = "your_user_name"
GMAIL_PASSWORD = "xxx"
receiver_email_id="your email to receive the information"

class tracker:
    def __init__(self):
        self.driver=webdriver.Firefox()

    # def signIn(self):
    #     '''you need this funcion if you also want to buy the item programatically'''
    #     driver=self.driver
    #     username_elem=driver.find_elementby_xpath("//input[@name='email'")
    #     username_elem.clear()
    #     username_elem.send_keys(self.username)
    #     time.sleep(randint(int(WAIT_TIME/2),WAIT_TIME))
    #     username_elem.send_keys(Keys.RETURN)
    #     time.sleep(randint(int(WAIT_TIME/2),WAIT_TIME))

    def findProduct(self):
        driver=self.driver
        driver.get(AMAZON_URL)
        time.sleep(randint(int(WAIT_TIME/2),WAIT_TIME))

        isAvailable=self.isProductAvailable()
        if isAvailable == 'Currently unavailable.':
            print('not available')
        else:
            self.sendemail()
            print('available')

    def isProductAvailable(self):
        driver = self.driver
        time.sleep(2)
        cookies = driver.find_element_by_id('sp-cc-accept')
        cookies.click()
        time.sleep(2)
        # you need the part below if there are multiple items sold within the same url
        # element = driver.find_element_by_xpath("//span[text()='PS5 - Digital Edition']")
        # element.click()
        # time.sleep(2)

        available=driver.find_element_by_class_name('a-color-price').text
        if available == 'Currently unavailable.':
            return available
        else:
            print(f'price: {available}')
            return available
            
    def closeBrowser(self):
        self.driver.close()

    def sendemail(self):       
        FROM = GMAIL_USERNAME
        TO = receiver_email_id
        SUBJECT = "ps5 available"
        TEXT = "available"

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
            server.sendmail(FROM, TO, message)
            server.close()
            print('successfully sent the mail')
        except:
            print("failed to send mail")

if __name__ == '__main__':
    while True:
        shopBot = tracker()
        shopBot.findProduct()
        shopBot.closeBrowser()
        time.sleep(50)

