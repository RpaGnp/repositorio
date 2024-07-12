import random
import time
from ast import If
import os
# import chromedriver_binary
# from selenium.common.exceptions import ElementNotVisibleException
# from selenium.common.exceptions import ElementNotSelectableException
from datetime import datetime, timedelta
from pathlib import Path
from platform import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# from ObtenerIP import get_my_ip
# import requests
# ip=get_my_ip()

BASEDIR = Path('.').absolute()

class bot():
    def __init__(self):
        self.bot_name = os.getenv('BOT_NAME', 'DefaultBot')
        print(self.bot_name)
        # Otros inicializadores

    def openChrome(self):

        if 'Windows' in platform():
            print('The operating system is Windows\nWe will look for "chromedriver.exe"')

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            self.browser = webdriver.Chrome(ChromeDriverManager().install())

        else:
            print('The operating system is Linux\nWe will look for "chromedriver"')
            path = BASEDIR / 'driver/chromedriver'
            print('aqui abrimos chrome')
            # options = webdriver.ChromeOptions()
            # options.add_argument("--incognito")
            self.browser = webdriver.Remote('http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
            )

        self.browser.get('http://www.google.com')

    def loops(self):
        self.openChrome()

        print("""
        listo, iniciamos..!!
        """)

        equipos = ['Colombia','Venezuela','Argentina','Brasil','Mexico','Peru']

        for i in equipos:
            try:
                print('inicio bot')
                search = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.NAME, "q"))
                )
                search.clear() 
                search.send_keys("pais "+i)
                search.send_keys(Keys.RETURN) # hit return after you enter search text
                time.sleep(2) # sleep for 3 seconds so you can see the results
                
                # Toma una captura de pantalla
                screenshot_path = "screenshot.png"
                self.browser.save_screenshot(screenshot_path)
                print(f"Captura de pantalla guardada en: {screenshot_path} del bot {self.bot_name}")


            except (ConnectionRefusedError,IndexError, ConnectionError, ConnectionResetError, ConnectionAbortedError, Exception):
              
                print('termino ciclo..!')
                try:
                    print('error')
                    self.browser.quit()
                    self.openChrome()
                    #self.browser.save_screenshot("error 1.png")
                except Exception:
                    pass              

    def init(self):
        try:
            self.loops()
        except (ConnectionRefusedError,IndexError, ConnectionError, ConnectionResetError, ConnectionAbortedError):
            print('salio..!')
            exit()

if __name__ == '__main__':
    """ entry point app """
    time.sleep(10)
    b=bot()
    b.init()


