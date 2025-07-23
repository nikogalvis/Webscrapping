"""
Terminal interface for interacting with the main scraping and document modules
"""

import sys
from logic.scraping_logic.wikipedia_logic import Wikipedia, create_url
from logic.scraping_logic.citizendium_logic import Citizendium
from logic.scraping_logic.mercado_libre_logic import MercadoLibre
from models.models_website import StaticWeb, DinamicWeb
from logic.document_logic.DocumentExcel import DocumentExcel
from config.settings import Config
from logic.document_logic.DocumentWord import WordDocument

def main_menu():
    while True:
        try:
            print("+--------------------+")
            print("| Web Scraping Tool  |")
            print("+--------------------+")
            print("1. Scrape Wikipedia")
            print("2. Scrape Citizendium")
            print("3. Scrape Mercado Libre")
            print("4. Modify Program Settings")
            print("5. Exit")
            option = int(input("Enter an option: "))
            if option not in range(1, 6):
                raise IndexError
            return option
        except (ValueError, IndexError):
            print("Error. Please enter a number between 1 and 5.")

def wikipedia_menu():
    while True:
        try:
            print("+---------------------+")
            print("|      Wikipedia      |")
            print("+---------------------+")
            print("1. Generate URL")
            print("2. Enter URL")
            option = int(input("Enter an option: "))
            if option not in range(1, 3):
                raise IndexError
            return option
        except (ValueError, IndexError):
            print("Error. Please enter a number between 1 and 3.")

def handle_wikipedia():
    choice = wikipedia_menu()
    name = input("Enter search term: ")
    url = create_url(name) if choice == 1 else input("Enter Wikipedia URL: ")
    wiki = Wikipedia(name, url)
    wiki.extraction_complete()
    doc = WordDocument(wiki)
    doc.generate()

def handle_citizendium():
    name = input("Enter search term: ")
    url = input("Enter Citizendium URL: ")
    citi = Citizendium(name, url)
    citi.extraction_complete()
    doc = WordDocument(citi)
    doc.generate()

def handle_mercado_libre():
    name = input("Enter product: ")
    url = input("Enter Mercado Libre URL: ")
    mercado = MercadoLibre(name, url)
    mercado.extract_complete()
    doc = DocumentExcel(name)
    doc.load_data()
    doc.normalize_data()
    doc.create_document(name)

def handle_config():
    while True:
        try:
            print("+--------------------+")
            print("|      Options       |")
            print("+--------------------+")
            print("1. Wikipedia language.")
            print("2. Wikipedia quantity search.")
            print("3. Wikipedia with url associeted.")
            print("4. Wikipedia with url references.")
            print("5. Citizendium with url associeted.")
            print("6. Citizendium with url references.")
            print("7. Mercado libre time sleep.")
            print("8. Exit.")
            option = int(input("Enter an option: "))
            if option not in range(1, 9):
                raise IndexError
            return option
        except (ValueError, IndexError):
            print("Error. Please enter a number between 1 and 5.")

def config():
    config_ = Config()
    while True:
        op = handle_config()
        if op == 1:
            lang = input("Enter Wikipedia language (e.g., 'en', 'es'): ")
            config_.set_wp_lenguage(lang)
        elif op == 2:
            try:
                quantity = int(input("Enter number of results to retrieve: "))
                config_.set__wp_quantity_search(quantity)
            except ValueError:
                print("Invalid number.")
        elif op == 3:
            config_.set_wp_with_urls_asocciated("wikipedia")
        elif op == 4:
            config_.set_wp_with_urls_references("wikipedia")
        elif op == 5:
            config_.set_ct_with_urls_asocciated("citizendium")
        elif op == 6:
            config_.set_ct_with_urls_references("citizendium")
        elif op == 7:
            try:
                wait_time = float(input("Enter Mercado Libre wait time (in seconds): "))
                config_.set_ml_time_sleep(wait_time)
            except ValueError:
                print("Invalid time format.")
        elif op == 8:
            print("Exiting configuration...")
            return

def main():
    while True:
        option = main_menu()
        if option == 1:
            handle_wikipedia()
        elif option == 2:
            handle_citizendium()
        elif option == 3:
            handle_mercado_libre()
        elif option == 4:
            config()
        elif option == 5:
            print("Exiting program...")
            sys.exit()