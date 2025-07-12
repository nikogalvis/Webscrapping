from bs4 import BeautifulSoup

class WebSites:
  def __init__(self, name: str, url: str):
    self.__name = name
    self.__url = url
    self.__data = ""
    self.__password = "HollowKnight"

  def set_html(self, html: str, url: str):
    self.__html = html
    self.__url = url
    print("HTML was succefully saved")

  def beautiful_soup(self, html, type_data):
    soup = BeautifulSoup(html, "lxml")
    print("The soup is ready!")

  def get_name(self)-> str:
    return self.__name
  
  def set_name(self, new_name: str, password: str):
    if (password == self.__password):
      self.__name = new_name
      print("The name was updated")
    else:
      print("Wrong Password")
  
  def get_url(self) -> str:
    return self.__url
  
  def set_url(self, new_url: str, password: str):
    if (password == self.__password):
      self.__name = new_url
      print("The url was updated")
    else:
      print("Wrong Password") 

  def save_data(self):
    if self.__data is None:
      return "There's no data to save"
    
    with open(f"{self.__name}_data.txt", "w", encoding ="utf-8") as file:
      file.write(str(self.__data))
    print("Succefully saved data! ;3 ")

  def reset_data(self):
    self.__data = None
    try:
      with open(f"{self.__name}_data.text", "w", encoding ="utf-8") as file:
        file.write(str(""))
    except FileNotFoundError:
      return "This file doesn't exist, maybe you write the name wrong"
    
  def export_data(self): #TODO Necesitamos la clase Document para poder exportar esta wea
    if self.__data is None:
      return "There's no data to export"
