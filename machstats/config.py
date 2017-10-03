import os
import pymysql

tornado_settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates')}

pymysql_settings = {
    'host': 'ip',
    'user': 'username',
    'password': 'password',
    'db': 'database',
    'cursorclass': pymysql.cursors.DictCursor}
