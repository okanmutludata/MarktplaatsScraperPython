from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup
import telegram

bot = telegram.Bot(token='') #Je telegrambot. De token krijg je tijdens het genereren van de bot., ik heb de python-telegram-bot library gebruikt =  https://python-telegram-bot.org
chat_id = # de Chat ID die je krijgt tijdens het genereren van een de bot

option = Options()
option.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe" // selenium setup

#path = Service('C:\Program Files\Google\Chrome Beta\Application\chrome.exe') #The version needs to keep being updated
driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='107.0.5304.62').install()), options=option)

#URL you want to search articles for
url = 'https://www.marktplaats.nl/q/nintendo+ds/#offeredSince:Vandaag|sortBy:SORT_INDEX|sortOrder:DECREASING|searchInTitleAndDescription:true'

#driver.maximize_window()
driver.get(url)
driver.maximize_window()
time.sleep(4)

#accepteert cookies
cookies_button = driver.find_element(By.ID, 'gdpr-consent-banner-accept-button')
cookies_button.click()
time.sleep(2)

#zoekt artikelen en hun waardes op binnen een zoekopdracht
#artikelen = driver.find_elements_by_xpath("//*[@id='content']/div[2]/ul/li")
#time.sleep(3)


#loops langs de artikelen in de zoekopdracht en slaat het op in titel_en_prijs
def loop_artikelen ():
	artikelen = driver.find_elements(By.XPATH, "//*[@id='content']/div[2]/ul/li")
	artikelen_lijst = []
	for artikel in artikelen[0:15]:
		titel = artikel.find_element(By.CLASS_NAME, 'mp-Listing-title').text
		prijs = artikel.find_element(By.CLASS_NAME, 'mp-Listing-price').text
		link = artikel.find_element(By.CLASS_NAME, 'mp-Listing-coverLink').get_attribute('href')
		artikel = (titel, prijs, link)
		artikelen_lijst.append(artikel)

	return artikelen_lijst

while True:
	driver.refresh()
	time.sleep(3)

	#code that runs the whole day
	loop_artikelen()
	oudeloop = loop_artikelen()
	#for artikels in oudeloop:
		#print(artikels)

	time.sleep(240)
	driver.refresh()
	print("refreshed")
	time.sleep(3)

	loop_artikelen()
	nieuweloop = loop_artikelen()

	#the return value of this function has to be messaged via telegram or some sort
	def check_nieuwe_item():
		verschillende_artikelen = []
		if oudeloop == nieuweloop:
			print('zelfde')
		else:
			print(f"Nieuwe item\n")
			verschillende_artikelen = list(set(nieuweloop) - set(oudeloop)) #Checks the difference between the second list and first list.

		return verschillende_artikelen

	check_nieuwe_item()

	for nieuwe_artikel in check_nieuwe_item():
		print(nieuwe_artikel)
		bot.sendMessage(text=nieuwe_artikel, chat_id = chat_id)



