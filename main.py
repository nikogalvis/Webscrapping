from logic.scraping_logic.wikipedia_logic import Wikipedia, create_url
from logic.scraping_logic.citizendium_logic import Citizendium
from logic.scraping_logic.mercado_libre_logic import MercadoLibre
from models.models_data import DataContainer
from config.settings import Config

if __name__ == "__main__":
    licuadora = MercadoLibre("licuadora", "https://listado.mercadolibre.com.co/licuadoras#D[A:licuadoras]")
    licuadora.extract_complete()
