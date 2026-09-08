from flask import Flask, request, jsonify
from database import get_connection

app = Flask(__name__)

def dic_imovel(imoveis_id):
    imovel = {'id':imoveis_id[0], 
                    'logradouro': imoveis_id[1],
                    "tipo_logradouro": imoveis_id[2],
                    "bairro" : imoveis_id[3],
                    "cidade": imoveis_id[4],
                    "cep": imoveis_id[5],
                    "tipo" : imoveis_id[6],
                    "valor": imoveis_id[7],
                    "data_aquisicao" : imoveis_id[8] }
    
    return imovel


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
    
@app.route("/imoveis/<int:imoveis_id>", methods=["GET"])
def listar_imovel(imoveis_id):
    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = ?",(imoveis_id,))
    imovel = cursor.fetchone()
    if imovel is None:
        cursor.close()
        conexao.close()

        return jsonify({
            "erro": "Imóvel não encontrado"
        }), 404
    lista_imovel = dic_imovel(imovel)
    conexao.close()
    cursor.close()
    return jsonify(lista_imovel), 200
    
