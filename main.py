import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymsteams
import json

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=chrome_options)
 # Opening JSON file
f = open('bot_url.json',)
data = json.load(f)

repTechUrl = "https://rptechindia.in/nvidia-geforce-rtx-3060-ti.html"

driver.get(repTechUrl)

def isAvailableText(driver):
  e = driver.find_element_by_css_selector("span[class='rs2'] strike")
  return e.text

def checkWebsite():
  # You must create the connectorcard object with the Microsoft Webhook URL
  myTeamsMessage = pymsteams.connectorcard(data["nvidiaGpuStockConnector"])

  print('refreshing...')
  driver.refresh()
  try:
    availableText = isAvailableText(driver)
    if availableText == 'Out of stock':
      text_to_send = "Sorry, the product is out of stock"
      linkText = "Visit Site"
    else:
      text_to_send = availableText
      linkText = "Buy Now"
  except Exception as e:
    text_to_send = str(e)

  myTeamsMessage.text(text_to_send)
  myTeamsMessage.addLinkButton(linkText, repTechUrl)
  myTeamsMessage.send()
  print('sent a message: ' + text_to_send)

while True:
  checkWebsite()
  time.sleep(3600)
  print(f'waited for: 1 hour')