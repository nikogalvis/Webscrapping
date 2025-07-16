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

from models_data import Data

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

class DinamicWeb(WebPage):
    """
    subclass for websites that do use JavaScript
    """
    def __init__(self, name: str, url: str):
        """
        Starts the page with a name and URL
        """
        super().__init__(name, url)
        self.__driver = None
    
    supported_drivers = {
            "Chrome": webdriver.Chrome,
            "Firefox": webdriver.Firefox,
            "Edge": webdriver.Edge
        }

    @property
    def driver(self):
        """
        returns the browser that opens the dynamic page
        """
        return self.__driver

    @driver.setter
    def driver(self, new_driver):
        """
        Change the browser driver based on the specified browser name.
        Supported browsers: 'chrome', 'firefox', 'edge'
        """
        new_driver = new_driver.lower()
        new_driver = new_driver.capitalize() #Change everything to lowercase
        if new_driver in self.supported_drivers:
            self.__driver = self.supported_drivers[new_driver]
            print(f"{new_driver} driver started successfully.")
        else:
            print(f"Browser '{new_driver}' not supported.")


    def hide_page(self, browser):
        """
        Hide the page that is automated with .page_source
        """
        browser = browser.lower()
        if browser == "chrome":
            options = Opt_chrome()
        elif browser == "edge":
            options = Opt_edge()
        elif browser == "firefox":
            options = Opt_firefox()
            options.headless = True
            return options
        else:
            print(f"Browser '{browser}' not supported.")
            return
        options.add_argument("--headless")
        return options

    #page load time
    load_time = 10

    def beautiful_soup(self):
        """
        Parser the HTML, and prepare "soup" for dinamic websites
        """
        driver = self.driver()
        driver.get(self.url)
        time.sleep(self.load_time)
        html = driver.page_source
        bs = BeautifulSoup(html, "lxml")
        print("The soup is ready!")
        self.html = bs
        return bs