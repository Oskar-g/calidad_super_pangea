#!/usr/bin/python 
from cspangea.app import request_session
from cspangea.app.calidad import Calidad
from cspangea.app.calidad_ui import Ui

if __name__ == '__main__':
    session = request_session.get_cookie()

    if request_session.validate_access(session):
        print("Iniciando interfaz...")
        app = Ui(Calidad(session))

    else:
        raise Exception("No se pudo inicializar la sesión.\nComprueba tu conexión o las credenciales")
