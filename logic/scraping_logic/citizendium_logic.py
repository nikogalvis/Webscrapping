"""
This module container the object Citizendium derived from tha class StaticWeb,
besides of contain everything functions an classes for the correct function of
the webscraping in Citizendium
"""

from bs4 import BeautifulSoup
import requests

from models.models_website import StaticWeb
from models.models_data import Data, DataContainer, DataUrl

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