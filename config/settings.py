"""
This module stores all the classes and functions for creating and modifying a
JSON with general program settings
"""

import json
import os

class Config():
    """
    Class that stores the attributes relating to the options of a settings
    menu and its methods to change them
    """
    def __init__(self):
        self.__wp_language: str = "en"
        self.__wp_quantity_search: int = 7
        self.__wp_with_urls_asocciated: bool = True
        self.__wp_with_urls_references: bool = True
        self.__ct_with_urls_asocciated: bool = True
        self.__ct_with_urls_references: bool = True
        self.__ml_time_sleep: int = 7

    @property
    def setting(self):
        setting = {
            "wp_language" : self.__wp_language,
            "wp_quantity_search" : self.__wp_quantity_search,
            "wp_with_urls_asocciated" : self.__wp_with_urls_asocciated,
            "wp_with_urls_references" : self.__wp_with_urls_references,
            "ct_with_urls_asocciated" : self.__ct_with_urls_asocciated,
            "ct_with_urls_references" : self.__ct_with_urls_references,
            "ml_time_sleep" : self.__ml_time_sleep,
        }
        return setting

    def save_config_json(self, file_name = "config_program"):
        """
        Create and/or save the configuration in a json
        """
        os.makedirs("config", exist_ok = True)
        path = f"config/{file_name}.json"
        with open(path, "w", encoding = "utf-8") as f:
            json.dump(self.setting, f, indent=4)

    def set_wp_lenguage(self, new_lenguage: str):
        """
        Change the language of the Wikipedia API
        """
        language = {"español" : "es", "english" : "en", "deutsche" : "de", "française" : "fr"}
        if new_lenguage in ["español", "english", "deutsche", "française"]:
            self.__wp_language = language[new_lenguage]
            self.save_config_json()

    def set__wp_quantity_search(self, new_quantity):
        """
        Change the quantity suggestions searchs obtained by search_suggestions()
        method
        """
        if isinstance(new_quantity, int):
            self.__wp_quantity_search = new_quantity
            self.save_config_json()

    def set_wp_with_urls_asocciated(self, value: bool):
        """
        Set whether associated URLs should be retrieved in Wikipedia scraping.
        """
        if isinstance(value, bool):
            self.__wp_with_urls_asocciated = value
            self.save_config_json()

    def set_wp_with_urls_references(self, value: bool):
        """
        Set whether reference URLs should be retrieved in Wikipedia scraping.
        """
        if isinstance(value, bool):
            self.__wp_with_urls_references = value
            self.save_config_json()

    def set_ct_with_urls_asocciated(self, value: bool):
        """
        Set whether associated URLs should be retrieved in Citizendium scraping.
        """
        if isinstance(value, bool):
            self.__ct_with_urls_asocciated = value
            self.save_config_json()

    def set_ct_with_urls_references(self, value: bool):
        """
        Set whether reference URLs should be retrieved in Citizendium scraping.
        """
        if isinstance(value, bool):
            self.__ct_with_urls_references = value
            self.save_config_json()

    def set_ml_time_sleep(self, new_time: int):
        """
        Set the waiting time between MercadoLibre scraping actions.
        """
        if isinstance(new_time, int) and new_time >= 0:
            self.__ml_time_sleep = new_time
            self.save_config_json()

    def load_config_json(self, file_name="config_program"):
        """
        Load configuration from JSON and update attributes.
        """
        path = f"config/{file_name}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                for key, value in config_data.items():
                    private_attr = f"_Config__{key}"
                    if hasattr(self, private_attr):
                        setattr(self, private_attr, value)