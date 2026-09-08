from flask import Flask, request, jsonify
from database import get_connection

app = Flask(__name__)



@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM imoveis")
    imoveis = cursor.fetchall()
    lista_imoveis = []
    for imovel in imoveis:

        im =        {'id':imovel[0], 
                    'logradouro': imovel[1],
                    "tipo_logradouro": imovel[2],
                    "bairro" : imovel[3],
                    "cidade": imovel[4],
                    "cep": imovel[5],
                    "tipo" : imovel[6],
                    "valor": imovel[7],
                    "data_aquisicao" : imovel[8] }
        lista_imoveis.append(im)
    cursor.close()
    conexao.close()

    return jsonify(lista_imoveis), 200
    

