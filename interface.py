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

def handle_citizendium():
    name = input("Enter search term: ")
    url = input("Enter Citizendium URL: ")
    citi = Citizendium(name, url)
    citi.extraction_complete()

def handle_mercado_libre():
    name = input("Enter product: ")
    url = input("Enter Mercado Libre URL: ")
    mercado = MercadoLibre(name, url)
    mercado.extract_complete()
    doc = DocumentExcel(name)
    doc.load_data()
    doc.normalize_data()
    doc.create_document(name)

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
            config = Config()
            config.modify_config()
        elif option == 5:
            print("Exiting program...")
            sys.exit()