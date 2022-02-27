from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import time
import os
import subprocess


usernameStr = ''
passwordStr = ''

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.prompt_for_download": True,
  "profile.default_content_setting_values.automatic_downloads": 2
})

browser = webdriver.Chrome("chromedriver.exe",chrome_options=options)

browser.get(('http://ereader.wsj.net/?editionStart=The+Wall+Street+Journal'))

browser.implicitly_wait(5)

# fill in username and hit the next button
username = browser.find_element_by_id("username")
username.send_keys(usernameStr)


fbButton = browser.find_element_by_xpath('//*[@id="social-card"]/div[2]/a/span')
fbButton.click()

#Depending on internet speed, need to include pauses to allow explorer to catch up with the script
browser.implicitly_wait(10)
#Find and email textbox and send email
username_textbox2 = browser.find_element_by_id("email")
username_textbox2.send_keys(usernameStr)
#Find password textbox and send credentials
password_textbox = browser.find_element_by_id("pass")
password_textbox.send_keys(passwordStr)
#Find and click the login button
login_button = browser.find_element_by_id("loginbutton")
login_button.click()
#Wait and switch to the 'mainframe' of the pdf paper
browser.implicitly_wait(5)
browser.switch_to.frame("mainframe") #, where frameid is the id attribute present under the frame/iframe tag in HTML.
#Find and click the download button
download_button = browser.find_element_by_id("hotspot1opt")
browser.implicitly_wait(5)
download_button.click()
#Switch to download prompt
browser.implicitly_wait(10)
obj = browser.switch_to.alert.accept()
#Press enter to download default pdf name
time.sleep(5)
pyautogui.press('enter')
time.sleep(20)

#Move all journals to dir
#Rename to 'WSJ_TodaysDate' and move to Papers/ dir
os.system('REN "\\Downloads\\wallstreetjournal*" "WSJ_%Date:/= %.pdf"')
os.system('move \\Downloads\\WSJ_* \\Downloads\\Papers')
#Change dir 
os.chdir('\\Downloads\\Papers\\') 
#Execute rmapi and push /Papers dir
cmd = "rmapi.exe mput /Papers"
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
process.wait()