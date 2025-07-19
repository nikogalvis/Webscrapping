"""
This module container the object wikipedia derived from tha class StaticWeb,
besides of contain everything functions an classes for the correct function of
the webscraping in Wikipedia
"""

from bs4 import BeautifulSoup
import requests

from models.models_website import StaticWeb
from models.models_data import Data, DataContainer, DataUrl, DataText

class Wikipedia(StaticWeb):
    """
    Class that allows you to manage a Wikipedia web page with special methods
    according to the permissions of its API
    """
    def __init__(self, name: str, url: str):
        """
        Starts the page with a name, URL and  api URL
        """
        super().__init__(name, url)
        self.__api = "https://en.wikipedia.org/w/api.php"
        self.html = self.beautiful_soup()
        self.container_data = self.html.find(
            "div", class_ = "mw-content-ltr mw-parser-output")
        self.principal_title = self.html.find("h1")

    ## constant variables for suggested search
    type_search = "normal"
    limit_search = 7

    def change_api_language(self, api_language: str):
        """
        Change the language subdomain of the api url
        """
        self.__api = f"https://{api_language}.wikipedia.org/w/api.php"

    def search_suggestions(self, word: str)-> dict[str]:
        """
        requests the API for related searches and their links based on a given word
        """
        parameters = {
            "action": "opensearch",
            "search": self.type_search,
            "limit": self.limit_search,
            "namespace": 0,
            "format": "json"
            }
        search = requests.get(self.__api, parameters)
        if search.status_code == 200: #200 means no errors
            data = search.json()
            suggestions = list(zip(data[1], data[3]))  #Titles and URLs
            return suggestions
        else:
            print(f"Error: {search.status_code}")
            return None

    def create_url(self, word: str):
        """
        With the search suggestions in search suggestions() the link is generated
        according to the option chosen by the user
        """
        searches = self.search_suggestions(word)
        try:
            search = int(input("select a search option: ")) #Receives a number from 1 to 7
            self.url(searches[search - 1][0])
            self.name(searches[search - 1][1])
        except (TypeError, IndexError):
            print("Error, The URL could not be obtained")

    def extract_full_data(self):
        """
        Create a DataContainer object to apply the object's data retrieval
        method and save it as data
        """
        obj = DataContainer(
            f"text_{self.name}", {"tag" : "div", "class" : "mw-content-ltr mw-parser-output"})
        obj.add_data_web(
            self.container_data, ["p", "h1", "h2", "h3", "h4", "h5", "h6", "ol", "ul", "table"])
        self._data = obj.data