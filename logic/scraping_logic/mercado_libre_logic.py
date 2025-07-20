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
        self.ol_products = self.html.find("ol", class_ = "ui-search-layout ui-search-layout--stack")

    #Possible Market Extraction Data
    # name_data: [tag, class]
    """
    list_product: ["ol", "ui-search-layout ui-search-layout--stack"]
        name_product: ["h3", "poly-component__title-wrapper"]
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

    def extract_name_product(self):
            """
            Extracts all product names from the page corresponding to a search in
            Mercado Libre and transforms them into Data objects
            """
            list_name_prod = []
            index = 1
            products = self.ol_products.find_all("li", class_ = "ui-search-layout__item")
            for product in products:
                name = product.find("h3", class_ = "poly-component__title-wrapper")
                title = name.text.strip() if name else "No defined"
                name_product = DataText(
                    index, {"tag" : "h3" , "class" : "poly-component__title-wrapper"})
                #The data is equally to the product names
                if title != "No defined":
                    name_product.add_data_text(title) 
                else:
                    name_product.add_data_text("<<NO INFORMATION>>")
                list_name_prod.append(name_product)
                index += 1
            return list_name_prod

    def extract_url_product(self):
        """
        Extracts all product urls from the page corresponding to a search in
        Mercado Libre and transforms them into Data objects
        """
        list_url_prod = []
        index = 1
        products = self.ol_products.find_all("li", class_="ui-search-layout__item")
        for product in products:
            url = product.find("a", class_="poly-component__title")
            name = product.find("h3", class_="poly-component__title-wrapper")
            title = name.text.strip() if name else "No defined"
            url_product = DataUrl(
                index, "poly-component__title"
            )
            if url:
                url_product.add_data_web(url)
            else:
                url_product.add_data_web("<<NO INFORMATION>>")
            list_url_prod.append(url_product)
            index += 1
        return list_url_prod


    def extract_start_price_product(self):
        """
        Extracts all product prices (no discount) from the page and transforms
        them into DataText objects
        """
        list_price_prod = []
        index = 1
        products = self.ol_products.find_all("li", class_="ui-search-layout__item")
        for product in products:
            container_prod = product.find(
                "s", class_="andes-money-amount andes-money-amount--previous andes-money-amount--cents-comma")
            price_tag = container_prod.find("span", class_="andes-money-amount__fraction") if container_prod else None
            price_obj = DataText(
                index, {"tag": "span", "class": "andes-money-amount__fraction"}
            )
            price_obj.add_data_text(price_tag.text.strip() if price_tag else "<<NOT APPLY >>")
            list_price_prod.append(price_obj)
            index += 1
        return list_price_prod


    def extract_final_price_product(self):
        """
        Extracts all product prices (with discount) from the page and transforms
        them into DataText objects
        """
        list_price_discount = []
        index = 1
        products = self.ol_products.find_all("li", class_="ui-search-layout__item")
        for product in products:
            container_prod = product.find("div", class_="poly-price__current")
            price_tag = container_prod.find("span", class_="andes-money-amount__fraction") if container_prod else None
            price_obj = DataText(
                index, {"tag": "span", "class": "andes-money-amount__fraction"}
            )
            price_obj.add_data_text(price_tag.text.strip() if price_tag else "<<NO INFORMATION>>")
            list_price_discount.append(price_obj)
            index += 1
        return list_price_discount


    def extract_discount_info(self):
        """
        Extracts discount information if present
        """
        list_discount_info = []
        index = 1
        products = self.ol_products.find_all("li", class_="ui-search-layout__item")
        for product in products:
            discount_tag = product.find("span", class_="andes-money-amount__discount")
            discount_obj = DataText(
                index, {"tag": "span", "class": "andes-money-amount__discount"}
            )
            discount_obj.add_data_text(discount_tag.text.strip() if discount_tag else "<<NOT APPLY >>")
            list_discount_info.append(discount_obj)
            index += 1
        return list_discount_info


    def extract_name_seller(self):
        """
        Extracts the seller's name
        """
        list_sellers = []
        index = 1
        products = self.ol_products.find_all("li", class_="ui-search-layout__item")
        for product in products:
            seller_tag = product.find("span", class_="poly-component__seller")
            seller_obj = DataText(
                index, {"tag": "span", "class": "poly-component__seller"}
            )
            seller_obj.add_data_text(seller_tag.text.strip() if seller_tag else "<<NO INFORMATION>>")
            list_sellers.append(seller_obj)
            index += 1
        return list_sellers


    def extract_score(self):
        """
        Extracts the score (rating) of the product
        """
        list_scores = []
        index = 1
        products = self.ol_products.find_all("li", class_="ui-search-layout__item")
        for product in products:
            score_tag = product.find("span", class_="poly-reviews__rating")
            score_obj = DataText(
                index, {"tag": "span", "class": "poly-reviews__rating"}
            )
            score_obj.add_data_text(score_tag.text.strip() if score_tag else "<<NO INFORMATION>>")
            list_scores.append(score_obj)
            index += 1
        return list_scores


    def extract_quantity_score(self):
        """
        Extracts the total number of reviews
        """
        list_q_scores = []
        index = 1
        products = self.ol_products.find_all("li", class_="ui-search-layout__item")
        for product in products:
            q_score_tag = product.find("span", class_="poly-reviews__total")
            q_score_obj = DataText(
                index, {"tag": "span", "class": "poly-reviews__total"}
            )
            q_score_obj.add_data_text(q_score_tag.text.strip() if q_score_tag else "<<NO INFORMATION>>")
            list_q_scores.append(q_score_obj)
            index += 1
        return list_q_scores

    def extract_complete(self):
        self.create_json()
        n = f"{self.name}_data"
        self.insert_to_json(n, "name_product", self.extract_name_product())
        self.insert_to_json(n, "url_product", self.extract_url_product())
        self.insert_to_json(n, "start_price_product", self.extract_start_price_product())
        self.insert_to_json(n, "final_price_product", self.extract_final_price_product())
        self.insert_to_json(n, "discount_info", self.extract_discount_info())
        self.insert_to_json(n, "name_seller", self.extract_name_seller())
        self.insert_to_json(n, "score", self.extract_score())
        self.insert_to_json(n, "quantity_score", self.extract_quantity_score())