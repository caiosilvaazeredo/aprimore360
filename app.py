from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os
import json

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Inicializa Firebase Admin
def initialize_firebase():
    try:
        # Cria credenciais do Firebase a partir das variáveis de ambiente
        cred_dict = {
            "type": "service_account",
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
        }
        
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("✓ Firebase inicializado com sucesso!")
    except Exception as e:
        print(f"✗ Erro ao inicializar Firebase: {e}")
        raise

# Inicializa Firebase
initialize_firebase()
db = firestore.client()

# Rotas principais
@app.route('/')
def index():
    return render_template('index.html')

# ============ API - CLIENTES ============
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    try:
        clientes_ref = db.collection('clientes')
        clientes = []
        
        for doc in clientes_ref.stream():
            cliente = doc.to_dict()
            cliente['id'] = doc.id
            clientes.append(cliente)
        
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/<cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    try:
        doc = db.collection('clientes').document(cliente_id).get()
        
        if doc.exists:
            cliente = doc.to_dict()
            cliente['id'] = doc.id
            return jsonify(cliente), 200
        else:
            return jsonify({'error': 'Cliente não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
def create_cliente():
    try:
        data = request.json
        
        # Validação básica
        required_fields = ['razaoSocial', 'fantasia', 'cnpj', 'telefone', 'cidade', 'bairro']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Adiciona timestamp
        from datetime import datetime
        data['criadoEm'] = datetime.now()
        data['atualizadoEm'] = datetime.now()
        
        # Adiciona no Firestore
        doc_ref = db.collection('clientes').add(data)
        cliente_id = doc_ref[1].id
        
        return jsonify({'id': cliente_id, 'message': 'Cliente criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/<cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    try:
        data = request.json
        
        # Atualiza timestamp
        from datetime import datetime
        data['atualizadoEm'] = datetime.now()
        
        # Atualiza no Firestore
        db.collection('clientes').document(cliente_id).update(data)
        
        return jsonify({'message': 'Cliente atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/<cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    try:
        db.collection('clientes').document(cliente_id).delete()
        return jsonify({'message': 'Cliente deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - COMPROMISSOS ============
@app.route('/api/compromissos', methods=['GET'])
def get_compromissos():
    try:
        compromissos_ref = db.collection('compromissos').order_by('data').order_by('hora')
        compromissos = []
        
        for doc in compromissos_ref.stream():
            compromisso = doc.to_dict()
            compromisso['id'] = doc.id
            compromissos.append(compromisso)
        
        return jsonify(compromissos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compromissos', methods=['POST'])
def create_compromisso():
    try:
        data = request.json
        
        # Validação básica
        required_fields = ['data', 'hora', 'cliente', 'tipo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Adiciona timestamp
        from datetime import datetime
        data['criadoEm'] = datetime.now()
        
        # Adiciona no Firestore
        doc_ref = db.collection('compromissos').add(data)
        compromisso_id = doc_ref[1].id
        
        return jsonify({'id': compromisso_id, 'message': 'Compromisso criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compromissos/<compromisso_id>', methods=['PUT'])
def update_compromisso(compromisso_id):
    try:
        data = request.json
        
        # Atualiza timestamp
        from datetime import datetime
        data['atualizadoEm'] = datetime.now()
        
        # Atualiza no Firestore
        db.collection('compromissos').document(compromisso_id).update(data)
        
        return jsonify({'message': 'Compromisso atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compromissos/<compromisso_id>', methods=['DELETE'])
def delete_compromisso(compromisso_id):
    try:
        db.collection('compromissos').document(compromisso_id).delete()
        return jsonify({'message': 'Compromisso deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - ESTATÍSTICAS ============
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        # Conta clientes
        clientes_count = len(list(db.collection('clientes').stream()))
        
        # Conta compromissos
        compromissos_count = len(list(db.collection('compromissos').stream()))
        
        # Calcula outros stats
        clientes_ativos = len([c for c in db.collection('clientes').where('status', '==', 'atual').stream()])
        clientes_ausentes = len([c for c in db.collection('clientes').where('status', '==', 'ausente').stream()])
        
        return jsonify({
            'totalClientes': clientes_count,
            'totalCompromissos': compromissos_count,
            'clientesAtivos': clientes_ativos,
            'clientesAusentes': clientes_ausentes
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
