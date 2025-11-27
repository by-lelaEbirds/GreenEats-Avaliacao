import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyairtable import Api

app = Flask(__name__)
# Habilita CORS para permitir que o frontend (página web) acesse este backend
CORS(app)

# --- CONFIGURAÇÃO DO AIRTABLE ---
# As chaves são pegas das variáveis de ambiente do sistema (Render)
AIRTABLE_API_KEY = os.environ.get('patHgHr8ijsAmL1hH.f491a5dafc8af5b6c1f52a7d55c639e106336c3d82abf28b6cb31f6556e6560a')
AIRTABLE_BASE_ID = os.environ.get('apptcBf1P3li7IgjI/tbl22kZIZ2xEGLYRY')
TABLE_NAME = 'Produtos'

# Inicializa a conexão com a tabela
if AIRTABLE_API_KEY and AIRTABLE_BASE_ID:
    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, TABLE_NAME)
else:
    print("AVISO: Variáveis de ambiente do Airtable não configuradas.")
    table = None

# --- PARTE 2: LÓGICA DE VALIDAÇÃO (Missão 9) ---
@app.route('/validar-produto', methods=['POST'])
def validar_produto():
    data = request.json
    erros = []
    
    # Validação 1: Preço
    try:
        preco = float(data.get('preco', 0))
        if preco <= 0:
            erros.append("O preço deve ser maior que zero.")
    except (ValueError, TypeError):
        erros.append("Preço inválido.")

    # Validação 2: Título
    titulo = data.get('titulo', '')
    if not titulo or len(titulo) < 5:
        erros.append("O título deve ter pelo menos 5 caracteres.")

    # Validação 3: Categoria
    categorias_permitidas = ['Fruta', 'Legume', 'Verdura']
    categoria = data.get('categoria', '')
    if categoria not in categorias_permitidas:
        erros.append(f"Categoria inválida. Deve ser: {', '.join(categorias_permitidas)}.")

    # Retorno da validação
    if erros:
        return jsonify({"valido": False, "erros": erros}), 400
    
    return jsonify({"valido": True, "mensagem": "Produto validado com sucesso!"}), 200

# --- PARTE 3: API CRUD (Missões 7 e 8) ---

# Rota: Listar todos os produtos (READ)
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    if not table:
        return jsonify({"erro": "Erro de conexão com o banco de dados"}), 500
    
    # Busca todos os registros no Airtable
    registros = table.all()
    
    # Formata para um JSON mais limpo
    produtos_formatados = []
    for reg in registros:
        dados = reg['fields']
        dados['id'] = reg['id'] # Inclui o ID do Airtable
        produtos_formatados.append(dados)
        
    return jsonify(produtos_formatados), 200

# Rota: Criar novo produto (CREATE)
@app.route('/produtos', methods=['POST'])
def criar_produto():
    if not table:
        return jsonify({"erro": "Erro de conexão com o banco de dados"}), 500
        
    data = request.json
    
    # Aplica a mesma validação antes de salvar
    # (Verifica preço e tamanho do título para segurança)
    try:
        if float(data.get('preco', 0)) <= 0 or len(data.get('titulo', '')) < 5:
             return jsonify({"erro": "Dados inválidos. Verifique a validação."}), 400
    except:
        return jsonify({"erro": "Erro nos dados enviados."}), 400

    # Prepara o objeto para salvar
    novo_produto = {
        "titulo": data.get('titulo'),
        "preco": float(data.get('preco')),
        "categoria": data.get('categoria'),
        "descricao": data.get('descricao', 'Sem descrição')
    }
    
    # Salva no Airtable
    resposta = table.create(novo_produto)
    return jsonify(resposta), 201

# Inicialização do Servidor
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
