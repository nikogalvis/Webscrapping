from logic.document_logic.DocumentExcel import DocumentExcel
from logic.scraping_logic.wikipedia_logic import Wikipedia, create_url
from logic.scraping_logic.citizendium_logic import Citizendium
from logic.scraping_logic.mercado_libre_logic import MercadoLibre
from models.models_data import DataContainer
from config.settings import Config

if __name__ == "__main__":
    licuadora = MercadoLibre("Teto", "https://listado.mercadolibre.com.co/kasane-teto?sb=all_mercadolibre#D[A:Kasane%20Teto]")
    licuadora.extract_complete()

    doc = DocumentExcel("Teto_data")
    doc.load_data()
    doc.normalize_data()
    doc.create_document(title = f"Teto")