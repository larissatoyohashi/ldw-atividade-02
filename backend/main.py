from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from flasgger import Swagger
from pydantic import BaseModel, ValidationError

app = Flask(__name__)
# Habilita o CORS para permitir que o Flet (Frontend) converse com o Flask
CORS(app) 
# Inicializa o Swagger (Acesse em: http://localhost:5000/apidocs)
swagger = Swagger(app)

# 1. Organização utilizando Blueprints
residencias_bp = Blueprint('residencias', __name__)

# Dados em memória (substitui o Banco de Dados)
db_residencias = [
    {
        "nome": "Apartamento Centro - São Paulo",
        "valor": 350000.00
    },
    {
        "nome": "Casa de Praia - Guarujá",
        "valor": 850000.00
    },
    {
        "nome": "Sítio Recanto Feliz - Atibaia",
        "valor": 650000.50
    },
    {
        "nome": "Kitnet Universitária - Campinas",
        "valor": 120000.00
    },
    {
        "nome": "Cobertura Duplex - Rio de Janeiro",
        "valor": 1250000.00
    }
]
id_counter = 1

# 2. Schema de Validação com Pydantic
class ResidenciaSchema(BaseModel):
    nome: str
    valor: float

# --- ENDPOINTS ---

# GET 1: Listar todas as residências
@residencias_bp.route('/residencias', methods=['GET'])
def listar_residencias():
    """
    Lista todas as residências cadastradas.
    ---
    responses:
      200:
        description: Retorna a lista de residências
    """
    return jsonify(db_residencias), 200

# GET 2: Endpoint extra (Informações da API)
@residencias_bp.route('/residencias/info', methods=['GET'])
def info_api():
    """
    Retorna o status e informações da API.
    ---
    responses:
      200:
        description: Informações básicas sobre a API
    """
    return jsonify({"api": "API de Residências LDW", "status": "online", "versao": "1.0"}), 200

# POST: Criar nova residência com validação
@residencias_bp.route('/residencias', methods=['POST'])
def criar_residencia():
    """
    Cadastra uma nova residência.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Mansão com Piscina - Florianópolis"
            valor:
              type: number
              example: 1500000.00
    responses:
      201:
        description: Residência criada com sucesso
      400:
        description: Erro de validação dos dados
    """
    global id_counter
    try:
        # Validação do Pydantic
        dados_validados = ResidenciaSchema(**request.json)
        
        nova_residencia = {
            "id": id_counter,
            "nome": dados_validados.nome,
            "valor": dados_validados.valor
        }
        db_residencias.append(nova_residencia)
        id_counter += 1
        
        return jsonify(nova_residencia), 201
        
    except ValidationError as e:
        # Retorna erro 400 se faltar nome ou o valor não for número
        return jsonify(e.errors()), 400

# Registra o Blueprint no app principal
app.register_blueprint(residencias_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)