from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3
import datetime

conn = sqlite3.connect('undercover.db')
c = conn.cursor()

def insert_row(word1, word2):
    c.execute(f'SELECT * from MalayWordPairs WHERE (word1="{word1}" and word2="{word2}") or (word1="{word2}" and word2="{word1}")')
    exist = c.fetchone()

    if not exist:
        c.execute("INSERT INTO MalayWordPairs VALUES (?, ?, 0)", (word1, word2))
        conn.commit()
        print(f"{word1}, {word2}")
        return True
    else:
        print(f"Existed: {word1}, {word2}")
        return True # True for now to make endless while loop

def initial_pick_card(player_name:str):
    ok_button = driver.find_element_by_id('com.yanstarstudio.joss.undercover:id/instructionOk')
    ok_button.click()
    card = driver.find_element_by_id("com.yanstarstudio.joss.undercover:id/card_cover")
    card.click()
    name_field = driver.find_element_by_id("com.yanstarstudio.joss.undercover:id/namePickEditText")
    name_field.send_keys(player_name)
    get_secret_word_btn = driver.find_element_by_id("com.yanstarstudio.joss.undercover:id/namePickGetWord")
    get_secret_word_btn.click()
    secret_word_field = driver.find_element_by_id("com.yanstarstudio.joss.undercover:id/showWordWordDisplay")
    secret_word = secret_word_field.text
    showWordOK_btn = driver.find_element_by_id("com.yanstarstudio.joss.undercover:id/showWordOk")
    showWordOK_btn.click()
    return secret_word

def pick_card():
    ok_button = wait.until(EC.visibility_of_element_located((By.ID, 'com.yanstarstudio.joss.undercover:id/instructionOk')))
    ok_button.click()
    card = wait.until(EC.visibility_of_element_located((By.ID, 'com.yanstarstudio.joss.undercover:id/card_cover')))
    card.click()
    secret_word_field = wait.until(EC.visibility_of_element_located((By.ID, 'com.yanstarstudio.joss.undercover:id/showWordWordDisplay')))
    secret_word = secret_word_field.text
    showWordOK_btn = wait.until(EC.visibility_of_element_located((By.ID, 'com.yanstarstudio.joss.undercover:id/showWordOk')))
    showWordOK_btn.click()
    return secret_word

desired_capabilities = {
    "platformName": "Android",
    "deviceName": "Android Emulator",
    "appPackage": "com.yanstarstudio.joss.undercover",
    "appActivity": "com.yanstarstudio.joss.undercover.splash.SplashActivity",
    "appWaitActivity": "com.yanstarstudio.joss.undercover.home.HomeActivity",
    "noReset": True,
    'newCommandTimeout': 0
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_capabilities)
driver.implicitly_wait(10)
wait = WebDriverWait(driver,10)

# Before loop
# Click on the button with id
homedoor = driver.find_element_by_id("com.yanstarstudio.joss.undercover:id/homeDoorButton")
homedoor.click()
time.sleep(0.5)
exit_first_tutorial = wait.until(EC.visibility_of_element_located((By.ID, 'com.yanstarstudio.joss.undercover:id/generalPopupImage')))
exit_first_tutorial.click()
time.sleep(0.5)
homedoor.click()

# Offline mood, swipe to lowest player, start game
time.sleep(3) # Load unlock content
wait.until(EC.visibility_of_element_located((By.ID, 'com.yanstarstudio.joss.undercover:id/onlineOfflineModeBackground')))
driver.find_elements_by_id("com.yanstarstudio.joss.undercover:id/onlineOfflineModeBackground")[1].click()
time.sleep(1)
driver.swipe(start_x=283, start_y=618, end_x=210, end_y=618)
driver.find_element_by_id("com.yanstarstudio.joss.undercover:id/gameSetStartButton").click()
# Close tutorial
time.sleep(1)
driver.tap([(996, 84)])

# Pick card
secret_word1 = initial_pick_card("a")
secret_word2 = initial_pick_card("b")
secret_word3 = initial_pick_card("c")
wordlist = list({secret_word1, secret_word2, secret_word3})
insert_row(wordlist[0], wordlist[1])
# Close tutorial
time.sleep(1)
driver.tap([(996, 84)])
ok_button = driver.find_element_by_id('com.yanstarstudio.joss.undercover:id/instructionOk')
ok_button.click()

# Looping through all the words
# while True:
while True:
    repick_btn = wait.until(EC.visibility_of_element_located((By.ID, 'com.yanstarstudio.joss.undercover:id/cardsRePickButton')))
    repick_btn.click()
    # Confirm repick
    confirm_repick_btn = wait.until(EC.visibility_of_element_located((By.ID, 'android:id/button1')))
    confirm_repick_btn.click()
    card1 = pick_card()
    card2 = pick_card()
    if card1 != card2:
        ok_button = driver.find_element_by_id('com.yanstarstudio.joss.undercover:id/instructionOk')
        ok_button.click()
        if not insert_row(card1, card2):
            break
        continue

    card3 = pick_card()
    if not insert_row(card1, card3):
        break
    ok_button = driver.find_element_by_id('com.yanstarstudio.joss.undercover:id/instructionOk')
    ok_button.click()
    