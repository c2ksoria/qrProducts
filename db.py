import os
from os.path import dirname, abspath, join
from dotenv import load_dotenv
import pymysql
import os
from pathlib import Path

APP_DIR = abspath(dirname(__file__))
dotenv_path = join(APP_DIR, '.env')
load_dotenv(dotenv_path)

class DATABASES:
    def __init__(self):
        self.__DB_TABLE= os.environ.get('DB_TABLE')
        self.__localhost = os.environ.get('DB_HOST')
        self.__port = int(os.environ.get('DB_PORT'))
        self.__username      = os.environ.get('DB_USERNAME')
        self.__password      = os.environ.get('DB_PASSWORD')
        self.__database_name = os.environ.get('DB_DATABASE')
        self.createConnection()
    def createConnection(self):
        db = pymysql.connect(
		  host     = self.__localhost,
          port = self.__port,
		  user     = self.__username,
		  passwd   = self.__password,
		  database = self.__database_name
		)
        self.__db = db
        self.cursor = db.cursor()
    def __close(self):
        self.__db.close()
        self.cursor.close()
    def search(self, id):
        print('Search data..')
        cursor = self.__db.cursor()
        # print(id)
        try:
            query="SELECT a.codigo,a.nombre,m.nombre as nmarca,p.prec1,ades.detalle,ades1.detalle,ades2.detalle from articulos a left join precios p on a.codigo=p.codigo left join marcas m on a.marca=m.marca left join articulosdes ades on a.codigo=ades.codigo and ades.iddescr=1 left join articulosdes ades1 on a.codigo=ades1.codigo and ades1.iddescr=2 left join articulosdes ades2 on a.codigo=ades2.codigo and ades2.iddescr=3 WHERE a.codigo=(%s) "
            cursor.execute(query, id)
            data=cursor.fetchall()
        except os.error:
            print("hubo un error al intentar almacenar valores",os.error )
        return data