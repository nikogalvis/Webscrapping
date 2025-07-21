"""
This module container the object Citizendium derived from tha class StaticWeb,
besides of contain everything functions an classes for the correct function of
the webscraping in Citizendium
"""

from bs4 import BeautifulSoup
import requests
import os
import json

from models.models_website import StaticWeb
from models.models_data import Data, DataContainer, DataUrl
from config.settings import Config

#Call to the general configuration container dictionary
if not os.path.exists("config/config_program.json"):
    config = Config()
    config.save_config_json()
with open("config/config_program.json", "r", encoding="utf-8") as file:
    config_ = json.load(file)

class Citizendium(StaticWeb):
    """
    Class that allows you to manage a Wikipedia web page
    """
    def __init__(self, name, url):
        """
        Starts the page with a name and URL
        """
        super().__init__(name, url)
        self.html = self.beautiful_soup()
        self.container_data = self.html.find(
            "div", class_ = "mw-parser-output")
        self.principal_title = self.html.find("h1")

    def extract_full_data(self):
        """
        Create a DataContainer object to apply the object's data retrieval
        method and save it as data
        """
        obj = DataContainer(
            f"text_{self.name}", {"tag" : "div", "class" : "mw-content-text"})
        obj.add_data_web(
            self.container_data, self.data_extraction_filter)
        self._data = obj._data

    @staticmethod
    def data_extraction_filter(tag) -> bool:
        """
        Filter to be used to search for tags ignoring unnecessary tables
        """
        if tag.name in ["p", "h1", "h2", "h3", "h4", "h5", "h6", "ol", "ul"]:
            return True
        class_ = tag.get("class", [])
        if tag.name == "table" and "noprint" not in class_:
            return True
        return False

    def extract_associated_url(self):
        """
        Find all URLs found in the paragraphs and lists of the useful information
        container on the web page, excluding those related to references.
        apply a filter and immediately insert into json
        """
        if config_["ct_with_urls_asocciated"]:
            e = super().extract_associated_url()
        self.insert_to_json(f"{self.name}_data", "urls_rasocciated", e)

    def extract_url_Reference(self):
        """
        Extracts all referring URLs and creates DataUrl objects
        apply a filter and immediately insert into json
        """
        if config_["ct_with_urls_references"]:
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