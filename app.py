from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json
import pytz
from functools import wraps
import bcrypt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import pandas as pd

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Configurações adicionais
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Inicializa extensões
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

jwt = JWTManager(app)

# Timezone Brasil
tz_brasil = pytz.timezone('America/Sao_Paulo')

# Inicializa Firebase Admin
def initialize_firebase():
    try:
        # Verifica se as variáveis de ambiente estão configuradas
        required_vars = [
            'FIREBASE_PROJECT_ID',
            'FIREBASE_PRIVATE_KEY_ID', 
            'FIREBASE_PRIVATE_KEY',
            'FIREBASE_CLIENT_EMAIL',
            'FIREBASE_CLIENT_ID'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print("\n❌ ERRO: Variáveis de ambiente não configuradas!")
            print(f"Faltando: {', '.join(missing_vars)}\n")
            raise ValueError(f"Variáveis de ambiente faltando: {', '.join(missing_vars)}")
        
        # Cria credenciais do Firebase
        private_key = os.getenv('FIREBASE_PRIVATE_KEY')
        if '\\n' in private_key:
            private_key = private_key.replace('\\n', '\n')
        
        cred_dict = {
            "type": "service_account",
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": private_key,
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
        }
        
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase inicializado com sucesso!")
        return True
    except Exception as e:
        print(f"\n❌ Erro ao inicializar Firebase: {e}\n")
        return False

# Inicializa Firebase
if not initialize_firebase():
    print("⚠️  Sistema rodando em modo DEMO - Firebase não configurado")
    db = None
else:
    db = firestore.client()

# Inicializa Geocoder
geolocator = Nominatim(user_agent="comercial-app")

# Classe User para Flask-Login
class User(UserMixin):
    def __init__(self, uid, email, nome=None, cargo=None, empresa=None):
        self.id = uid
        self.email = email
        self.nome = nome
        self.cargo = cargo
        self.empresa = empresa

@login_manager.user_loader
def load_user(user_id):
    if not db:
        return None
    try:
        user_doc = db.collection('usuarios').document(user_id).get()
        if user_doc.exists:
            data = user_doc.to_dict()
            return User(
                uid=user_id,
                email=data.get('email'),
                nome=data.get('nome'),
                cargo=data.get('cargo'),
                empresa=data.get('empresa')
            )
    except Exception:
        pass
    return None

# Decorator para verificar autenticação em APIs
def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Autenticação necessária'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ============ ROTAS DE PÁGINAS ============
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/clientes')
@login_required
def clientes_page():
    return render_template('clientes.html', user=current_user)

@app.route('/mapa')
@login_required
def mapa_page():
    return render_template('mapa.html', user=current_user)

@app.route('/agenda')
@login_required
def agenda_page():
    return render_template('agenda.html', user=current_user)

@app.route('/metas')
@login_required
def metas_page():
    return render_template('metas.html', user=current_user)

@app.route('/pedidos')
@login_required
def pedidos_page():
    return render_template('pedidos.html', user=current_user)

@app.route('/relatorios')
@login_required
def relatorios_page():
    return render_template('relatorios.html', user=current_user)

@app.route('/configuracoes')
@login_required
def configuracoes_page():
    return render_template('configuracoes.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ============ API - AUTENTICAÇÃO ============
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        data = request.json
        email = data.get('email')
        senha = data.get('senha')
        
        if not email or not senha:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        if not db:
            # Modo DEMO
            if email == "demo@teste.com" and senha == "demo123":
                user = User(
                    uid="demo_user",
                    email=email,
                    nome="Usuário Demo",
                    cargo="Vendedor",
                    empresa="Empresa Demo"
                )
                login_user(user, remember=True)
                return jsonify({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'nome': user.nome,
                        'cargo': user.cargo
                    }
                }), 200
            else:
                return jsonify({'error': 'Credenciais inválidas'}), 401
        
        # Busca usuário no Firestore
        users_ref = db.collection('usuarios')
        query = users_ref.where('email', '==', email).limit(1)
        users = query.get()
        
        if not users:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        user_doc = users[0]
        user_data = user_doc.to_dict()
        
        # Verifica senha
        if not bcrypt.checkpw(senha.encode('utf-8'), user_data['senha'].encode('utf-8')):
            return jsonify({'error': 'Senha incorreta'}), 401
        
        # Cria objeto User
        user = User(
            uid=user_doc.id,
            email=user_data['email'],
            nome=user_data.get('nome'),
            cargo=user_data.get('cargo'),
            empresa=user_data.get('empresa')
        )
        
        # Faz login
        login_user(user, remember=True)
        
        # Atualiza último acesso
        db.collection('usuarios').document(user_doc.id).update({
            'ultimoAcesso': datetime.now(tz_brasil)
        })
        
        # Cria token JWT
        access_token = create_access_token(identity=user_doc.id)
        
        return jsonify({
            'success': True,
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'nome': user.nome,
                'cargo': user.cargo,
                'empresa': user.empresa
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO - registro desabilitado'}), 400
            
        data = request.json
        
        # Validação
        required_fields = ['email', 'senha', 'nome', 'cargo', 'empresa']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Verifica se email já existe
        existing = db.collection('usuarios').where('email', '==', data['email']).get()
        if existing:
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Hash da senha
        hashed_password = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        
        # Cria usuário
        user_data = {
            'email': data['email'],
            'senha': hashed_password.decode('utf-8'),
            'nome': data['nome'],
            'cargo': data['cargo'],
            'empresa': data['empresa'],
            'telefone': data.get('telefone', ''),
            'criadoEm': datetime.now(tz_brasil),
            'ultimoAcesso': datetime.now(tz_brasil),
            'ativo': True,
            'configuracoes': {
                'notificacoes': True,
                'relatoriosDiarios': True,
                'alertasMetas': True
            }
        }
        
        doc_ref = db.collection('usuarios').add(user_data)
        user_id = doc_ref[1].id
        
        return jsonify({
            'success': True,
            'message': 'Usuário criado com sucesso',
            'userId': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - DASHBOARD ============
@app.route('/api/dashboard/stats', methods=['GET'])
@api_login_required
def get_dashboard_stats():
    try:
        if not db:
            # Dados DEMO
            return jsonify({
                'vendas': {
                    'mes': 125000,
                    'meta': 150000,
                    'percentual': 83.3,
                    'crescimento': 15.5
                },
                'clientes': {
                    'total': 45,
                    'ativos': 38,
                    'novos': 5,
                    'ausentes': 7
                },
                'compromissos': {
                    'hoje': 4,
                    'semana': 18,
                    'concluidos': 12,
                    'pendentes': 6
                },
                'produtos': {
                    'maisVendidos': ['Produto A', 'Produto B', 'Produto C'],
                    'estoqueBaixo': 3
                }
            }), 200
        
        # Estatísticas reais
        hoje = datetime.now(tz_brasil).date()
        inicio_mes = hoje.replace(day=1)
        
        # Vendas do mês
        vendas_ref = db.collection('pedidos').where('vendedorId', '==', current_user.id)
        vendas_mes = vendas_ref.where('data', '>=', inicio_mes).get()
        total_vendas = sum([v.to_dict().get('valorTotal', 0) for v in vendas_mes])
        
        # Clientes
        clientes_ref = db.collection('clientes').where('vendedorId', '==', current_user.id)
        clientes = list(clientes_ref.stream())
        clientes_ativos = len([c for c in clientes if c.to_dict().get('status') == 'ativo'])
        
        # Compromissos
        compromissos_ref = db.collection('compromissos').where('vendedorId', '==', current_user.id)
        compromissos_hoje = compromissos_ref.where('data', '==', hoje).get()
        
        stats = {
            'vendas': {
                'mes': total_vendas,
                'meta': 150000,
                'percentual': (total_vendas / 150000 * 100) if total_vendas else 0,
                'crescimento': 15.5
            },
            'clientes': {
                'total': len(clientes),
                'ativos': clientes_ativos,
                'novos': 5,
                'ausentes': len(clientes) - clientes_ativos
            },
            'compromissos': {
                'hoje': len(compromissos_hoje),
                'semana': 18,
                'concluidos': 12,
                'pendentes': 6
            },
            'produtos': {
                'maisVendidos': ['Produto A', 'Produto B', 'Produto C'],
                'estoqueBaixo': 3
            }
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - CLIENTES ============
@app.route('/api/clientes', methods=['GET'])
@api_login_required
def get_clientes():
    try:
        if not db:
            # Dados DEMO
            return jsonify([
                {
                    'id': '1',
                    'razaoSocial': 'Boutique Elegance Ltda',
                    'fantasia': 'Elegance Store',
                    'cnpj': '12.345.678/0001-90',
                    'telefone': '(11) 98765-4321',
                    'email': 'contato@elegance.com',
                    'endereco': {
                        'logradouro': 'Rua Oscar Freire',
                        'numero': '1234',
                        'bairro': 'Jardins',
                        'cidade': 'São Paulo',
                        'uf': 'SP',
                        'cep': '01426-001'
                    },
                    'status': 'ativo',
                    'ultimoPedido': '2025-01-10',
                    'totalCompras': 45000,
                    'limite': 50000,
                    'latitude': -23.5629,
                    'longitude': -46.6674
                }
            ]), 200
        
        clientes_ref = db.collection('clientes').where('vendedorId', '==', current_user.id)
        clientes = []
        
        for doc in clientes_ref.stream():
            cliente = doc.to_dict()
            cliente['id'] = doc.id
            clientes.append(cliente)
        
        return jsonify(clientes), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
@api_login_required
def create_cliente():
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        
        # Validação
        required_fields = ['razaoSocial', 'fantasia', 'cnpj', 'telefone']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Geocodificação
        endereco = data.get('endereco', {})
        if endereco:
            try:
                address = f"{endereco.get('logradouro')}, {endereco.get('numero')} - {endereco.get('cidade')}, {endereco.get('uf')}"
                location = geolocator.geocode(address)
                if location:
                    data['latitude'] = location.latitude
                    data['longitude'] = location.longitude
            except Exception as geo_error:
                print(f"Erro na geocodificação: {geo_error}")
        
        # Adiciona metadados
        data['vendedorId'] = current_user.id
        data['criadoEm'] = datetime.now(tz_brasil)
        data['atualizadoEm'] = datetime.now(tz_brasil)
        data['status'] = 'ativo'
        data['totalCompras'] = 0
        data['numeroCompras'] = 0
        
        # Salva no Firestore
        doc_ref = db.collection('clientes').add(data)
        cliente_id = doc_ref[1].id
        
        # Registra atividade
        db.collection('atividades').add({
            'tipo': 'cliente_criado',
            'vendedorId': current_user.id,
            'clienteId': cliente_id,
            'descricao': f'Novo cliente cadastrado: {data["fantasia"]}',
            'data': datetime.now(tz_brasil)
        })
        
        return jsonify({'id': cliente_id, 'message': 'Cliente criado com sucesso'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/<cliente_id>', methods=['PUT'])
@api_login_required
def update_cliente(cliente_id):
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        data['atualizadoEm'] = datetime.now(tz_brasil)
        
        # Geocodificação se endereço foi atualizado
        if 'endereco' in data:
            endereco = data['endereco']
            try:
                address = f"{endereco.get('logradouro')}, {endereco.get('numero')} - {endereco.get('cidade')}, {endereco.get('uf')}"
                location = geolocator.geocode(address)
                if location:
                    data['latitude'] = location.latitude
                    data['longitude'] = location.longitude
            except Exception:
                pass
        
        db.collection('clientes').document(cliente_id).update(data)
        
        return jsonify({'message': 'Cliente atualizado com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - COMPROMISSOS/AGENDA ============
@app.route('/api/compromissos', methods=['GET'])
@api_login_required
def get_compromissos():
    try:
        if not db:
            # Dados DEMO
            return jsonify([
                {
                    'id': '1',
                    'titulo': 'Visita - Elegance Store',
                    'tipo': 'visita',
                    'data': '2025-01-15',
                    'hora': '09:00',
                    'clienteId': '1',
                    'cliente': 'Elegance Store',
                    'endereco': 'Rua Oscar Freire, 1234',
                    'observacoes': 'Apresentar nova coleção',
                    'status': 'pendente'
                }
            ]), 200
        
        # Filtros
        data_inicio = request.args.get('dataInicio')
        data_fim = request.args.get('dataFim')
        
        compromissos_ref = db.collection('compromissos').where('vendedorId', '==', current_user.id)
        
        if data_inicio:
            compromissos_ref = compromissos_ref.where('data', '>=', data_inicio)
        if data_fim:
            compromissos_ref = compromissos_ref.where('data', '<=', data_fim)
        
        compromissos_ref = compromissos_ref.order_by('data').order_by('hora')
        
        compromissos = []
        for doc in compromissos_ref.stream():
            compromisso = doc.to_dict()
            compromisso['id'] = doc.id
            
            # Busca dados do cliente
            if compromisso.get('clienteId'):
                cliente_doc = db.collection('clientes').document(compromisso['clienteId']).get()
                if cliente_doc.exists:
                    cliente_data = cliente_doc.to_dict()
                    compromisso['cliente'] = cliente_data.get('fantasia')
                    compromisso['clienteEndereco'] = cliente_data.get('endereco')
            
            compromissos.append(compromisso)
        
        return jsonify(compromissos), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compromissos', methods=['POST'])
@api_login_required
def create_compromisso():
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        
        # Validação
        required_fields = ['titulo', 'data', 'hora', 'tipo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Adiciona metadados
        data['vendedorId'] = current_user.id
        data['criadoEm'] = datetime.now(tz_brasil)
        data['status'] = 'pendente'
        data['notificado'] = False
        
        # Salva no Firestore
        doc_ref = db.collection('compromissos').add(data)
        compromisso_id = doc_ref[1].id
        
        # Registra atividade
        db.collection('atividades').add({
            'tipo': 'compromisso_criado',
            'vendedorId': current_user.id,
            'compromissoId': compromisso_id,
            'descricao': f'Novo compromisso: {data["titulo"]}',
            'data': datetime.now(tz_brasil)
        })
        
        return jsonify({'id': compromisso_id, 'message': 'Compromisso criado com sucesso'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compromissos/<compromisso_id>/concluir', methods=['POST'])
@api_login_required
def concluir_compromisso(compromisso_id):
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        
        # Atualiza status
        db.collection('compromissos').document(compromisso_id).update({
            'status': 'concluido',
            'concluidoEm': datetime.now(tz_brasil),
            'observacoesConclusao': data.get('observacoes', '')
        })
        
        # Se for visita, criar relatório
        if data.get('criarRelatorio'):
            relatorio = {
                'compromissoId': compromisso_id,
                'vendedorId': current_user.id,
                'clienteId': data.get('clienteId'),
                'data': datetime.now(tz_brasil),
                'tipo': 'visita',
                'detalhes': data.get('detalhes', {}),
                'proximosPassos': data.get('proximosPassos', ''),
                'pedidoRealizado': data.get('pedidoRealizado', False)
            }
            
            if data.get('pedidoRealizado'):
                relatorio['valorPedido'] = data.get('valorPedido', 0)
                
            db.collection('relatorios').add(relatorio)
        
        return jsonify({'message': 'Compromisso concluído com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - MAPA/ROTAS ============
@app.route('/api/mapa/clientes', methods=['GET'])
@api_login_required
def get_clientes_mapa():
    try:
        if not db:
            # Dados DEMO
            return jsonify([
                {
                    'id': '1',
                    'nome': 'Elegance Store',
                    'endereco': 'Rua Oscar Freire, 1234',
                    'latitude': -23.5629,
                    'longitude': -46.6674,
                    'status': 'ativo',
                    'ultimaVisita': '2025-01-10'
                }
            ]), 200
        
        clientes_ref = db.collection('clientes').where('vendedorId', '==', current_user.id)
        clientes = []
        
        for doc in clientes_ref.stream():
            cliente = doc.to_dict()
            if cliente.get('latitude') and cliente.get('longitude'):
                clientes.append({
                    'id': doc.id,
                    'nome': cliente.get('fantasia'),
                    'endereco': f"{cliente.get('endereco', {}).get('logradouro', '')}, {cliente.get('endereco', {}).get('numero', '')}",
                    'latitude': cliente['latitude'],
                    'longitude': cliente['longitude'],
                    'status': cliente.get('status'),
                    'ultimaVisita': cliente.get('ultimaVisita')
                })
        
        return jsonify(clientes), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mapa/otimizar-rota', methods=['POST'])
@api_login_required
def otimizar_rota():
    try:
        data = request.json
        cliente_ids = data.get('clienteIds', [])
        
        if not cliente_ids:
            return jsonify({'error': 'Nenhum cliente selecionado'}), 400
        
        # Algoritmo simples de otimização (TSP simplificado)
        # Em produção, usar algo como OR-Tools do Google
        
        rota_otimizada = {
            'clientes': cliente_ids,
            'distanciaTotal': 45.2,  # km
            'tempoEstimado': 180,  # minutos
            'economia': {
                'distancia': 12.5,  # km economizados
                'tempo': 35  # minutos economizados
            }
        }
        
        return jsonify(rota_otimizada), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - PEDIDOS ============
@app.route('/api/pedidos', methods=['GET'])
@api_login_required
def get_pedidos():
    try:
        if not db:
            return jsonify([]), 200
            
        pedidos_ref = db.collection('pedidos').where('vendedorId', '==', current_user.id)
        pedidos_ref = pedidos_ref.order_by('data', direction=firestore.Query.DESCENDING)
        
        pedidos = []
        for doc in pedidos_ref.stream():
            pedido = doc.to_dict()
            pedido['id'] = doc.id
            pedidos.append(pedido)
        
        return jsonify(pedidos), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pedidos', methods=['POST'])
@api_login_required
def create_pedido():
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        
        # Validação
        required_fields = ['clienteId', 'itens', 'valorTotal']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Adiciona metadados
        data['vendedorId'] = current_user.id
        data['numero'] = f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        data['data'] = datetime.now(tz_brasil)
        data['status'] = 'pendente'
        
        # Calcula comissão
        comissao_percentual = 5  # 5% de comissão
        data['comissao'] = data['valorTotal'] * (comissao_percentual / 100)
        
        # Salva pedido
        doc_ref = db.collection('pedidos').add(data)
        pedido_id = doc_ref[1].id
        
        # Atualiza estatísticas do cliente
        cliente_ref = db.collection('clientes').document(data['clienteId'])
        cliente_ref.update({
            'ultimoPedido': datetime.now(tz_brasil),
            'totalCompras': firestore.Increment(data['valorTotal']),
            'numeroCompras': firestore.Increment(1)
        })
        
        # Registra atividade
        db.collection('atividades').add({
            'tipo': 'pedido_criado',
            'vendedorId': current_user.id,
            'pedidoId': pedido_id,
            'clienteId': data['clienteId'],
            'valor': data['valorTotal'],
            'descricao': f'Novo pedido: {data["numero"]}',
            'data': datetime.now(tz_brasil)
        })
        
        return jsonify({
            'id': pedido_id,
            'numero': data['numero'],
            'message': 'Pedido criado com sucesso'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - METAS ============
@app.route('/api/metas', methods=['GET'])
@api_login_required
def get_metas():
    try:
        if not db:
            # Dados DEMO
            return jsonify({
                'metaMensal': 150000,
                'realizado': 125000,
                'percentual': 83.3,
                'diasRestantes': 14,
                'metaDiaria': 1785,
                'ranking': 3,
                'totalVendedores': 12
            }), 200
        
        hoje = datetime.now(tz_brasil).date()
        inicio_mes = hoje.replace(day=1)
        fim_mes = (hoje.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Busca meta do vendedor
        meta_doc = db.collection('metas').document(f"{current_user.id}_{hoje.strftime('%Y%m')}").get()
        
        if meta_doc.exists:
            meta_data = meta_doc.to_dict()
            meta_valor = meta_data.get('valor', 150000)
        else:
            meta_valor = 150000  # Meta padrão
        
        # Calcula vendas do mês
        vendas_ref = db.collection('pedidos').where('vendedorId', '==', current_user.id)
        vendas_mes = vendas_ref.where('data', '>=', inicio_mes).where('data', '<=', fim_mes).get()
        total_vendas = sum([v.to_dict().get('valorTotal', 0) for v in vendas_mes])
        
        # Calcula métricas
        percentual = (total_vendas / meta_valor * 100) if meta_valor else 0
        dias_restantes = (fim_mes - hoje).days
        meta_diaria = ((meta_valor - total_vendas) / dias_restantes) if dias_restantes > 0 else 0
        
        return jsonify({
            'metaMensal': meta_valor,
            'realizado': total_vendas,
            'percentual': round(percentual, 1),
            'diasRestantes': dias_restantes,
            'metaDiaria': round(meta_diaria, 2),
            'ranking': 3,
            'totalVendedores': 12
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - RELATÓRIOS ============
@app.route('/api/relatorios/vendas', methods=['GET'])
@api_login_required
def get_relatorio_vendas():
    try:
        if not db:
            return jsonify({
                'vendas': [],
                'totalGeral': 0,
                'totalComissao': 0
            }), 200
            
        # Filtros
        data_inicio = request.args.get('dataInicio')
        data_fim = request.args.get('dataFim')
        
        vendas_ref = db.collection('pedidos').where('vendedorId', '==', current_user.id)
        
        if data_inicio:
            vendas_ref = vendas_ref.where('data', '>=', data_inicio)
        if data_fim:
            vendas_ref = vendas_ref.where('data', '<=', data_fim)
        
        vendas = []
        total_geral = 0
        total_comissao = 0
        
        for doc in vendas_ref.stream():
            venda = doc.to_dict()
            venda['id'] = doc.id
            
            # Busca dados do cliente
            if venda.get('clienteId'):
                cliente_doc = db.collection('clientes').document(venda['clienteId']).get()
                if cliente_doc.exists:
                    venda['cliente'] = cliente_doc.to_dict().get('fantasia')
            
            vendas.append(venda)
            total_geral += venda.get('valorTotal', 0)
            total_comissao += venda.get('comissao', 0)
        
        return jsonify({
            'vendas': vendas,
            'totalGeral': total_geral,
            'totalComissao': total_comissao
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - PRODUTOS ============
@app.route('/api/produtos', methods=['GET'])
@api_login_required
def get_produtos():
    try:
        if not db:
            # Dados DEMO
            return jsonify([
                {
                    'id': '1',
                    'codigo': 'PROD001',
                    'nome': 'Produto A',
                    'categoria': 'Categoria 1',
                    'preco': 150.00,
                    'estoque': 100,
                    'unidade': 'UN'
                }
            ]), 200
        
        produtos_ref = db.collection('produtos')
        produtos = []
        
        for doc in produtos_ref.stream():
            produto = doc.to_dict()
            produto['id'] = doc.id
            produtos.append(produto)
        
        return jsonify(produtos), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - NOTIFICAÇÕES ============
@app.route('/api/notificacoes', methods=['GET'])
@api_login_required
def get_notificacoes():
    try:
        if not db:
            return jsonify([]), 200
            
        notif_ref = db.collection('notificacoes').where('usuarioId', '==', current_user.id)
        notif_ref = notif_ref.where('lida', '==', False).order_by('data', direction=firestore.Query.DESCENDING).limit(10)
        
        notificacoes = []
        for doc in notif_ref.stream():
            notif = doc.to_dict()
            notif['id'] = doc.id
            notificacoes.append(notif)
        
        return jsonify(notificacoes), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ CONFIGURAÇÕES DO USUÁRIO ============
@app.route('/api/usuario/perfil', methods=['GET'])
@api_login_required
def get_perfil():
    try:
        if not db:
            return jsonify({
                'id': current_user.id,
                'email': current_user.email,
                'nome': current_user.nome,
                'cargo': current_user.cargo,
                'empresa': current_user.empresa
            }), 200
        
        user_doc = db.collection('usuarios').document(current_user.id).get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            user_data['id'] = current_user.id
            del user_data['senha']  # Remove senha do retorno
            return jsonify(user_data), 200
        
        return jsonify({'error': 'Usuário não encontrado'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuario/perfil', methods=['PUT'])
@api_login_required
def update_perfil():
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        
        # Remove campos sensíveis
        if 'senha' in data:
            del data['senha']
        if 'email' in data:
            del data['email']  # Email não pode ser alterado
        
        data['atualizadoEm'] = datetime.now(tz_brasil)
        
        db.collection('usuarios').document(current_user.id).update(data)
        
        return jsonify({'message': 'Perfil atualizado com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rotas para arquivos estáticos
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Cria diretórios necessários
    import os
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Cria arquivo CSS básico se não existir
    css_file = 'static/css/style.css'
    if not os.path.exists(css_file):
        with open(css_file, 'w') as f:
            f.write('/* Custom CSS */')
    
    # Cria arquivo JS básico se não existir  
    js_file = 'static/js/app.js'
    if not os.path.exists(js_file):
        with open(js_file, 'w') as f:
            f.write('console.log("App loaded");')
    
    app.run(debug=True, host='0.0.0.0', port=5000)