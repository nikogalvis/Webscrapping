"""
In this module you will find all the classes to create and manage websites for
data scraping
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import os

from models_data import Data

class WebSites:
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
        self.__password = "HollowKnight"

    def set_html(self, html: str, url: str):
        """
        Save the HTML of a page, 
        and update the URL that we are working
        """
        self.__html = html
        self.__url = url
        print("HTML was succefully saved")

    def beautiful_soup(self, html):
        """
        Parser the HTML, and prepare "soup" for other subclasses
        """
        soup = BeautifulSoup(html, "lxml")
        print("The soup is ready!")
        return soup

    def get_name(self)-> str:
        """
        Get the name of the page
        """
        return self.__name
    
    def set_name(self, new_name: str, password: str):
        """
        Check the password, and change the name of the page
        """
        if (password == self.__password):
            self.__name = new_name
            print("The name was updated")
        else:
            print("Wrong Password")
    
    def get_url(self) -> str:
        """
        Return the name of the page
        """
        return self.__url
    
    def set_url(self, new_url: str, password: str):
        """
        Check the password, and set a new url
        """
        if (password == self.__password):
            self.__url = new_url
            print("The url was updated")
        else:
            print("Wrong Password")
    
    def create_json(self, name_json: str):
        """     
        Create an empty json file
        """
        folder = "data_json"
        os.makedirs(folder, exist_ok=True)
        file_name = f"{self.__name}_{name_json}_data"
        path = path = f"data_json/{file_name}.json"
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
        
    def save_data_in_json(self, file_name):
        """      
        Sends the data stored in self._data to a specified .json
        """
        if not os.path.exists(f"data_json/{file_name}.json"):
            raise FileNotFoundError(f"{file_name}.json not exists")
        path = f"data_json/{file_name}.json"
        dict_data = {title : data.to_dict() for title, data in self._data.items()}
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(dict_data, f, indent=4, ensure_ascii=False)
            print(f"Saved JSON at: {path}")
        except TypeError:
            print("One or more objects are not serializable.")


class StaticWeb(WebSites):
    """
    subclass for websites that do not use JavaScript
    """
    def __init__(self, name: str, url: str):
        """
        Starts the page with a name and URL, and create a Password
        """
        super().__init__(name, url)

class DinamicWeb(WebSites):
    def __init__(self, name, url):
        """
        subclass for websites that do use JavaScript
        """
        super().__init__(name, url)
        self.__driver = None
    
    supported = {
            "chrome": webdriver.Chrome,
            "firefox": webdriver.Firefox,
            "edge": webdriver.Edge
        }

    def access_browser(self, browser: str):
            """
            Initializes the browser driver based on the specified browser name.
            Supported browsers: 'chrome', 'firefox', 'edge'
            """
            browser = browser.lower() #Change everything to lowercase
            if browser in self.supported:
                    self.__driver = self.supported[browser]()
                    print(f"{browser.capitalize()} driver started successfully.")
            else:
                print(f"Browser '{browser}' not supported.")