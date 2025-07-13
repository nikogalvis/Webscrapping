"""
In the module you will find all the class releated to the types datas get in
the web to scrapp
"""

from bs4 import BeautifulSoup

class Data:
    """
    Base class for the all types of datas get in the web to scrapp
    """
    def __init__(self, title:str, type_tag:dict = None):
        """
        Starts the data with a title and type tag, and create a Password
        """
        self.__title = title
        self.__type_tag = type_tag or {"tag" : None, "class" : None} #type_tag also contains the class for dynamic websites
        self.__data = None
        self.__password = "HollowKinght" #Posiblemente se cambie el manejo de la contraseña

    def set_data_web(self, data):
        """
        Add data depending on the tag and class
        """
        self.__data = data

    def get_title(self):
        """
        Return the type_tag
        """
        return self.__title

    def set_title(self, password:str, new_title:str):
        """
        Change the value of type_tag
        """
        if password == self.__pasword: #Posiblemente se cambie el manejo de la contraseña
            self.__title = new_title
            print("The type_tag was updated")
        else:
            print("Wrong Password")

    def get_type(self):
        """
        Return the type_tag
        """
        return self.__type_tag

    def set_data(self):
        """
        Return the data depending on the tag and class
        """
        raise NotImplementedError("Subclasses must implement add_data_web()")

class DataImage(Data):
    """
    Creates a specialized Data instance for extracting images.
    """
    def __init__(self, title, class_:str):
        """
        Starts the data with a title and type tag <img>
        """
        super().__init__(title = title, type_tag = {"tag" : "img", "class" : class_})

class DataUrl(Data):
    """
    Creates a specialized Data instance for extracting url.
    """
    def __init__(self, title, class_:str):
        """
        Starts the data with a title and type tag <a>
        """
        super().__init__(title, {"tag" : "a", "class" : class_})

class DataTable(Data):
    """
    Creates a specialized Data instance for extracting tables.
    """
    def __init__(self, title, class_:str):
        """
        Starts the data with a title and type tag <a>
        """
        super().__init__(title, {"tag" : "table", "class" : class_})
        self.__data = {}

    def set_data_web(self, data):
        """       
        receives the HTML part with the table tag and takes the information
        according to the sub-tags

        data = html of tag <table>
        """
        self.__data["caption"] = data.find("caption") if data.find("caption") else None
        header = data.find("thead")
        body = data.find("tbody")
        if header:
            tr = header.find_all("tr")
            self.__data["thead"] = [
            [th.text.strip() for th in fila.find_all("th")] for fila in tr]
            tr = body.find_all("tr")
            self.__data["tbody"] = [
            [td.text.strip() for td in f.find_all("td")] for f in tr]
        else:
            rows = data.find_all("tr")
            self.__data["tr"] = [
                [td.text.strip() for td in f.find_all("td")] for f in rows]
