from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask('vet')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%Jtc150509@localhost/db_clinicavetbd'
mybd = SQLAlchemy(app)

# TABELA CLIENTES -----------------------------------------------------
class Vet(mybd.Model):
    __tablename__= 'clientes'
    id_cliente = mybd.Column(mybd.Integer, primary_key=True)
    nome_cli = mybd.Column(mybd.String(100))
    endereco_cli = mybd.Column(mybd.String(100))
    telefone_cli = mybd.Column(mybd.String(100))

    def to_json(self):
        return{
            'id_cliente':self.id_cliente,
            'nome_cli': self.nome_cli,
            'endereco_cli': self.endereco_cli,
            'telefone_cli': self.telefone_cli
        }
# GET CLIENTES
@app.route('/vets', methods=['GET'])
def seleciona_vet():
    vet_selecionado = Vet.query.all()
    vet_json = [vet.to_json()
                for vet in vet_selecionado]
    return gera_resposta(200, 'Lista de Clientes', vet_json)

# POST CLIENTES
@app.route('/vets', methods=['POST'])
def criar_vet():
    requisicao = request.get_json()
    try:
        vet = Vet(
            id_cliente = requisicao['id_cliente'],
            nome_cli = requisicao['nome_cli'],
            endereco_cli = requisicao['endereco_cli'],
            telefone_cli = requisicao['telefone_cli']
        )
        mybd.session.add(vet)
        mybd.session.commit()
        return gera_resposta(201, 'Vet', vet.to_json(), 'Criado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao cadastrar!')
    
# DELETE CLIENTES
@app.route('/vets/<int:id_cliente_pam>', methods=['DELETE'])
def deleta_vet(id_cliente_pam):
    vet = Vet.query.filter_by(id_cliente = id_cliente_pam).first()
    try:
        mybd.session.delete(vet)
        mybd.session.commit()
        return gera_resposta(200, 'Vet', vet.to_json(), 'Deletado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao deletar registro!')
    
# PUT CLIENTES
@app.route('/vets/<int:id_cliente_pam>', methods=['PUT'])
def atualiza_vet(id_cliente_pam):
    vet = Vet.query.filter_by(id_cliente = id_cliente_pam).first()
    requisicao = request.get_json()
    try:
        if('nome_cli' in requisicao):
            vet.nome_cli = requisicao['nome_cli']
        if('endereco_cli' in requisicao):
            vet.endereco_cli = requisicao['endereco_cli']
        if('telefone_cli' in requisicao):
            vet.telefone_cli = requisicao['telefone_cli']
        mybd.session.add(vet)
        mybd.session.commit()
        return gera_resposta(200, 'Vet', vet.to_json(), 'Atualizado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao atualizar registro!')

# TABELA PETS -----------------------------------------------------
class Pets(mybd.Model):
    __tablename__= 'pets'
    id_pet = mybd.Column(mybd.Integer, primary_key=True)
    nome_pet = mybd.Column(mybd.String(100))
    tipo_pet = mybd.Column(mybd.String(100))
    raca_pet = mybd.Column(mybd.String(100))
    data_nascimento_pet = mybd.Column(mybd.Date())
    id_cliente = mybd.Column(mybd.Integer, mybd.ForeignKey('clientes.id_cliente'), nullable=False)

    def to_json(self):
        return{
            'id_pet':self.id_pet,
            'nome_pet': self.nome_pet,
            'tipo_pet': self.tipo_pet,
            'raca_pet': self.raca_pet,
            'data_nascimento_pet': str(self.data_nascimento_pet) if self.data_nascimento_pet else None,
            'id_cliente': self.id_cliente
        }
# GET PETS
@app.route('/pets', methods=['GET'])
def seleciona_pet():
    pets_selecionados = Pets.query.all()
    pets_json = [pet.to_json()
                for pet in pets_selecionados]
    return gera_resposta(200, 'Lista de Pets', pets_json)

# POST PETS
@app.route('/pets', methods=['POST'])
def criar_pet():
    requisicao = request.get_json()
    try:
        pet = Pets(
            id_pet = requisicao['id_pet'],
            nome_pet = requisicao['nome_pet'],
            tipo_pet = requisicao['tipo_pet'],
            raca_pet = requisicao['raca_pet'],
            data_nascimento_pet = requisicao['data_nascimento_pet'],
            id_cliente = requisicao['id_cliente']
        )
        mybd.session.add(pet)
        mybd.session.commit()
        return gera_resposta(201, 'Vet', pet.to_json(), 'Criado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao cadastrar!')
    
# DELETE PETS
@app.route('/pets/<int:id_pet_pam>', methods=['DELETE'])
def deleta_pet(id_pet_pam):
    pet = Pets.query.filter_by(id_pet = id_pet_pam).first()
    try:
        mybd.session.delete(pet)
        mybd.session.commit()
        return gera_resposta(200, 'Vet', pet.to_json(), 'Deletado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao deletar registro!')
    
# PUT PETS
@app.route('/pets/<int:id_pet_pam>', methods=['PUT'])
def atualiza_pet(id_pet_pam):
    pet = Pets.query.filter_by(id_pet = id_pet_pam).first()
    requisicao = request.get_json()
    try:
        if('nome_pet' in requisicao):
            pet.nome_pet = requisicao['nome_pet']
        if('tipo_pet' in requisicao):
            pet.tipo_pet = requisicao['tipo_pet']
        if('raca_pet' in requisicao):
            pet.raca_pet = requisicao['raca_pet']
        if('data_nascimento_pet' in requisicao):
            pet.data_nascimento_pet = requisicao['data_nascimento_pet']
        if('id_cliente' in requisicao):
            pet.id_cliente = requisicao['id_cliente']
        mybd.session.add(pet)
        mybd.session.commit()

        return gera_resposta(200, 'Vet', pet.to_json(), 'Pet atualizado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Vet', {}, 'Erro ao atualizar registro!')

# RESPOSTAS -----------------------------------------------------

def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if (mensagem):
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')
    
app.run(port=5000, host='localhost', debug=True)