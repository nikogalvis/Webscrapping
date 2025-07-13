"""
In this module you will find the classes related to websites except specific
class reference to specific websites
"""

from bs4 import BeautifulSoup
from selenium import webdriver

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
        self.__data = {}
        self.__password = "HollowKnight" #Posiblemente se cambie el manejo de la contraseña

    def set_html(self, html: str, url: str):
        """
        Save the HTML of a page, 
        and update the URL that we are working
        """
        
        self.__html = html
        self.__url = url
        print("HTML was succefully saved")

    def beautiful_soup(self, html, type_data):
        """
        Parser the HTML, and prepare "soup" for other subclasses
        """
        soup = BeautifulSoup(html, "lxml")
        print("The soup is ready!")

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
        if (password == self.__password): #Posiblemente se cambie el manejo de la contraseña
            self.__name = new_url
            print("The url was updated")
        else:
            print("Wrong Password") 

    def save_data(self, data:Data, name_data:str, password:str):
        """
        Saves the data recolected
        """
        if not isinstance(data, Data):
            raise TypeError("data no valid")
        if password == self.__password: #Posiblemente se cambie el manejo de la contraseña
            self.__data[name_data] = data
            print("data save")
        else:
            print("Access denied")



    def reset_data(self, password:str):
        """
        Reset the recolected data
        """
        if password == self.__password: #Posiblemente se cambie el manejo de la contraseña
            self.__data = {}
        else:
            print("Access denied")
        
    def export_data(self): #TODO Necesitamos la clase Document para poder exportar esta wea
        """
        Exports the data to the class Document
        """
        pass
        #if self.__data is None:
            #return "There's no data to export"
        
        #else:
        # doc = Document(type = "word", data = "self.__data")
            #return
    
    def delete_data(self, name_data:str, password:str):
        """
        Deletes data according to the assigned name
        """
        if password == self.__password: #Posiblemente se cambie el manejo de la contraseña
            try:
                del self.__data[name_data]
            except KeyError:
                print("data not found")
        else:
            print("Access denied")


class StaticWeb(WebSites):
    """
    the class only that it work with html (static)
    """
    def __init__(self, name, url):
        """
        Starts the page with a name and URL
        """
        super().__init__(name, url)
    
    def add_data(self, new_data:Data):
        """
        Adds data to dictionary (list of data corresponding to __data)
        """
        raise NotImplementedError("Subclasses must implement add_data()")


class DinamicWeb(WebSites):
    def __init__(self, name, url):
        """
        Starts the page with a name and URL
        """
        super().__init__(name, url)
    
    #Tuple of posible browsers
    list_browser:dict[str] = {
        "Chrome" : webdriver.Chrome,
        "Firefox" : webdriver.Firefox,
        "Edge" : webdriver.Edge
        }

    def add_data(self, new_data:Data):
        """
        Adds data to dictionary (list of data corresponding to __data)
        """
        raise NotImplementedError("Subclasses must implement add_data()")

    def access_browser(self, browser:str):
        """
        Create the driver for you access the web through the browser
        """
        if  not browser in self.list_browser:
            raise  ValueError("Browser not supported")
        driver = self.list_browser[browser]
        return driver