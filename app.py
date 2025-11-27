from flask import Flask, request, jsonify
from flask_cors import CORS
from pyairtable import Api
import os

app = Flask(__name__)
CORS(app) # Permite que o frontend converse com o backend

# Configuração do Airtable via Variáveis de Ambiente (Configuraremos no Render)
API_KEY = os.environ.get('AIRTABLE_KEY')
BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
TABLE_NAME = 'Produtos'

# Conexão
api = Api(API_KEY)
table = api.table(BASE_ID, TABLE_NAME)

# --- PARTE 2: Lógica de Validação ---
@app.route('/validar-produto', methods=['POST'])
def validar_produto():
    data = request.json
    erros = []

    # 1. Preço menor ou igual a zero
    try:
        preco = float(data.get('preco', 0))
        if preco <= 0:
            erros.append("O preço deve ser maior que zero.")
    except ValueError:
        erros.append("Preço inválido.")

    # 2. Título com menos de 5 caracteres
    titulo = data.get('titulo', '')
    if len(titulo) < 5:
        erros.append("O título deve ter pelo menos 5 caracteres.")

    # 3. Categoria não permitida
    categorias_permitidas = ['Fruta', 'Legume', 'Verdura']
    categoria = data.get('categoria', '')
    if categoria not in categorias_permitidas:
        erros.append(f"Categoria inválida. Permitidas: {categorias_permitidas}")

    if erros:
        return jsonify({"valido": False, "erros": erros}), 400
    
    return jsonify({"valido": True, "mensagem": "Produto validado com sucesso!"}), 200

# --- PARTE 3: Arquitetura API e CRUD ---

# Modelo de Dados (Conceitual):
# {
#   "id": "recXXXXX" (Gerado pelo Airtable),
#   "titulo": "String",
#   "preco": Float,
#   "categoria": "String",
#   "descricao": "String"
# }

# LISTAR (GET)
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = table.all()
    # Limpando o retorno do Airtable para ficar mais simples
    lista_limpa = [{"id": p['id'], **p['fields']} for p in produtos]
    return jsonify(lista_limpa)

# CRIAR (POST) - Com validação embutida
@app.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.json
    
    # Reutilizando a lógica de validação
    # (Em um sistema real, faríamos uma função separada, mas aqui chamamos a rota logicamente)
    if float(data.get('preco', 0)) <= 0 or len(data.get('titulo', '')) < 5:
         return jsonify({"erro": "Dados inválidos (preço ou título)"}), 400

    novo_produto = {
        "titulo": data.get('titulo'),
        "preco": float(data.get('preco')),
        "categoria": data.get('categoria'),
        "descricao": data.get('descricao', '')
    }
    
    resposta = table.create(novo_produto)
    return jsonify(resposta), 201

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
