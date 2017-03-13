from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
import sys
import sqlite3



def page_is_loaded(driver):
   return driver.find_element_by_tag_name("body") != None

# opens chrome
chrome_path = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_path)

i = 0

# goes to the website
driver.get("http://www2.dre.ca.gov/PublicASP/pplinfo.asp")
i = i + 1

# waits for the webpage to load
wait = ui.WebDriverWait(driver, 30)
wait.until(page_is_loaded)

if i == 1:
   # cycles through the input file, and searches the website for that license
   for line in sys.stdin:

      recordInfo = ''

      # takes line from input file
      license = line.strip()

      # inserts license into text field and hits submit
      license_field = driver.find_element_by_name("LICENSE_ID")
      license_field.send_keys(license)
      driver.find_element_by_xpath("""//*[@id="main_content"]/div/form/table/tbody/tr[6]/td[2]/input[1]""").click()

      # saves resulting page source to a BeautifulSoup object for parsing
      html = driver.page_source
      soup = BeautifulSoup(html, "html.parser")

      table = soup.find('tbody')
      rows = table.findAll('tr', limit=7)

      for tr in rows: 
         cols = tr.find_all('td')[1:] #skips the first column since those are field
                                   #names
         for td in cols:
            licType = ''.join(td.text).encode('utf-8')
            #lic_list[0].append(td.text)
      #    text = u''.join(td.text).encode('utf-8')

            recordInfo = recordInfo + '"' + licType + '",'

      print (recordInfo)


      # goes back and clears text field for next input
      driver.back()
      driver.find_element_by_xpath("""//*[@id="main_content"]/div/form/table/tbody/tr[6]/td[2]/input[2]""").click()

   #licenseInfo = pd.DataFrame( data )

