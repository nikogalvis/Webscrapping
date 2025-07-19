from logic.scraping_logic.wikipedia_logic import Wikipedia
from logic.scraping_logic.citizendium_logic import Citizendium
from logic.scraping_logic.mercado_libre_logic import MercadoLibre
from models.models_data import DataContainer

if __name__ == "__main__":
    licuadora = MercadoLibre("licuadora", "https://listado.mercadolibre.com.co/licuadoras#D[A:licuadoras]")
    licuadora.create_json()
    licuadora.insert_to_json("licuadora_data", "name_product", licuadora.extract_name_product())
    licuadora.insert_to_json("licuadora_data", "url_product", licuadora.extract_url_product())
    licuadora.insert_to_json("licuadora_data", "start_price_product", licuadora.extract_start_price_product())
    licuadora.insert_to_json("licuadora_data", "final_price_product", licuadora.extract_final_price_product())
    licuadora.insert_to_json("licuadora_data", "discount_info", licuadora.extract_discount_info())
    licuadora.insert_to_json("licuadora_data", "name_seller", licuadora.extract_name_seller())
    licuadora.insert_to_json("licuadora_data", "score", licuadora.extract_score())
    licuadora.insert_to_json("licuadora_data", "quantity_score", licuadora.extract_quantity_score())
