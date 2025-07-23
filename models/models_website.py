"""
In this module you will find all the classes to create and manage websites for
data scraping
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
import os
import time
from selenium.webdriver.firefox.options import Options as Opt_firefox
from selenium.webdriver.chrome.options import Options as Opt_chrome
from selenium.webdriver.edge.options import Options as Opt_edge

from models.models_data import (
    Data, DataContainer, DataImage, DataList, DataText, DataUrl)
from config.settings import Config

#Call to the general configuration container dictionary
if not os.path.exists("config/config_program.json"):
    config = Config()
    config.save_config_json()
with open("config/config_program.json", "r", encoding="utf-8") as file:
    config_ = json.load(file)

class WebPage:
    """
    Base class
    Store HTML, prepare it to the subclasses
    This can save, reset, and export data
    """

    def __init__(self, name: str, url: str):
        """
        Starts the page with a name and URL, and create a Password
        """
        self.__name = name
        self.__url = url
        self.__html = "" 
        self._data = {}

    #This variable corresponds to the readable HTML and not the one obtained directly
    @property
    def html(self):
        """
        keep the html readable
        """
        return self.__html
        print("HTML was succefully saved")

    @html.setter
    def html(self, new_html: str):
        """
        Change the readable html
        """
        self.__html = new_html

    def beautiful_soup(self):
        """
        Parser the HTML of the web page, and prepare "soup" for other subclasses
        """
        raise NotImplementedError("Subclasses must implement the beatiful_soup() method")

    def reset_html(self):
        """
        leave the html empty
        """
        self.__html = ""

    @property
    def name(self)-> str:
        """
        Get the name of the page
        """
        return self.__name

    @name.setter
    def name(self, new_name: str):
        """
        Check the password, and change the name of the page
        """
        self.__name = new_name
        print("The name was updated")

    @property
    def url(self) -> str:
        """
        Return the name of the page
        """
        return self.__url

    @url.setter
    def url(self, new_url: str):
        """
        Check the password, and set a new url
        """
        self.__url = new_url
        print("The url was updated")

    def create_json(self, folder: str):
        """     
        Create an empty JSON file inside a subfolder of 'data_json', 
        like 'data_products' or 'data_wiki'.
        """
        base_folder = os.path.join("data_json", folder)
        os.makedirs(base_folder, exist_ok=True)
        file_name = f"{self.name}_data.json"
        path = os.path.join(base_folder, file_name)
        if os.path.exists(path):
            print(f"El archivo ya existe en: {path}")
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

    def add_data(self, data: Data):
        """
        Save the data recolected
        """
        self._data[data.get_title()] = data

    def reset_data(self):
        """
        Reset the recolected data
        """
        self._data = {}

    def save_data_in_json(self, folder: str):
        """      
        Sends the data stored in self._data to a specified .json
        """
        if not os.path.exists(f"data_json/{folder}/{self.name}_data.json"):
            raise FileNotFoundError(f"{self.name}_data.json not exists")
        path = f"data_json/{folder}/{self.name}_data.json"
        d = {f"text_{self.name}": []}
        for data in self._data[f"text_{self.name}"]:
            d[f"text_{self.name}"].append(data.to_dict())
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=4, ensure_ascii=False)
            print(f"Saved JSON at: {path}")
        except TypeError:
            print("One or more objects are not serializable.")

    def load_json(self, file_name: str, folder: str) -> dict:
        """
        Loads and returns data from a JSON file. If file doesn't exist, returns empty dict
        """
        path = f"data_json/{folder}/{file_name}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def insert_to_json(self, file_name: str, key: str, objects: list[Data], folder: str):
        """
        Converts given objects to serializable form and appends them under the specified key
        in the given JSON file located at data_json/<folder>/<file_name>.json
        """
        base_folder = os.path.join("data_json", folder)
        os.makedirs(base_folder, exist_ok=True)
        path = os.path.join(base_folder, f"{file_name}.json")
        data = self.load_json(file_name, folder)
        if isinstance(objects, list):
            d = [obj.to_dict() if hasattr(obj, "to_dict") else obj for obj in objects]
        else:
            d = []
        if key in data and isinstance(data[key], list):
            data[key].extend(d)
        else:
            data[key] = d
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class StaticWeb(WebPage):
    """
    subclass for websites that do not use JavaScript
    """
    def __init__(self, name: str, url: str):
        """
        Starts the page with a name and URL
        """
        super().__init__(name, url)

    def beautiful_soup(self):
        """
        Parser the HTML, and prepare "soup" for static websites
        """
        html = requests.get(self.url).text
        bs = BeautifulSoup(html, "lxml")
        self.html = bs
        print("The soup is ready!")
        return bs

    def create_json(self):
        return super().create_json("data_wiki")

    def save_data_in_json(self):
        return super().save_data_in_json("data_wiki")

    def insert_to_json(self, file_name, key, objects):
        return super().insert_to_json(file_name, key, objects, "data_wiki")

    ###########################################################################
    #The following methods apply for two wiki type websites which are the same on both
    ###########################################################################
    @staticmethod
    def filter_in_paragraphs(tag_search):
        """
        filter to get only paragraphs and lists that are not related to the
        references
        """
        if tag_search.name == "p":
            return True
        class_ = tag_search.get("class", [])
        if tag_search.name in ["ol", "ul"] and "reference" not in class_:
            return True
        return False

    def extract_associated_url(self):
        """
        Find all URLs found in the paragraphs and lists of the useful information
        container on the web page, excluding those related to references
        """
        contain_tag = self.container_data.find_all(StaticWeb.filter_in_paragraphs)
        urls = []
        for tag in contain_tag:
            for a in tag.find_all("a", href = True):
                obj = DataUrl(a.get("title", ""), a.get("class", []))
                obj.add_data_web(a) 
                urls.append(obj)
        return urls

    def extract_url_Reference(self):
        """
        Extracts all referring URLs and creates DataUrl objects
        """
        contain_tag = self.container_data.find_all(["ol", "ul"], class_ = "references")
        urls = []
        for tag in contain_tag:
            for a in tag.find_all("a", href = True):
                obj = DataUrl(a.get("title", ""), a.get("class", []))
                obj.add_data_web(a) 
                urls.append(obj)
        return urls
    ###########################################################################

class DinamicWeb(WebPage):
    """
    subclass for websites that do use JavaScript
    """
    def __init__(self, name: str, url: str):
        """
        Starts the page with a name and URL
        """
        super().__init__(name, url)
        self.__driver = webdriver.Chrome() #Standar browser

    @property
    def driver(self):
        """
        returns the browser that opens the dynamic page
        """
        return self.__driver

    #page load time
    load_time = config_["ml_time_sleep"]

    def beautiful_soup(self):
        """
        Parser the HTML, and prepare "soup" for dinamic websites
        """
        try:
            self.driver.get(self.url)
            time.sleep(self.load_time)
            html = self.driver.page_source
            bs = BeautifulSoup(html, "lxml")
            print("The soup is ready!")
            self.html = bs
            return bs
        except AttributeError:
            raise("Driver is not defined")

    @driver.setter
    def driver(self, new_driver):
        self.__driver = new_driver

    def create_json(self):
        return super().create_json("data_product")

    def save_data_in_json(self):
        return super().save_data_in_json("data_product")

    def insert_to_json(self, file_name, key, objects):
        return super().insert_to_json(file_name, key, objects, "data_product")