import json
from openpyxl import Workbook
from Webscrapping import Documents

class DocumentExcel(Documents):
  def __init__(self, name):
    self.path = name
    self.data = []
    super().__init__(name = self.path, type = "Excel")

  def load_data(self):
    try:
      with open(self.path, encoding = "utf-8") as f:
        self.data = json.load(f)
    except Exception:
      print(f"Load of {self.path}, failed")


  def create_document(self, title: "str"):
    if not self.data:
      raise FileNotFoundError("No data found")
    
    excel = Workbook()
    page = excel.active
    page.title = title

    heads = list(self.data[0].keys())
    page.append(heads)

    for item in self.data:
      row = []
      for cipher in heads:
        value = item.get(cipher, "")
        row.append(value)
      page.append(row)

    excel.save(f"{title}.xlsx")

    

