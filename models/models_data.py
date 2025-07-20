"""
This module references all the data classes obtained from a website's HTML
They are stored as dictionaries and lists
"""
from bs4 import BeautifulSoup
import pandas
import numpy

class Data:
    def __init__(self, title: str, type_tag:dict = {"tag" : None, "class" : None}):
        """
        Initialize the Data with title and type
        """
        self.__title = title
        self.__type_tag = type_tag
        self._data = {}
        self.index = 0

    @property
    def data(self):
        """
        return the data
        """
        return self._data

    @data.setter
    def data(self, new_data):
        """
        changes the data
        """
        self._data = new_data

    def add_data_web(self, data):
        """
        Set the internal data directly (used in subclasses)
        """
        raise NotImplementedError("Method implemented by subclasses")

    @property
    def type(self) -> str:
        """
        Return the type of the data
        """
        return self.__type_tag

    @type.setter
    def type(self, new_type_tag:dict) -> str:
        """
        Update the type
        """
        self.__type_tag = new_type_tag

    def set_value(self, key, value):
        if value is not None:
            self._data[key] = value
        else:
            print(f"WARNING: Not setting {key} because value is None")

    @property
    def title(self) -> str:
        """
        Return the title of the data
        """
        return self.__title

    @title.setter
    def title(self, new_title: str) -> str:
        """
        Update the title
        """
        self.__title = new_title

    def extract_sub_data(self, container_html, filter_ = None):
        """
        For a tag container, create objects for each tag.
        exception_ is a boolean exception to filter tags
        """
        sub_data = []
        for t in container_html.find_all(filter_):
            if not hasattr(t, "name") or t.name is None:
                continue  #Ignore unnecessary text
            class_ = t.get("class")
            title_ = t.get("title")
            if t.name == "a":
                obj = DataUrl(title_, class_)
                obj.add_data_web(t)
            elif t.name in ["img", "figure"]:
                obj = DataImage(title_, class_)
                obj.add_data_web(t)
            elif t.name in [
                "p", "b", "h1", "h2", "h3", "h4", "h5", "h6", "span"]:
                obj = DataText(f"text_{t.name}_{self.index}", {"tag" : t.name, "class" : class_})
                obj.add_data_web(t)
            elif t.name in ["ol", "ul"]:
                obj = DataList(f"list_{t.name}_{self.index}", {"tag" : t.name, "class" : class_})
                obj.add_data_web(t)
            elif t.name == "table":
                obj = DataTable(f"table_{t.name}_{self.index}", class_)
                obj.add_data_web(t, False)
            else:
                continue
            sub_data.append(obj)
            self.index += 1
        return sub_data

    def to_dict(self):
        """
        Returns the class information as a dictionary to be passed to json
        """
        return {self.title : self.data}

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
        self.set_value(data_img.get("title"), data_img.get("src"))


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
        self.set_value(data_url.get("title"), data_url.get("href"))


class DataTable(Data):
    """
    This class refers to the data type table
    """
    def __init__(self, title: str, class_: str):
        """
        Initialize the DataTable with title and tag <table>
        """
        super().__init__(title, {"tag" : "table", "class" : class_})

    def add_data_web(self, table_html, with_index: bool):
        """
        Receives a <table> HTML element and parses caption, header, and body
        """
        table = pandas.read_html(str(table_html))
        self.set_value(f"{self.title}", table)

    def to_dict(self):
        """
        Serializes the content of the DataTable object to a dictionary,
        converting pandas DataFrames into JSON-friendly format.
        """
        serialized = {}
        for idx, df in enumerate(self.data.get(self.title, [])):
            key = f"{self.title}_{idx}"
            if isinstance(df, pandas.DataFrame):
                df_clean = df.replace({numpy.nan: None, pandas.NaT: None})
                serialized[key] = df_clean.to_dict(orient="records")
            else:
                serialized[key] = str(df)  # fallback, shouldn't usually happen
        return serialized


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
        self.set_value(f"{self.title}", data_text.get_text(strip=True))

    def add_data_text(self, text: str):
        """      
        receive the text directly and save it, can also be None
        """
        self.set_value(f"{self.title}", text)


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
        self.data = {}
        self.set_value(
            "li",
            [li.get_text(strip=True) for li in list_html.find_all("li")])


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

    def add_data_web(self, container_html, filter = None):
        """
        Receives an HTML container and parses each sub_tag
        """
        extracted = self.extract_sub_data(container_html, filter)
        if extracted:
            key = f"{self.title}"
            self._data[key] = extracted
        else:
            print(f"WARNING: Empty container data for '{self.title}' (HTML)")

    def to_dict(self):
        """
        Converts data objects into a single dictionary to save as JSON.
        Each entry has the title as key and its associated data as value.
        """
        return {k: v.data for k, v in self._data.items()}