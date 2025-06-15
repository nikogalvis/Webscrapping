# Programación Orientada a Objetos - UNAL
## Proyecto Final - Alternativa Webscrapping
Decidimos encaminarnos por la alternativa dos, un **Sistema de Webscrapping**

### Definición de alternativa
Un sistema de Webscrapping, es una manera de extraer información de paginas en linea, de manera automatizada, (Algo asi como un copiar y pegar mucho mas eficiente), y con estos datos recolectados, se organizan y se presentan de otra forma, ya sea json, csv, Excel, etc. Este sistema tiene diversos usos, ya sea el monitoreo de precios (De acciones, aplicaciones, juegos, indumentaria, etc), o monitorear las paginas en internet de entidades de interes propio, como se puede observar, la principar funcion de este sistema, es **recopilar información** que pueda ser de utilidad para quien la necesite. En este caso, se extraera información de paginas web estaticas, como lo son las **wikis**, y de paginas web de sitios de retail, como lo puede ser **mercado libre** o **airbnb**.

Además, por el momento, cumpliremos con una **Feature Extra**, se generaran reportes en forma de documentos de la información recopilada de estos sitios, para darle mas profesionalismo a nuestro programa.

## Diagrama de clases

Hemos planteada inicialmente el siguiente *diagrama de clases* para nuestro codigo, este sera el esqueleto del cual partiremos para programar nuestro sistema:

```mermaid
  classDiagram
    class WebSites {
        - name: str
        - main_url: str
        + __init__(name, url)
        + set_html(html, url): str
        + beautiful_soup(html, type_data): Data
        + get_name(): str
        + set_name(new_name, password): str
        + get_url(): str
        + set_url(new_url, password): str
        - save_data()
        - reset_data()
        + export_document(): Document
    }

    class StaticWeb {
        + add_data(new_data)
    }

    class DynamicWeb {
        - opts: Options
        - driver: str
        + add_data(new_data)
        + access_browser(browser): str
    }

    class Wikipedia {
        - name: str = "Wikipedia"
        - urlstr: str = "https:// www. wikipedia. org/"
        + __init__(name, url)
        + search_suggestions(word, language): list[str]
        + create_url(): str
        + export_document(): Document
    }

    class MercadoLibre {
        - name: str = "Mercado Libre"
        - urlstr: str = "https:// www. mercadolibre. com. co/"
        + __init__(name, url)
        + find_data(type, name): str
        + export_document(): Document
    }

    class Citizendium {
        - name: str = "Citizendium"
        - urlstr: str = "https:// www. citizendium. org/"
        + __init__(name, url)
        + create_url(): str
        + export_document(): Document
    }

    class Data {
        - title: str
        - type: str
        - data
        + __init__(title, type)
        + add_data(data)
        + get_type(): str
        + set_type(new_type, password): str
        + get_type(password): str
        + set_data()
    }

    class DataImage {
        + add_data(new_data)
    }

    class DataUrl {
        + add_data(new_data)
    }

    class DataTable {
        + add_data(new_data)
    }

    class DataText {
        + add_data(new_data)
    }

    class Document {
        - Name: str
        - Type: str
        + __init__(name, type)
        + create_document()
        + add_information(new_information)
    }

    class DocumentPdf {
        + create_document()
        + add_information(new_information)
    }

    class DocumentWord {
        + create_document()
        + add_information(new_information)
    }

    class DocumentExcel {
        + create_document()
        + add_information(new_information)
    }

    %% Herencia
    WebSites <|-- StaticWeb
    WebSites <|-- DynamicWeb
    StaticWeb <|-- Wikipedia
    StaticWeb <|-- Citizendium
    DynamicWeb <|-- MercadoLibre

    Data <|-- DataImage
    Data <|-- DataUrl
    Data <|-- DataTable
    Data <|-- DataText

    Document <|-- DocumentPdf
    Document <|-- DocumentWord
    Document <|-- DocumentExcel

    %% Relaciones de composición
    WebSites "1" o-- "*" Data
    WebSites "1" o-- "1" Document
