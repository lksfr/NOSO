from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import csv


#GitHub Link
#https://github.com/lksfr/WebScraping/

#opening Chrome
driver = webdriver.Chrome()

#retrieving the website containing the reviews for the iPhone X
driver.get('https://www.kohls.com/catalog/fashion-jewelry.jsp?CN=Trend:Fashion+Department:Jewelry&cc=jewelry_accessories-TN2.0-S-fashionjewelry&kls_sbp=86507101832324889460463120834667304434')

time.sleep(4)

#setting an index to count page numbers
index = 0

#creating a csv file named reviews_uk to save all review data in
csv_file = open('kohls.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)



#starting a while-loop that ends once Selenium doesnt find a "Next Page" button on the last review page
while True:
	try:
		#printing the page index to verify that the loop is working properly 
		print('scraping page number ' + str(index))

		#increasing the page index by one during every loop iteration
		index += 1
		print('='*50)
		products = driver.find_elements_by_xpath('//li[@class="products_grid yourPrice_eligible"]')
		print(len(products))
		print('='*50)

		
		#starting a for-loop iterating over the length of the review boxes list
		#finding all reviews and saving them in variable "reviews"
		#opening a "review_dict" dictionary to store results in
		#subscripting the "reviews" list and retrieving the ith review box
		for product in products:

			wait = WebDriverWait(driver, 10)

		#	wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-element="product-results-product-module-desktop"]')))
		#	reviews = driver.find_elements_by_xpath('//div[@data-element="product-results-product-module-desktop"]')
			review_dict = {}
			
		#	review = reviews[i]
	


			#extracting the star rating of review i
			product_name = product.find_element_by_xpath('.//div[4]/div[3]/p[1]').get_attribute("textContent")
			print(product_name)

	# # 	#extracting the title of review i
			sale_price = product.find_element_by_xpath('.//p[@class="prod_price_amount red_color"]').get_attribute("textContent")
			print(sale_price)

	# # 	#extracting the date of review i
			regular_price = product.find_element_by_xpath('.//p[@class="prod_price_original"]').get_attribute("textContent")
			print(regular_price)

	# # 		#extracting the username of review i
	# # 		username = review.find_element_by_xpath('.//a[@data-hook="review-author"]').get_attribute("textContent")

	# # 		#extracting the text of review i
	# # 		text = review.find_element_by_xpath('.//span[@data-hook="review-body"]').get_attribute("textContent")

	# # 		#extracting whether or not review i is a verified purchase
	# # 		try:
	# # 			purchase_type = review.find_element_by_xpath('.//span[@data-hook="avp-badge"]').get_attribute("textContent")

	# # 		except Exception:
	# # 			purchase_type = 'Not Verified Purchase'

	# # 		#extracting the number of "helpful" votes, 0 if element does not exist
	# # 		try:

	# # 			helpful = review.find_element_by_xpath('.//span[@data-hook="helpful-vote-statement"]').get_attribute("textContent")
	# # 		except Exception:
	# # 			helpful = '0 people found this helpful'

			#saving all retrieved information in the review_dict dictionary
			review_dict['product_name'] = product_name
			review_dict['sale_price'] = sale_price
			review_dict['regular_price'] = regular_price
	# 		review_dict['review_text'] = text
	# 		review_dict['user_name'] = username
	# 		review_dict['purchase_type'] = purchase_type
	# 		review_dict['helpful'] = helpful

	# # 		#writing all entries of review i into the csv file
			writer.writerow(review_dict.values())
		#xidentifying and clicking the "Next Page" button once all reviews on one page have been extracted
		time.sleep(5)
		next_button = driver.find_element_by_xpath('//a[@class="ce-pgntn nextArw fr  changed"]')
		next_button.click()
		#actions = ActionChains(driver)
		#actions.move_to_element(next_button).click().perform()
		time.sleep(5)

		

	# # #printing the error in case scraping fails
	except Exception as e:
		print(e)
		break