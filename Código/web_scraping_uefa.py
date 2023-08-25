
#driver de selenium
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

#para modificar las opciones de webdriver en Chrome
from selenium.webdriver.chrome.options import Options

#para instalar automáticamente chromedriver
import os
os.environ['WDM_LOCAL'] = '1'
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

#para condiciones en selenium
from selenium.webdriver.support import expected_conditions as ec

#excepción de timeout en selenium
from selenium.common.exceptions import TimeoutException

#para definir que tipo de búsqueda voy a definir para el elemento
from selenium.webdriver.common.by import By


import time

from selenium.webdriver.common.keys import Keys

import pandas as pd











def iniciar_chrome():
    """Inicia Chrome con los parámetros indicados y devuelve el driver"""

    ruta = ChromeDriverManager().install()

    #OPCIONES de CHROME:
    options = Options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}') #define un user-agent personalizado
    #options.add_argument('--window-size=1000,1000') #configuramos el ancho y largo de la ventana
    options.add_argument('--start-maximized')  #para que la ventana de Chrome aparezca maximizada
    options.add_argument('--headless')
    options.add_argument('--disable-web-security') #deshabilita la política del mismo origen o Same Origin Policy
    options.add_argument('--disable-extensions') #para que no cargue las extensiones de Chrome
    options.add_argument('--disable-notifications') #bloquea las notificiaciones de Chrome
    options.add_argument('--ignore-certificate-errors') #para ignorar el aviso "Su conexión es privada"
    options.add_argument('--no-sandbox') #deshabilita el modo sandbox
    options.add_argument('--log-level=3') #para que chromedriver no muestre nada en la terminal
    options.add_argument('--allow-running-insecure-content') #desactiva el aviso de "contenido no seguro"
    options.add_argument('--no-default-browser-check') #evita el aviso de que Chrome no es el navegador por defecto
    options.add_argument('--no-first-run') #evita la ejecución de ciertas tareas que se realizan la primera vez que se ejecuta Chrome
    options.add_argument('--no-proxy-server') #para no usar proxy, sino conexiones directas
    options.add_argument('--disable-blink-features-AutomationControlled') #evita que selenium sea

    #instanciamos el servicio de chromedriver
    s = Service(ruta)

    #instanciamos webdriver de selenium con Chrome
    driver = webdriver.Chrome(service=s, options=options) #añadimos el argumento options

    #devolvemos el driver
    return driver








# ENTRAMOS A LA WEB DE UEFA ########################################################################
def uefa(year):
    print(year)
    driver.get(f'https://es.uefa.com/uefachampionsleague/history/seasons/{year}/matches/')

    if year == 1955:
        try:
            elemento = wait.until(
                ec.element_to_be_clickable(
                    (By.ID, 'onetrust-accept-btn-handler')
                )
            )
        
        except TimeoutException:
            print('Error: Botón de COOKIES no encontrado')

        elemento.click()

    elemento = driver.find_element(By.CSS_SELECTOR, 'html')
    for n in range(50):
        time.sleep(0.2)
        elemento.send_keys(Keys.PAGE_DOWN)
        
    partidos = []
    try:
        partidos = wait.until(
            ec.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR,
                     "pk-match-unit[class='pk-match-unit hydrated']")
            )
        )
    except TimeoutError:
        print('Partidos no encontrados')
    
    
    matches = []

    for partido in partidos:
        partido = partido.text.split('\n')
        for expresion in partido:
            if ('Final' not in expresion) and ('Glo:' not in expresion)\
                and ('gana' not in expresion) and ('Ver ' not in expresion)\
                and ('Gana' not in expresion) and ('Group' not in expresion)\
                and ('Partido' not in expresion) and ('Ida:' not in expresion)\
                and ('Vuelta:' not in expresion) and (':' not in expresion)\
                and ('Grupo' not in expresion) and ('(' not in expresion):
                matches.append(expresion)

    print(matches)
    #print(len(matches))
    #print()
    #print()
    match = {}
    home = []
    away = []
    goalHome =[]
    goalAway = []
    
    for i in range(0, len(matches), 4):
        #match.append(matches[i:i+4])
        
        
        home.append(matches[i])
        away.append(matches[i+1])
        goalHome.append(matches[i+2])
        goalAway.append(matches[i+3])


    for partido in partidos:
        partido = partido.text.split('\n')
        for i in range(len(partido)):
            if '(' in partido[i] and '(' in partido[i+1]:
                home.append(partido[i-2])
                away.append(partido[i-1])
                goalHome.append(partido[i])
                goalAway.append(partido[i+1])
                i+=2

    match['Home'] = home
    match['GoalHome'] = goalHome
    match ['GoalAway'] = goalAway
    match['Away'] = away

    
    df = pd.DataFrame(match)
    if year < 2007:
        df['season'] = year+1
    elif year > 2007:
        df['season'] = year
    print(df)
    print()
    return df
    

    
    
    

        







# MAIN ##########################################################################################
if __name__=='__main__':
    driver = iniciar_chrome()

    wait = WebDriverWait(driver, 10)

    years = [i for i in range(1955,2024)]
    
    champions_league = [uefa(year) for year in years if year!=2007]

    df_champions = pd.concat(champions_league, ignore_index = True)

    df_champions.to_csv('/home/zaraki/Escritorio/Proyectos/Proyecto furbo/Data/partidos_champions_data.json')

    
    driver.quit()
