import os
import json

from logic.document_logic.DocumentExcel import DocumentExcel
from logic.scraping_logic.wikipedia_logic import Wikipedia, create_url
from logic.scraping_logic.citizendium_logic import Citizendium
from logic.scraping_logic.mercado_libre_logic import MercadoLibre
from models.models_data import DataContainer
from config.settings import Config
from interface import main

if __name__ == "__main__":
    #Call to the general configuration container dictionary
    if not os.path.exists("config/config_program.json"):
        config = Config()
        config.save_config_json()
    with open("config/config_program.json", "r", encoding="utf-8") as file:
        config_ = json.load(file)
    main()