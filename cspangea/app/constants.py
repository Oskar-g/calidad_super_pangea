#!/usr/bin/python
APP_TITLE = "Calidad Super Pangea v4.1.201812"
APP_ICO = "http://lineadirecta.fue.es/img/avatar.png"
SOUP_PARSER = 'html.parser'
APP_VIOLATION_COLOR_CODE = {
    '1': '#FF1111',
    '2': '#FF9568',
    '3': '#FFD358',
    '4': '#D1EE69',
    '5': '#5BDE53',
}

QA_URL_TEMPLATE = 'http://desarrollo.lda/CheckingPRO/plugindata/qaking/CERTIFICACION/{}/{}.{}/report{}.html'
LOGIN_URL = 'http://desarrollo.lda/CheckingPRO/login.jsp'
LOGIN_SUBMIT_URL = 'http://desarrollo.lda/CheckingPRO/j_acegi_security_check'
HOME_URL = 'http://desarrollo.lda/CheckingPRO/dashboard/view.run?category=requests'
HOME_TITLE = 'checKing Portal'

QA_EXTENSIONS = {
    "Java": {
        "cert": "JAVA",
        "report": "java",
        "extension": "java"
    },
    "JavaScript": {
        "cert": "JAVASCRIPT",
        "report": "javascript",
        "extension": "js"
    },
    "JSP": {
        "cert": "JSP",
        "report": "jsp",
        "extension": "jsp"
    }
}
