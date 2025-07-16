"""
This module container the object Mercado Libre derived from tha class DinamicWeb,
besides of contain everything functions an classes for the correct function of
the webscraping in Mercado Libre
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from models.models_website import DinamicWeb, WebPage

from models.models_data import Data, DataText, DataUrl

class MercadoLibre(DinamicWeb):
    """
    Class that allows you to manage a Mercado Libre web page with special methods
    """
    def __init__(self, name: str, url: str):
        """
        Starts the page with a name and URL
        """
        super().__init__(name, url)
        self.html = self.beautiful_soup()

    #Possible Market Extraction Data
    # name_data: [tag, class]
    """
    list_product: ["ol", "ui-search-layout ui-search-layout--stack"]
        name_product: ["h3", "poly-component_title-wrapper"]
            url_product: ["a", "poly-component__title"]
        container_price: ["s", "andes-money-amount andes-money-amount--previous andes-money-amount--cents-coma"]
            price_product: ["span", "andes-money-amount__fraction"] -- no discount --
        name_seller: ["span", "poly-component__seller"]
        container_price: ["div", "poly-price__current"]
            price_product: ["span" , "andes-money-amount__fraction"] -- discount -- 
        information_discount: ["span", "andes-money-amount__discount"]
        score: ["span", "poly-reviews__rating" --> "calificación"]
        quantity_score: ["span", "poly-reviews__total" --> "total de calificaciones"]
    """

    def extract_name_product(self, ol_products):
        """
        Extracts all product names from the page corresponding to a search in
        Mercado Libre and transforms them into Data objects
        """
        list_name_prod = []
        for product in ol_products:
            name = product.find("h3", class_ = "poly-component_title-wrapper")
            title = name.text.strip() if name else "No defined"
            name_product = DataText(
                f"{title}_name", {"tag" : "h3" , "class" : "poly-component_title-wrapper"})
            #The data is equally to the product names
            if title != "No defined":
                name_product.add_data_text(title) 
            else:
                name_product.add_data_text(None)
            list_name_prod.append(name_product)
        dict_name_products = {"name_product": list_name_prod}
        return dict_name_products

    def extract_url_product(self, ol_products):
        """
        Extracts all product urls from the page corresponding to a search in
        Mercado Libre and transforms them into Data objects
        """
        list_url_prod = []
        for product in ol_products:
            url = product.find("a", class_ = "poly-component__title")
            title = product.find("h3", class_ = "poly-component_title-wrapper")
            #The title equally to name_product
            title = title.text.strip() if title else "No defined"
            url_product = DataUrl(f"{title}_url", "poly-component__title")
            url_product.add_data_web(url)
            list_url_prod.append(url_product)
        dict_url_products = {"url_product": list_url_prod}
        return dict_url_products

    def extract_start_price_product(self, ol_products):
        """
        Extracts all product prices (no discount) from the page and transforms
        them into DataText objects
        """
        list_price_prod = []
        for product in ol_products:
            container_prod = product.find(
                "s", class_ = "andes-money-amount andes-money-amount--previous andes-money-amount--cents-coma")
            price_tag = container_prod.find("span", class_ = "andes-money-amount__fraction")
            #The title equally to name_product
            title = product.find("h3", class_ = "poly-component_title-wrapper")
            title = title.text.strip() if title else "No defined"
            price_obj = DataText(
                f"{title}_price", {"tag": "span", "class": "andes-money-amount__fraction"})
            price_obj.add_data_text(price_tag.text.strip() if price_tag else None)
            list_price_prod.append(price_obj)
        return {"price_product": list_price_prod}

    def extract_final_price_product(self, ol_products):
        """
        Extracts all product prices (with discount) from the page and transforms
        them into DataText objects
        """
        list_price_discount = []
        for product in ol_products:
            container_prod = product.find("div", class_ = "poly-price__current")
            price_tag = container_prod.find(
                "span", class_ = "andes-money-amount__fraction") if container_prod else None
            #The title equally to name_product
            title = product.find("h3", class_="poly-component_title-wrapper")
            title = title.text.strip() if title else "No defined"
            price_obj = DataText(
                f"{title}_price_discount", {"tag": "span", "class": "andes-money-amount__fraction"})
            price_obj.add_data_text(price_tag.text.strip() if price_tag else None)
            list_price_discount.append(price_obj)
        return {"price_discount": list_price_discount}

    def extract_discount_info(self, ol_products):
        """
        Extracts discount information if present
        """
        list_discount_info = []
        for product in ol_products:
            discount_tag = product.find("span", class_ = "andes-money-amount__discount")
            #The title equally to name_product
            title = product.find("h3", class_ = "poly-component_title-wrapper")
            title = title.text.strip() if title else "No defined"
            discount_obj = DataText(
                f"{title}_discount", {"tag": "span", "class": "andes-money-amount__discount"})
            discount_obj.add_data_text(discount_tag.text.strip() if discount_tag else None)
            list_discount_info.append(discount_obj)
        return {"information_discount": list_discount_info}

    def extract_name_seller(self, ol_products):
        """
        Extracts the seller's name
        """
        list_sellers = []
        for product in ol_products:
            seller_tag = product.find("span", class_ = "poly-component__seller")
            title = product.find("h3", class_ = "poly-component_title-wrapper")
            title = title.text.strip() if title else "No defined"
            #The title equally to name_product
            seller_obj = DataText(
                f"{title}_seller", {"tag": "span", "class": "poly-component__seller"})
            seller_obj.add_data_text(seller_tag.text.strip() if seller_tag else None)
            list_sellers.append(seller_obj)
        return {"name_seller": list_sellers}

    def extract_score(self, ol_products):
        """
        Extracts the score (rating) of the product
        """
        list_scores = []
        for product in ol_products:
            score_tag = product.find("span", class_ = "poly-reviews__rating")
            #The title equally to name_product
            title = product.find("h3", class_ = "poly-component_title-wrapper")
            title = title.text.strip() if title else "No defined"
            score_obj = DataText(
                f"{title}_score", {"tag": "span", "class": "poly-reviews__rating"})
            score_obj.add_data_text(score_tag.text.strip() if score_tag else None)
            list_scores.append(score_obj)
        return {"score": list_scores}

    def extract_quantity_score(self, ol_products):
        """
        Extracts the total number of reviews
        """
        list_q_scores = []
        for product in ol_products:
            q_score_tag = product.find("span", class_ = "poly-reviews__total")
            #The title equally to name_product
            title = product.find("h3", class_ = "poly-component_title-wrapper")
            title = title.text.strip() if title else "No defined"
            q_score_obj = DataText(
                f"{title}_quantity_score", {"tag": "span", "class": "poly-reviews__total"})
            q_score_obj.add_data_text(q_score_tag.text.strip() if q_score_tag else None)
            list_q_scores.append(q_score_obj)
        return {"quantity_score": list_q_scores}