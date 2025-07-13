from bs4 import BeautifulSoup

class Data:
    def __init__(self, title: str, type_tag:dict = {"tag" : None, "class" : None}):
        """
        Initialize the Data with title and type.
        """
        self.__title = title
        self.__type_tag = type_tag
        self.__data = {}
        self.__password = "HollowKnight" #Posibles cambios al manejo de la password

    def add_data_web(self, data):
        """
        Set the internal data directly (used in subclasses).
        """
        self.__data = data

    def get_type(self) -> str:
        """
        Return the type of the data.
        """
        return self.__type_tag

    def set_type(self, new_type_tag:dict, password:str) -> str:
        """
        Update the type if password is correct.
        """
        if password == self.__password:
            self.__type_tag = new_type_tag
        else:
            print("Invalid password")

    def get_data(self, password: str):
        """
        Return the stored data if password is correct.
        """
        if password == self.__password:
            return self.__data
        return "Access denied"

    def get_title(self) -> str:
        """
        Return the title of the data.
        """
        return self.__title

    def set_title(self, new_title: str, password: str) -> str:
        """
        Update the title if the password is correct.
        """
        if password == self.__password:
            self.__title = new_title
        else:
            print("Invalid password")

    def to_dict(self)-> dict:
        """      
        Converts data objects into dictionaries for handling in JSON
        """
        dictionary = {
            "title" : self.__title,
            "type_tag" : self.__type_tag,
            "data" : self.__data
        }
        return dictionary


class DataImage(Data):
    def __init__(self, title, class_):
        """
        Initialize the DataImage with title and type <img>.
        """
        super().__init__(title, {"tag" : "img", "class" : class_})


class DataUrl(Data):
    def __init__(self, title, class_):
        """
        Initialize the DataUrl with title and type <a>.
        """
        super().__init__(title, {"tag" : "a" , "class" : class_})


class DataTable(Data):
    def __init__(self, title, class_):
        """
        Initialize the DataTable with title and type <table>.
        """
        super().__init__(title, {"tag" : "table", "class" : class_})
    
    def set_data_web(self, table_html):
        """
        Receives a <table> HTML element and parses caption, header, and body.
        """
        self._Data__data = {}
        self._Data__data["caption"] = table_html.find("caption") if table_html.find("caption") else None
        header = table_html.find("thead")
        body = table_html.find("tbody")
        if header:
            tr = header.find_all("tr")
            self._Data__data["thead"] = [
                [th.text.strip() for th in row.find_all("th")] for row in tr]
            tr = body.find_all("tr")
            self._Data__data["tbody"] = [
                [td.text.strip() for td in row.find_all("td")] for row in tr]
        else:
            rows = table_html.find_all("tr")
            self._Data__data["tr"] = [
                [td.text.strip() for td in row.find_all("td")] for row in rows]