import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyairtable import Api

app = Flask(__name__)
CORS(app)

# --- CONFIGURAÇÃO DO AIRTABLE ---
# ATENÇÃO: Aqui usamos os NOMES das variáveis definidas no Render
# Não cole a chave direta aqui, deixe 'AIRTABLE_KEY'
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
TABLE_NAME = 'Produtos'

# Inicializa conexão
table = None
if AIRTABLE_API_KEY and AIRTABLE_BASE_ID:
    try:
        api = Api(AIRTABLE_API_KEY)
        table = api.table(AIRTABLE_BASE_ID, TABLE_NAME)
        print("LOG: Conexão com Airtable iniciada com sucesso.")
    except Exception as e:
        print(f"LOG: Erro ao iniciar Airtable: {e}")
else:
    # Se entrar aqui, é porque o Render não passou as variáveis
    print("ERRO CRÍTICO: As chaves do Airtable não foram encontradas no Render.")
    print(f"DEBUG: Chave recebida: {AIRTABLE_API_KEY} | ID recebido: {AIRTABLE_BASE_ID}")

# --- ROTA RAIZ ---
@app.route('/', methods=['GET'])
def home():
    status = "Conectado 🟢" if table else "Desconectado 🔴 (Erro de Config)"
    return jsonify({
        "sistema": "GreenEats API",
        "status_banco": status
    })

# --- ROTA: Validar (Parte 2) ---
@app.route('/validar-produto', methods=['POST'])
def validar_produto():
    data = request.json
    erros = []
    
    try:
        if float(data.get('preco', 0)) <= 0: erros.append("O preço deve ser maior que zero.")
    except: erros.append("Preço inválido.")

    if len(data.get('titulo', '')) < 5: erros.append("O título deve ter 5+ letras.")
    
    cats = ['Fruta', 'Legume', 'Verdura']
    if data.get('categoria') not in cats: erros.append("Categoria inválida.")

    if erros: return jsonify({"valido": False, "erros": erros}), 400
    return jsonify({"valido": True, "mensagem": "Ok"}), 200

# --- ROTA: Listar (Parte 3) ---
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    if not table: return jsonify({"erro": "Banco desconectado"}), 500
    try:
        registros = table.all()
        # Formata os dados para o frontend
        dados_limpos = [{"id": r['id'], **r['fields']} for r in registros]
        return jsonify(dados_limpos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# --- ROTA: Criar (Parte 3) ---
@app.route('/produtos', methods=['POST'])
def criar_produto():
    if not table: return jsonify({"erro": "Banco desconectado"}), 500
    data = request.json
    try:
        novo = {
            "titulo": data.get('titulo'),
            "preco": float(data.get('preco')),
            "categoria": data.get('categoria'),
            "descricao": data.get('descricao', '')
        }
        table.create(novo)
        return jsonify({"msg": "Criado"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
