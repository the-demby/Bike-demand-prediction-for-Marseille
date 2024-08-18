import os
import time
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import glob
import logging

# Fonction pour attendre que le fichier CSV soit téléchargé
def wait_for_file_download(directory, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if any(file.endswith('.csv') for file in os.listdir(directory)):
            return True
        time.sleep(1)
    return False

download_dir = r"C:\Users\39812\OneDrive - Aix Marseille Provence Métropole\Documents\Bike Project\Datasets_preparation"
Dataset = r"C:\Users\39812\OneDrive - Aix Marseille Provence Métropole\Documents\Bike Project\Datasets"

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration du navigateur
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximiser la fenêtre
prefs = {"download.default_directory": download_dir}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

# Lien de la page et identifiants
Trips_page = "https://analytics.omega.fifteen.eu/mobility/trips/"

# Liste pour stocker les DataFrames de chaque fichier CSV
dfs = []

try:
    # Accéder à la page suivante
    driver.get(Trips_page)
    logging.info("Page de voyages vélos ouverte.")
    
    # Attendre un certain élément pour s'assurer que la page est chargée    
    # Par exemple, attendre le titre de la page
    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.v-field__input[data-no-activator=""]')))
    logging.info("Page chargée avec succès.")    

    # Après avoir accédé à next_page_url
    # Itération sur les dates de début jusqu'au jour avant aujourd'hui
    start_date = datetime(2024, 7, 28)
    end_date = datetime.now() - timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        # Cliquer sur le premier bouton pour afficher l'icône du calendrier
        calendar_icon1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/main/div/section/div/div[1]/div[1]/div[1]/div/div/div/div[4]')))
        calendar_icon1.click() 

        # Attendre que l'icône du calendrier soit visible et cliquer dessus
        calendar_icon2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ZaDateRangePicker__date__selector svg.v-icon[aria-hidden="true"].iconify.iconify--solar')))
        calendar_icon2.click()
        logging.info("Icône du calendrier cliquée pour afficher les dates du calendrier.")
    
        # Vérifier si le mois et l'année correspondent à la date actuelle
        formatted_date = current_date.strftime("%B %Y")
        month_year_element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".v-date-picker-controls__month-btn")))
        if month_year_element.text != formatted_date:
            # Cliquer sur le bouton pour changer de mois jusqu'à ce que le mois corresponde
            while month_year_element.text != formatted_date:
                if current_date == start_date:
                    prev_button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".mdi-chevron-left")))
                    prev_button.click()
                else:
                    time.sleep(2)
                    next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="v-menu-296"]/div/div/div/div[2]/div[1]/div[2]/button[2]')))
                    next_button.click()
                    # Attendre que la page se mette à jour après avoir cliqué sur le bouton "Suivant"
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".v-date-picker-month__days")))                                                    
        
        # Déterminer le format de date à utiliser
        if current_date.month >= 10:  # Mois d'Octobre, Novembre, Décembre
            if current_date.day < 10:  # Jours de 1 à 9
                format_day = current_date.strftime("%Y-%m-%d")
            else:  # Jours de 10 à 31
                format_day = current_date.strftime("%Y-%m-%d")
        else:  # Mois de Janvier à Septembre
            if current_date.day < 10:  # Jours de 1 à 9
                format_day = current_date.strftime("%Y-%m-%d")
            else:  # Jours de 10 à 31
                format_day = current_date.strftime("%Y-%m-%d")
        logging.info(f"format day: {format_day}")    
        time.sleep(4)
        
        # Sélectionner la date dans le calendrier
        day_elements = driver.find_elements(By.CSS_SELECTOR, ".v-date-picker-month__day, .v-date-picker-month__day--adjacent, .v-date-picker-month__day--week-start, .v-date-picker-month__day--week-end")   
    
    
        for day_element in day_elements:
            if day_element.get_attribute("data-v-date") == format_day:
                logging.info(f"Le day_element sélectionné pour le clic : {day_element.get_attribute('data-v-date')}")
                day_element.click()
                day_element.click()
                date_found = True
                break
        
        time.sleep(10)
        # Attendre que le bouton de téléchargement soit cliquable et cliquer dessus
        download_button1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/main/div/section/div/div[2]/div/div[3]/div/div[1]/div/div[2]/button/span[3]')))
        download_button1.click()

        # Attendre que le deuxième bouton de téléchargement soit visible et cliquer dessus
        download_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.v-list-item__content i.mdi-file-delimited.mdi.v-icon.notranslate.v-theme--light.v-icon--size-default.text-tertiary[loading="false"]')))
        download_button2.click()

        # Attendre que le fichier soit téléchargé
        if wait_for_file_download(download_dir):
            logging.info(f"Le fichier CSV pour la date {current_date.strftime('%Y-%m-%d')} a été téléchargé.")
        else:
            logging.warning(f"Le fichier CSV pour la date {current_date.strftime('%Y-%m-%d')} n'a pas été téléchargé.")
        
        # Passer à la prochaine date
        current_date += timedelta(days=1) 
        
finally:
    logging.info("Télécahrgement terminé")
    driver.quit()