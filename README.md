# Programación Orientada a Objetos - UNAL
## Proyecto Final
Este grupo de nombre **Bizarre Coding Adventure** conformado por las personas **Juan Sebastian Peñuela Duran**,
**Nicolas Steven Galvis Ordoñez** y **Andres Arturo Lozano Olivares** realizará la alternativa 2 **(Sistema de Web Scraping)**

### Definición de alternativa
Un sistema de web scraping es una herramienta que permite extraer datos de sitios web de forma automática (Algo así como un copiar y pegar mucho más eficiente). Estos datos se estructuran y se presentan en formatos como: JSON, CSV, Excel, etc.
Este sistema es utilizado en actividades como el monitoreo de precios (acciones, aplicaciones, juegos, indumentaria, etc), monitoreo de páginas en internet de interés propio o colectivo, estudios poblacionales y estadísticos, entre otros. En resumen, la función de un sistema de web scraping es **recopilar datos**, con los cuales es común construir información para satisfacer la necesidad y el interés del usuario. En este caso, se busca extraer datos de páginas web estáticas, como lo son las **wikis**, y de paginas web de sitios de retail, como **Mercado libre** o **Airbnb**.

Además, como **Feature Extra**, se generaran reportes en forma de documentos de la información recopilada de estos sitios, para darle mas profesionalismo a nuestro programa.

**Consideraciones legales del web scraping**
El web scraping no es ilegal por sí mismo. Sin embargo, se deben tener en cuenta los permisos que la página web que se intenta manipular otorgue, los cuales están determinados en los **términos y condiciones**. Es necesario tener cuidado con lo que se intenta scrapear, la ley 1581 de 2012, también conocida como la **Ley de protección de datos personales**, establece parámetros que se deben cumplir al momento de manipular datos privados de cualquier individuo, los cuales abarcan el consentimiento, la finalidad, y la garantía de su seguridad.

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
        - urlstr: str = "https://www.wikipedia.org/"
        + __init__(name, url)
        + search_suggestions(word, language): list[str]
        + create_url(): str
        + export_document(): Document
    }

    class MercadoLibre {
        - name: str = "Mercado Libre"
        - urlstr: str = "https://www.mercadolibre.com.co/"
        + __init__(name, url)
        + find_data(type, name): str
        + export_document(): Document
    }

    class Citizendium {
        - name: str = "Citizendium"
        - urlstr: str = "https://www.citizendium.org/"
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
```
## Solución Preliminar
Haremos un codigo, el cual sea capaz de recopilar informacion util de disntintas paginas web, ya sean wikis o paginas de compra, y retornar toda esta información, de manera organizada, en un documento, apto para la lectura y analisis de la misma.

