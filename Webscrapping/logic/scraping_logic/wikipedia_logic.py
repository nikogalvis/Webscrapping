"""
This module container the object wikipedia derived from tha class StaticWeb,
besides of contain everything functions an classes for the correct function of
the webscraping in Wikipedia
"""

from bs4 import BeautifulSoup
import requests
import os
import json

from models.models_website import StaticWeb
from models.models_data import Data, DataContainer, DataUrl, DataText
from config.settings import Config

#Call to the general configuration container dictionary
if not os.path.exists("config/config_program.json"):
    config = Config()
    config.save_config_json()
with open("config/config_program.json", "r", encoding="utf-8") as file:
    config_ = json.load(file)

## constant variables for suggested search
type_search = "normal"
limit_search = config_["wp_quantity_search"]
##

#Class Wikipedia
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
        self.html = self.beautiful_soup()
        self.container_data = self.html.find(
            "div", class_ = "mw-content-ltr mw-parser-output")
        self.principal_title = self.html.find("h1")

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

    def extract_associated_url(self):
        """
        Find all URLs found in the paragraphs and lists of the useful information
        container on the web page, excluding those related to references.
        apply a filter and immediately insert into json
        """
        if config_["wp_with_urls_asocciated"]:
            e = super().extract_associated_url()
            self.insert_to_json(f"{self.name}_data", "urls_rasocciated", e)

    def extract_url_Reference(self):
        """
        Extracts all referring URLs and creates DataUrl objects
        apply a filter and immediately insert into json
        """
        if config_["wp_with_urls_references"]:
            e = super().extract_url_Reference()
            self.insert_to_json(f"{self.name}_data", "url_references", e)

    def extraction_complete(self):
        """
        Executes all extraction methods, if the conditions are met
        """
        self.extract_full_data()
        self.create_json()
        self.save_data_in_json()
        self.extract_associated_url()
        self.extract_url_Reference()


##Customization features for creating Wikipedia instances
def search_suggestions(word: str)-> dict[str]:
    """
    requests the API for related searches and their links based on a given word
    """
    parameters = {
    "action": "opensearch",
        "search": word,
        "limit": limit_search,
        "profile": type_search,
        "namespace": 0,
        "format": "json"
        }
    search = requests.get(f"https://{config_['wp_language']}.wikipedia.org/w/api.php", parameters)
    if search.status_code == 200: #200 means no errors
        data = search.json()
        suggestions = list(zip(data[1], data[3]))  #Titles and URLs
        return suggestions
    else:
        print(f"Error: {search.status_code}")
        return None

def create_url(word: str):
    """
    With the search suggestions in search suggestions() the link is generated
    according to the option chosen by the user
    """
    searches = search_suggestions(word)
    for search in searches:
        print(search) 
    try:
        search = int(input("select a search option: ")) #Receives a number from 1 to quantity_Search
        return Wikipedia(searches[search - 1][0], searches[search - 1][1])
    except (TypeError, IndexError):
        print("Error, The URL could not be obtained")