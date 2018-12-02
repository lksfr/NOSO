from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import csv
import os
import urllib.request as urllib
import imageio as im

os.mkdir('/Users/lukas/Downloads/necklaces2')
os.chdir('/Users/lukas/Downloads/necklaces2')

#opening Chrome
driver = webdriver.Chrome()

#retrieving the website 
driver.get('https://shop.nordstrom.com/c/necklaces?top=72&offset=0&page=25&sort=Boosted')

p=0

#starting a while-loop that ends once Selenium doesnt find a "Next Page" button on the last page
while True:
	try:

		images = driver.find_elements_by_xpath('//img[@name="product-module-image"]')
		
		p+=1
		i=0

		for img in images:

			i+=1

			url = img.get_attribute("src")
			urllib.urlretrieve(url, "{}{}.png".format(str(p),str(i)))

			print("="*50)
			print("Downloading Picture {}".format(str(i)))
			print("="*50)

		time.sleep(2)
		next_button = driver.find_element_by_xpath('//li[@data-element="page-arrow-page-next"]')
		next_button.click()
		time.sleep(4)




	except Exception as e:
		print(e)
		break