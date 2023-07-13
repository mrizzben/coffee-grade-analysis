import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# open chromedriver
driver = webdriver.Chrome(ChromeDriverManager().install())
time.sleep(2)

# navigate to arabica coffees page
driver.get('https://database.coffeeinstitute.org/coffees/arabica')
time.sleep(3)

# these values can be changed if this breaks midway through collecting data to pick up close to where you left off
page = 0
coffeenum = 0

while True:
	print('page {}'.format(page))

	# 50 rows in these tables * 7 columns per row = 350 cells. Every 7th cell clicks through to that coffee's data page
	for i in range(1, 400, 8):
		time.sleep(2)

		# paginate back to the desired page number
		# don't think there's a way around this - the back() option goes too far back
		# some page numbers aren't available in the ui, but 'next' always is unless you've reached the end
		for p_num in range(page):
			page_buttons = driver.find_elements('class file', 'paginate_button')
			page_buttons[-1].click() # the 'next' button
			time.sleep(1)
			page_buttons = driver.find_elements('class file', 'paginate_button')

		# select the cell to click through to the next coffee-data page
		time.sleep(2) # this next line errors out sometimes, maybe it needs more of a time buffer
		test_page = driver.find_elements('xpath', '//td')[i].click()
		time.sleep(2)
		print('rows: ')
		print(len(driver.find_elements('xpath', "//tr")))
		tables = driver.find_elements(By.ID, "DataTables_Table_0")

		# loop over all coffee reports on the page, processing each one and writing to csv
		print('tables: ')
		print(len(tables))
		j = 0
		for tab in tables:
			try:
				t = BeautifulSoup(tab.get_attribute('outerHTML'), "html.parser")
				df = pd.read_html(str(t))
				file = 'coffee_{}_table_{}.csv'.format(coffeenum, j)
				df[0].to_csv(file)
				print(file)
			except:
				# only one's needed but I want this to be obnoxious since it's the only way I'm logging this currently
				print('ERROR: {} failed'.format(file))
				print('ERROR: {} failed'.format(file))
				print('ERROR: {} failed'.format(file))
				print('ERROR: {} failed'.format(file))
			j += 1

		# go back to page with all other coffee results
		#driver.back() # note: this isn't working as expected, manually going back to pg 1 via url instead
		driver.get('https://database.coffeeinstitute.org/coffees/arabica')
		time.sleep(2)
		coffeenum += 1

	page += 1
	if page == 6:
		break


# close the driver
driver.close()
