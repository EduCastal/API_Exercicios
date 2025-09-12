from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask('vet')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@Jtc150509/db_clinicavetbd'
mybd = SQLAlchemy(app)

class Vet(mybd.Model):
    __tablename__= 'tb_clientes'
    id_cliente = mybd.Column(mybd.Integer, primary_key=True)
    nome = mybd.Column(mybd.String(100))
    endereco = mybd.Column(mybd.String(100))
    telefone = mybd.Column(mybd.String(100))

    def to_json(self):
        return{
            'id_cliente':self.id_cliente,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefone': self.telefone
        }
# GET    
@app.route('/vets', methods=['GET'])
def seleciona_vet():
    vet_selecionado = Vet.query.all()
    vet_json = [vet.to_json()
                for vet in vet_selecionado]
    return gera_resposta(200, 'Lista de Clientes', vet_json)

# POST
@app.route('/vets', methods=['POST'])
def criar_vet():
    requisicao = request.get_json()
    try:
        vet = Vet(
            id_cliente = requisicao['id_cliente'],
            nome = requisicao['nome'],
            endereco = requisicao['endereco'],
            telefone = requisicao['telefone']
        )
        mybd.session.add(vet)
        mybd.session.commit()
        return gera_resposta(201, 'Vet', vet.to_json(), 'Criado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao cadastrar!')
    
# DELETE
@app.route('/vets/<id_cliente_pam>', methods=['DELETE'])
def deleta_vet(id_cliente_pam):
    vet = Vet.query.filter_by(id_cliente = id_cliente_pam).first()
    try:
        mybd.session.delete(vet)
        mybd.session.commit()
        return gera_resposta(200, 'Vet', vet.to_json(), 'Deletado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao deletar registro!')
    
# PUT
@app.route('/vets/<id_cliente_pam>', methods=['PUT'])
def atualiza_vet(id_cliente_pam):
    vet = Vet.query.filter_by(id_carro = id_cliente_pam).first()
    requisicao = request.get_json()
    try:
        if('nome' in requisicao):
            vet.nome = requisicao['nome']
        if('endereco' in requisicao):
            vet.endereco = requisicao['endereco']
        if('telefone' in requisicao):
            vet.telefone = requisicao['telefone']
        mybd.session.add(vet)
        mybd.session.commit()

        return gera_resposta(200, 'Vet', vet.to_json(), 'Carro atualizado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao atualizar registro!')


def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if (mensagem):
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')
    
app.run(port=5000, host='localhost', debug=True)