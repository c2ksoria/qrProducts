from curses.ascii import NUL
import os
from email.mime import base
from flask import Flask, redirect, render_template, send_from_directory
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
            bytesDecoded = code.encode('ascii')
            # print("base64_bytes",bytesDecoded)
            message_bytes = base64.urlsafe_b64decode(bytesDecoded)
            # print("message_bytes",message_bytes)
            string = message_bytes.decode('ascii')
            # print(string)
            jsonResult=json.loads(string)
            # print (jsonResult)
            valor=int(jsonResult["codigo"])
            # print(jsonResult)
            # print(valor)
            # print(type(valor))
            data= DB.search(valor)
            if (data):
                # print(data[0])
                data=data[0]
                dataDetected={"code":data[0], "name": data[1], "maker": data[2], "price": data[3], "details": [data[4], data[5], data[6]]}
                print(f'url Ingresado: {code}, código decodificado: {valor}')
            else:
                 print("Código no encontrado")
        except:
                 print("Hubo un error, la url solicitada no es válida")
                 return redirect("/notfound")
        return render_template('qr.html', DataProduct=dataDetected)

    @app.route("/notfound")
    def code_not_found():
        return render_template('notFound.html')

    @app.errorhandler(404)
    def page_not_found(e):
    #snip
        return render_template('404.html'), 404
    
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

    return app