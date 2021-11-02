import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib
import os
import sys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "whatever.selenium")
options = Options()

options.add_argument("-profile")
options.add_argument(profile)
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
navegador = webdriver.Firefox(executable_path=os.path.join(dir_path, "geckodriver.exe"),capabilities=firefox_capabilities, firefox_options=options)
navegador.get("https://web.whatsapp.com/")
while len(navegador.find_elements_by_id("side")) < 1:
   time.sleep(1)
contatos_df = pd.read_json("contatos.json")
for i, item in enumerate(contatos_df["mensagem"]):
    numero = contatos_df.loc[i,"numero"]
    contato = contatos_df.loc[i,"contato"]
    mensagem = urllib.parse.quote(contatos_df.loc[i,"mensagem"])
    print(numero,contato)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"
    navegador.get(link)
    while len(navegador.find_elements_by_id("side")) < 1:
        time.sleep(1)
    WebDriverWait(navegador, 10).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'))).send_keys(Keys.ENTER)
    time.sleep(10)