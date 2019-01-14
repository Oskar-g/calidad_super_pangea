#!/usr/bin/python

# Herramienta para apertura de items de calidad

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests.sessions import Session

from cspangea.app.constants import QA_EXTENSIONS, QA_URL_TEMPLATE, SOUP_PARSER


class Calidad:
    def __init__(self, session: Session):
        self._session = session
        self._qa_url = None
        self._web_dom = None

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @property
    def qa_url(self):
        return self._qa_url

    @qa_url.setter
    def qa_url(self, qa_url):
        self._qa_url = qa_url

    @property
    def web_dom(self):
        return self._web_dom

    @web_dom.setter
    def web_dom(self, web_dom):
        self._web_dom = web_dom

    def get_data(self, file: str, extension: str) -> dict:
        """
        Obtener datos de calidad de un archivo con una extensión

        :param file: Nombre del archivo que verificar la calidad
        :param extension: Extensión del archivo [Java, JavaScript, JSP]
        :return: datos de la calidad
        """
        self.build_url(file, extension)
        self.__web_parse()

        return {
            "file_found": self.__is_file_found(),
            "file_path": self.__get_file_path(),
            "qa_infractions": self.__get_infractions()
        }

    def build_url(self, file: str, extension: str):
        """
        Constructor de la url de calidad, reemplaza los valores por los indicados en el dict

        :param file: nombre del archivo a buscar
        :param extension: datos de la extensión del archivo [JAVA, JavaScript, JSP]
        :return: String de la url formateado
        """
        extension_data = QA_EXTENSIONS[extension]
        self._qa_url = QA_URL_TEMPLATE.format(
            extension_data['cert'],
            file,
            extension_data['extension'],
            extension_data['report'])

    def __web_parse(self):
        """
        Obtener el dom de la web de calidad
        """
        print("Abriendo direccion: " + self._qa_url)
        page = self._session.get(self._qa_url)
        if None is page:
            raise Exception("web no encontrada:", page)
        self.web_dom = BeautifulSoup(page.content, SOUP_PARSER)

    def __is_file_found(self):
        """
        Verificar que el archivo buscado tiene ficha de calidad
        :return: TRUE / FALSE
        """
        return True if self.web_dom.select("#divStayTopLeft") \
                       and self.web_dom.select("#divStayTopLeft")[0] else False

    def __get_file_path(self):
        """
        Obtener path del fichero de la ficha de calidad
        :return: None / Path del fichero
        """
        filename = None
        try:
            name = self.web_dom.select(".enlaceTitulo")[0].get_text()
            filename = str(name).replace("Aplicaciones.Fuentes.", "")
        except Exception as e:
            print("Error al capturar nombre de fichero", e)
        finally:
            return filename

    def __get_infractions(self) -> list:
        """
        Recuperar la lista de infracciones (si existe)
        :return:  lista de infracciones de calidad
        """
        qa_web = self.web_dom.select("#anacla_layer tbody tr")
        infractions = []
        if len(qa_web):
            for qa in qa_web:
                infractions.append(self.__get_infraction(qa))

        return infractions

    @staticmethod
    def __get_infraction(tag: Tag = None) -> dict:
        """
        Recuperar datos de la infracción
        :param tag: tr del contenido de la infracción.
        :return: datos de la infracción contenida en la tag <tr>
        """
        infraction = None
        if tag:
            tds = tag.select("td")
            infraction = {
                "c_regla": tds[0].get_text(),
                "descripcion": tds[1].get_text(),
                "c_fuente": tds[2].get_text(),
                "n_linea": tds[3].get_text(),
                "prioridad": tds[4].get_text(),
            }

        return infraction
