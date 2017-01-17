from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
import fileinput
import sys



def page_is_loaded(driver):
   return driver.find_element_by_tag_name("body") != None

chrome_path = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_path)

driver.get("http://www2.dre.ca.gov/PublicASP/pplinfo.asp")
wait = ui.WebDriverWait(driver, 30)
wait.until(page_is_loaded)

for line in sys.stdin:
   license = line.strip()
   license_field = driver.find_element_by_name("LICENSE_ID")
   license_field.send_keys(license)
   driver.find_element_by_xpath("""//*[@id="main_content"]/div/form/table/tbody/tr[6]/td[2]/input[1]""").click()

   html = driver.page_source
   soup = BeautifulSoup(html, "html.parser")

   table = soup.find('tbody')
   rows = table.findAll('tr', limit=3)

   for tr in rows: 
      cols = tr.find_all('td')[1:] #only counts second columns
      for td in cols:
         licType = ''.join(td.text).encode('utf-8')
         #lic_list[0].append(td.text)
     #    text = u''.join(td.text).encode('utf-8')

      print (licType)


   driver.back()
   driver.find_element_by_xpath("""//*[@id="main_content"]/div/form/table/tbody/tr[6]/td[2]/input[2]""").click()

#licenseInfo = pd.DataFrame( data )

