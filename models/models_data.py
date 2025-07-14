"""
This module references all the data classes obtained from a website's HTML
They are stored as dictionaries and lists
"""
from bs4 import BeautifulSoup

class Data:
    def __init__(self, title: str, type_tag:dict = {"tag" : None, "class" : None}):
        """
        Initialize the Data with title and type
        """
        self.__title = title
        self.__type_tag = type_tag
        self._data = {}
        self.__password = "HollowKnight" #Posibles cambios al manejo de la password

    def add_data_web(self, data):
        """
        Set the internal data directly (used in subclasses)
        """
        self._data = data

    def get_type(self) -> str:
        """
        Return the type of the data
        """
        return self.__type_tag

    def set_type(self, new_type_tag:dict, password:str) -> str:
        """
        Update the type if password is correct
        """
        if password == self.__password:
            self.__type_tag = new_type_tag
        else:
            print("Invalid password")

    def get_data(self, password: str):
        """
        Return the stored data if password is correct
        """
        if password == self.__password:
            return self._data
        return "Access denied"

    def get_title(self) -> str:
        """
        Return the title of the data
        """
        return self.__title

    def set_title(self, new_title: str, password: str) -> str:
        """
        Update the title if the password is correct
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
            "data" : self._data
        }
        return dictionary

    def extract_sub_data(self, container_html):
        sub_data = []
        for t in container_html.descendants:
            if not hasattr(t, "name") or t.name is None:
                continue  #Ignore unnecessary text
            class_ = t.get("class")
            title_ = t.get("title")
            if t.name == "a":
                obj = DataUrl(title_, class_)
                obj.add_data_web(t)
            elif t.name == "img":
                obj = DataImage(title_, class_)
                obj.add_data_web(t)
            elif t.name in ["p", "b", "h1", "h2", "h3", "h4", "h5", "h6",]:
                obj = DataText("text", {"tag" : t.name, "class" : class_})
                obj.add_data_web(t)
            elif t.name in ["div", "section", "article", "nav", "header", "footer"]:
                obj = DataContainer("container", {"tag" : t.name, "class" : class_})
                obj.add_data_web(self.extract_sub_data(t))
            elif t.name in ["ol", "ul"]:
                obj = DataList("list", {"tag" : t.name, "class" : class_})
                obj.add_data_web([li.get_text(strip=True) for li in t.find_all("li")])
            else:
                return None
            sub_data.append(obj)
        return sub_data

class DataImage(Data):
    """
    This class refers to image tag <img>
    """
    def __init__(self, title: str, class_: str):
        """
        Initialize the DataImage with title and type <img>
        """
        super().__init__(title, {"tag" : "img", "class" : class_})

    def add_data_web(self, data_img):
        """
        receives the part of the HTML corresponding to tag <img> and return the
        src attribute
        """
        self._data = data_img.get("src")


class DataUrl(Data):
    """
    This class refers to the data type link
    """
    def __init__(self, title: str, class_: str):
        """
        Initialize the DataUrl with title and tag <a>
        """
        super().__init__(title, {"tag" : "a" , "class" : class_})

    def add_data_web(self, data_url):
        """
        receives the part of the HTML corresponding to tag <a> and return the
        href attribute
        """
        self._data = data_url.get("href")


class DataTable(Data):
    """
    This class refers to the data type table
    """
    def __init__(self, title: str, class_: str):
        """
        Initialize the DataTable with title and tag <table>
        """
        super().__init__(title, {"tag" : "table", "class" : class_})

    def set_data_web(self, table_html):
        """
        Receives a <table> HTML element and parses caption, header, and body
        """
        self._data = {}
        self._data["caption"] = table_html.find("caption") if table_html.find("caption") else None
        header = table_html.find("thead")
        body = table_html.find("tbody")
        if header:
            tr = header.find_all("tr")
            self._data["thead"] = [
                [th.text.strip() for th in row.find_all("th")] for row in tr]
            tr = body.find_all("tr")
            self._data["tbody"] = [
                [td.text.strip() for td in row.find_all("td")] for row in tr]
        else:
            rows = table_html.find_all("tr")
            self._data["tr"] = [
                [td.text.strip() for td in row.find_all("td")] for row in rows]
        


class DataText(Data):
    """
    This class refers to the data type paragraph or title tag <p>, <b> or
    <h1> - <h6>
    """
    def __init__(self, title, type_tag: dict = { "tag": None,"class": None }):
        """
        Initialize the DataText with title and tag 
        """
        super().__init__(title, type_tag)

    def add_data_web(self, data_text):
        """
        receives the part of the HTML corresponding to the text and return the
        total text
        """
        self._data = data_text.get_text(strip=True)


class DataList(Data):
    """
    This class refers to the data type list
    """
    def __init__(self, title, type_tag = { "tag": None,"class": None }):
        """
        Initialize the DataList with title and tag <ol> or <ul>
        """
        super().__init__(title, type_tag)

    def add_data_web(self, list_html):
        """
        Receives an HTML <ul> or <ol> element and parses each <li> tag
        """
        self._data = {}
        i = 0
        for li in list_html.find_all("li"):
            self._data[f"li{i}"] = self.extract_sub_data(li)
            i += 1


class DataContainer(Data):
    """
    This class refers to the data of tag "div", "section", "article", "nav",
    "header" or "footer"
    """
    def __init__(self, title, type_tag = { "tag": None,"class": None }):
        """
        Initialize the DataContainer with title and tag "div", "section",
        "article", "nav", "header" or "footer"
        """
        super().__init__(title, type_tag)

    def add_data_web(self, container_html):
        """
        Receives an HTML of container and parses each sub_tag
        """
        self._data = self.extract_sub_data(container_html)