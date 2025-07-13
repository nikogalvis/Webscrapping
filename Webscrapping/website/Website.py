from bs4 import BeautifulSoup

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
    self.__data = None
    self.__password = "HollowKnight"

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
    if (password == self.__password):
      self.__name = new_url
      print("The url was updated")
    else:
      print("Wrong Password") 

  def save_data(self):
    """
    Save the data recolected
    """
    if self.__data is None:
      return "There's no data to save"
    
    with open(f"{self.__name}_data.txt", "w", encoding ="utf-8") as file:
      file.write(str(self.__data))
    print("Succefully saved data! ;3 ")

  def reset_data(self):
    """
    Reset the recolected data
    """
    self.__data = None
    try:
      with open(f"{self.__name}_data.text", "w", encoding ="utf-8") as file:
        file.write(str(""))
    except FileNotFoundError:
      return "This file doesn't exist, maybe you write the name wrong"
    
  def export_data(self): #TODO Necesitamos la clase Document para poder exportar esta wea
    """
    Exports the data to the class Document
    """
    if self.__data is None:
      return "There's no data to export"
    
    else:
      # doc = Document(type = "word", data = "self.__data")
      return
