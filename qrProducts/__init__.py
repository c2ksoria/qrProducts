from curses.ascii import NUL
import os
from email.mime import base
from flask import Flask, redirect, render_template
from example.data import dataProduct
import db
import json
import base64
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='holasss'
    )

    DB = db.DATABASES()
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello

    @app.route("/<code>")
    def qrRead(code):
        dataDetected={}
        try:
            print(code)
            bytesDecoded= base64.b64decode(code)
            print(bytesDecoded)
            print(type(bytesDecoded))
            string=bytesDecoded.decode("utf-8")
            print(type(string))
            # string='{"codigo":"00000026"}'
            print(string)
            jsonResult=json.loads(string)
            valor=int(jsonResult["codigo"])
            print(jsonResult)
            print(valor)
            print(type(valor))
            data= DB.search(valor)

            if (data):
                print(data[0])

                data=data[0]
                dataDetected={"code":valor, "name": data[1], "maker": data[2], "price": data[3], "details": [data[4], data[5], data[6]]}
                print(dataDetected)
            else:
                print("Código no encontrado")
        
        except:
            print("hubo un error en la decodificación")
            return redirect('/notfound')
        return render_template('qr.html', DataProduct=dataDetected)

    @app.route("/notfound")
    def code_not_found():
        return render_template('notFound.html')

    @app.errorhandler(404)
    def page_not_found(e):
    #snip
        return render_template('404.html'), 404
    return app