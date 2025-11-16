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
            print(f"   Faltando: {', '.join(missing_vars)}")
            return False
        
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
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL').replace('@', '%40')}"
        }
        
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("\n✅ Firebase inicializado com sucesso!")
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

# Configurações do Firebase para o frontend
app.config['FIREBASE_API_KEY'] = os.getenv('FIREBASE_API_KEY', '')
app.config['FIREBASE_AUTH_DOMAIN'] = os.getenv('FIREBASE_AUTH_DOMAIN', '')
app.config['FIREBASE_PROJECT_ID'] = os.getenv('FIREBASE_PROJECT_ID', '')
app.config['FIREBASE_STORAGE_BUCKET'] = os.getenv('FIREBASE_STORAGE_BUCKET', '')
app.config['FIREBASE_MESSAGING_SENDER_ID'] = os.getenv('FIREBASE_MESSAGING_SENDER_ID', '')
app.config['FIREBASE_APP_ID'] = os.getenv('FIREBASE_APP_ID', '')

# Inicializa Geocoder
geolocator = Nominatim(user_agent="comercial-app")

# Classe User para Flask-Login
class User(UserMixin):
    def __init__(self, uid, email, nome=None, cargo=None, empresa_id=None, empresas=None):
        self.id = uid
        self.email = email
        self.nome = nome
        self.cargo = cargo
        self.empresa_id = empresa_id  # Empresa atual selecionada
        self.empresas = empresas or []  # Lista de empresas que o usuário pode acessar

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
                empresa_id=data.get('empresaAtual'),
                empresas=data.get('empresas', [])
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
    return render_template('landing.html')

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('cadastro.html')

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

# ============ API - AUTENTICAÇÃO ============
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        if not db:
            # Modo DEMO - login automático
            demo_user = User(
                uid='demo_user',
                email='demo@exemplo.com',
                nome='Usuário Demo',
                cargo='Vendedor',
                empresa_id='demo_empresa',
                empresas=[{'id': 'demo_empresa', 'nome': 'Empresa Demo'}]
            )
            login_user(demo_user)
            return jsonify({
                'success': True,
                'message': 'Login realizado (MODO DEMO)',
                'user': {
                    'id': demo_user.id,
                    'email': demo_user.email,
                    'nome': demo_user.nome,
                    'cargo': demo_user.cargo,
                    'empresaAtual': demo_user.empresa_id
                }
            }), 200
            
        data = request.json
        email = data.get('email')
        senha = data.get('senha')
        
        if not email or not senha:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Busca usuário
        users = db.collection('usuarios').where('email', '==', email).limit(1).get()
        
        if not users:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        user_doc = users[0]
        user_data = user_doc.to_dict()
        
        # Verifica senha
        if not bcrypt.checkpw(senha.encode('utf-8'), user_data['senha'].encode('utf-8')):
            return jsonify({'error': 'Senha incorreta'}), 401
        
        # Atualiza último acesso
        db.collection('usuarios').document(user_doc.id).update({
            'ultimoAcesso': datetime.now(tz_brasil)
        })
        
        # Cria sessão
        user = User(
            uid=user_doc.id,
            email=user_data.get('email'),
            nome=user_data.get('nome'),
            cargo=user_data.get('cargo'),
            empresa_id=user_data.get('empresaAtual'),
            empresas=user_data.get('empresas', [])
        )
        login_user(user)
        
        return jsonify({
            'success': True,
            'message': 'Login realizado com sucesso',
            'user': {
                'id': user.id,
                'email': user.email,
                'nome': user.nome,
                'cargo': user.cargo,
                'empresaAtual': user.empresa_id
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
        required_fields = ['email', 'senha', 'nome', 'cargo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Verifica se email já existe
        existing = list(db.collection('usuarios').where('email', '==', data['email']).get())
        if existing:
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Hash da senha
        hashed_password = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        
        # Cria ou vincula empresa
        empresa_id = None
        empresas = []
        
        if data.get('criarEmpresa') and data.get('nomeEmpresa'):
            # Cria nova empresa
            empresa_data = {
                'nome': data['nomeEmpresa'],
                'cnpj': data.get('cnpjEmpresa', ''),
                'criadoEm': datetime.now(tz_brasil),
                'ativo': True,
                'configuracoes': {
                    'comissaoPadrao': 5,
                    'metaMensal': 100000
                }
            }
            empresa_ref = db.collection('empresas').add(empresa_data)
            empresa_id = empresa_ref[1].id
            empresas = [{'id': empresa_id, 'nome': data['nomeEmpresa'], 'role': 'admin'}]
        elif data.get('codigoEmpresa'):
            # Vincula a empresa existente por código
            empresa_doc = db.collection('empresas').where('codigoConvite', '==', data['codigoEmpresa']).limit(1).get()
            if empresa_doc:
                empresa = empresa_doc[0]
                empresa_id = empresa.id
                empresas = [{'id': empresa_id, 'nome': empresa.to_dict().get('nome'), 'role': 'vendedor'}]
            else:
                return jsonify({'error': 'Código de empresa inválido'}), 400
        
        # Cria usuário
        user_data = {
            'email': data['email'],
            'senha': hashed_password.decode('utf-8'),
            'nome': data['nome'],
            'cargo': data['cargo'],
            'telefone': data.get('telefone', ''),
            'empresaAtual': empresa_id,
            'empresas': empresas,
            'criadoEm': datetime.now(tz_brasil),
            'ultimoAcesso': datetime.now(tz_brasil),
            'ativo': True,
            'configuracoes': {
                'notificacoes': True,
                'relatoriosDiarios': True,
                'alertasMetas': True,
                'privacidadeRanking': True  # Por padrão, dados são privados
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

@app.route('/api/auth/logout', methods=['POST'])
@api_login_required
def api_logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Logout realizado'}), 200

# ============ API - AUTENTICAÇÃO FIREBASE ============
@app.route('/api/auth/firebase-login', methods=['POST'])
def firebase_login():
    """Login usando token do Firebase Authentication"""
    try:
        data = request.json
        id_token = data.get('idToken')
        
        if not id_token:
            return jsonify({'error': 'Token não fornecido'}), 400
        
        if not db:
            # Modo DEMO
            demo_user = User(
                uid='demo_user',
                email='demo@exemplo.com',
                nome='Usuário Demo',
                cargo='Vendedor',
                empresa_id='demo_empresa',
                empresas=[{'id': 'demo_empresa', 'nome': 'Empresa Demo'}]
            )
            login_user(demo_user)
            return jsonify({
                'success': True,
                'message': 'Login realizado (MODO DEMO)',
                'user': {
                    'id': demo_user.id,
                    'email': demo_user.email,
                    'nome': demo_user.nome
                }
            }), 200
        
        # Verifica o token no Firebase
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            firebase_uid = decoded_token['uid']
            email = decoded_token.get('email', '')
            display_name = data.get('displayName') or decoded_token.get('name', '')
            photo_url = data.get('photoURL') or decoded_token.get('picture', '')
            is_new_user = data.get('isNewUser', False)
        except Exception as e:
            return jsonify({'error': f'Token inválido: {str(e)}'}), 401
        
        # Busca ou cria usuário no Firestore
        user_doc = db.collection('usuarios').document(firebase_uid).get()
        
        if not user_doc.exists:
            # Usuário novo - cria perfil no Firestore
            user_data = {
                'email': email,
                'nome': display_name or email.split('@')[0],
                'cargo': 'Vendedor',
                'telefone': '',
                'fotoURL': photo_url,
                'empresaAtual': None,
                'empresas': [],
                'criadoEm': datetime.now(tz_brasil),
                'ultimoAcesso': datetime.now(tz_brasil),
                'ativo': True,
                'authProvider': 'google' if 'google' in decoded_token.get('firebase', {}).get('sign_in_provider', '') else 'email',
                'configuracoes': {
                    'notificacoes': True,
                    'relatoriosDiarios': True,
                    'alertasMetas': True,
                    'privacidadeRanking': True
                }
            }
            db.collection('usuarios').document(firebase_uid).set(user_data)
            
            # Se for novo usuário, redireciona para completar cadastro
            user = User(
                uid=firebase_uid,
                email=email,
                nome=user_data['nome'],
                cargo=user_data['cargo'],
                empresa_id=None,
                empresas=[]
            )
            login_user(user)
            
            return jsonify({
                'success': True,
                'message': 'Usuário criado com sucesso',
                'user': {
                    'id': firebase_uid,
                    'email': email,
                    'nome': user_data['nome'],
                    'cargo': user_data['cargo'],
                    'empresaAtual': None
                },
                'isNewUser': True,
                'needsSetup': True
            }), 200
        else:
            # Usuário existente - atualiza último acesso
            user_data = user_doc.to_dict()
            
            db.collection('usuarios').document(firebase_uid).update({
                'ultimoAcesso': datetime.now(tz_brasil)
            })
            
            user = User(
                uid=firebase_uid,
                email=user_data.get('email', email),
                nome=user_data.get('nome'),
                cargo=user_data.get('cargo'),
                empresa_id=user_data.get('empresaAtual'),
                empresas=user_data.get('empresas', [])
            )
            login_user(user)
            
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso',
                'user': {
                    'id': firebase_uid,
                    'email': user_data.get('email'),
                    'nome': user_data.get('nome'),
                    'cargo': user_data.get('cargo'),
                    'empresaAtual': user_data.get('empresaAtual')
                },
                'isNewUser': False
            }), 200
        
    except Exception as e:
        print(f"Erro no firebase_login: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/firebase-register', methods=['POST'])
def firebase_register():
    """Registra novo usuário usando Firebase Authentication"""
    try:
        data = request.json
        id_token = data.get('idToken')
        
        if not id_token:
            return jsonify({'error': 'Token não fornecido'}), 400
        
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
        
        # Verifica o token
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            firebase_uid = decoded_token['uid']
            email = decoded_token.get('email', '')
        except Exception as e:
            return jsonify({'error': f'Token inválido: {str(e)}'}), 401
        
        # Verifica se já existe
        existing = db.collection('usuarios').document(firebase_uid).get()
        if existing.exists:
            return jsonify({'error': 'Usuário já existe'}), 400
        
        # Cria ou vincula empresa
        empresa_id = None
        empresas = []
        
        if data.get('criarEmpresa') and data.get('nomeEmpresa'):
            empresa_data = {
                'nome': data['nomeEmpresa'],
                'cnpj': data.get('cnpjEmpresa', ''),
                'criadoEm': datetime.now(tz_brasil),
                'ativo': True,
                'configuracoes': {
                    'comissaoPadrao': 5,
                    'metaMensal': 100000
                }
            }
            empresa_ref = db.collection('empresas').add(empresa_data)
            empresa_id = empresa_ref[1].id
            empresas = [{'id': empresa_id, 'nome': data['nomeEmpresa'], 'role': 'admin'}]
        elif data.get('codigoEmpresa'):
            empresa_docs = list(db.collection('empresas').where('codigoConvite', '==', data['codigoEmpresa']).limit(1).stream())
            if empresa_docs:
                empresa = empresa_docs[0]
                empresa_id = empresa.id
                empresas = [{'id': empresa_id, 'nome': empresa.to_dict().get('nome'), 'role': 'vendedor'}]
            else:
                return jsonify({'error': 'Código de empresa inválido'}), 400
        
        # Cria perfil do usuário
        user_data = {
            'email': email,
            'nome': data.get('nome', email.split('@')[0]),
            'cargo': data.get('cargo', 'Vendedor'),
            'telefone': data.get('telefone', ''),
            'empresaAtual': empresa_id,
            'empresas': empresas,
            'criadoEm': datetime.now(tz_brasil),
            'ultimoAcesso': datetime.now(tz_brasil),
            'ativo': True,
            'authProvider': 'email',
            'configuracoes': {
                'notificacoes': True,
                'relatoriosDiarios': True,
                'alertasMetas': True,
                'privacidadeRanking': True
            }
        }
        
        db.collection('usuarios').document(firebase_uid).set(user_data)
        
        return jsonify({
            'success': True,
            'message': 'Usuário criado com sucesso',
            'userId': firebase_uid
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/complete-profile', methods=['POST'])
@api_login_required
def complete_profile():
    """Completa o perfil do usuário após login com Google"""
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
        
        data = request.json
        
        empresa_id = None
        empresas = []
        
        if data.get('criarEmpresa') and data.get('nomeEmpresa'):
            empresa_data = {
                'nome': data['nomeEmpresa'],
                'cnpj': data.get('cnpjEmpresa', ''),
                'criadoEm': datetime.now(tz_brasil),
                'ativo': True,
                'configuracoes': {
                    'comissaoPadrao': 5,
                    'metaMensal': 100000
                }
            }
            empresa_ref = db.collection('empresas').add(empresa_data)
            empresa_id = empresa_ref[1].id
            empresas = [{'id': empresa_id, 'nome': data['nomeEmpresa'], 'role': 'admin'}]
        elif data.get('codigoEmpresa'):
            empresa_docs = list(db.collection('empresas').where('codigoConvite', '==', data['codigoEmpresa']).limit(1).stream())
            if empresa_docs:
                empresa = empresa_docs[0]
                empresa_id = empresa.id
                empresas = [{'id': empresa_id, 'nome': empresa.to_dict().get('nome'), 'role': 'vendedor'}]
            else:
                return jsonify({'error': 'Código de empresa inválido'}), 400
        
        update_data = {
            'nome': data.get('nome', current_user.nome),
            'cargo': data.get('cargo', 'Vendedor'),
            'telefone': data.get('telefone', ''),
            'empresaAtual': empresa_id,
            'empresas': empresas,
            'atualizadoEm': datetime.now(tz_brasil)
        }
        
        db.collection('usuarios').document(current_user.id).update(update_data)
        
        return jsonify({
            'success': True,
            'message': 'Perfil completado com sucesso'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/alterar-senha', methods=['POST'])
@api_login_required
def alterar_senha():
    """Altera a senha do usuário (para usuários com auth email/password)"""
    try:
        # Esta função é apenas para feedback - a alteração real é feita no Firebase Auth pelo frontend
        return jsonify({'success': True, 'message': 'Senha alterada com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - EMPRESAS ============
@app.route('/api/empresas', methods=['GET'])
@api_login_required
def get_empresas():
    """Lista empresas do usuário"""
    try:
        if not db:
            return jsonify([{'id': 'demo', 'nome': 'Empresa Demo'}]), 200
        
        return jsonify(current_user.empresas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas/trocar', methods=['POST'])
@api_login_required
def trocar_empresa():
    """Troca a empresa ativa do usuário"""
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
        
        data = request.json
        empresa_id = data.get('empresaId')
        
        # Verifica se usuário tem acesso à empresa
        if not any(e['id'] == empresa_id for e in current_user.empresas):
            return jsonify({'error': 'Acesso negado a esta empresa'}), 403
        
        # Atualiza empresa ativa
        db.collection('usuarios').document(current_user.id).update({
            'empresaAtual': empresa_id
        })
        
        return jsonify({'success': True, 'message': 'Empresa alterada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas/convite', methods=['POST'])
@api_login_required
def gerar_convite():
    """Gera código de convite para empresa"""
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
        
        import secrets
        codigo = secrets.token_urlsafe(8)
        
        db.collection('empresas').document(current_user.empresa_id).update({
            'codigoConvite': codigo,
            'codigoExpira': datetime.now(tz_brasil) + timedelta(days=7)
        })
        
        return jsonify({'codigo': codigo}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - COMPROMISSOS/AGENDA (CORRIGIDO) ============
@app.route('/api/compromissos', methods=['GET'])
@api_login_required
def get_compromissos():
    try:
        if not db:
            return jsonify([
                {
                    'id': '1',
                    'titulo': 'Visita - Elegance Store',
                    'tipo': 'visita',
                    'data': '2025-01-15',
                    'horaInicio': '09:00',
                    'horaFim': '10:00',
                    'clienteId': '1',
                    'cliente': 'Elegance Store',
                    'endereco': 'Rua Oscar Freire, 1234',
                    'observacoes': 'Apresentar nova coleção',
                    'status': 'pendente'
                }
            ]), 200
        
        data_inicio = request.args.get('dataInicio')
        data_fim = request.args.get('dataFim')
        
        compromissos_ref = db.collection('compromissos').where('vendedorId', '==', current_user.id)
        
        if data_inicio:
            compromissos_ref = compromissos_ref.where('data', '>=', data_inicio)
        if data_fim:
            compromissos_ref = compromissos_ref.where('data', '<=', data_fim)
        
        compromissos_ref = compromissos_ref.order_by('data').order_by('horaInicio')
        
        compromissos = []
        for doc in compromissos_ref.stream():
            compromisso = doc.to_dict()
            compromisso['id'] = doc.id
            
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
        
        # CORREÇÃO: Aceita tanto 'hora' quanto 'horaInicio'
        if 'horaInicio' in data and 'hora' not in data:
            data['hora'] = data['horaInicio']
        
        # Validação flexível
        required_fields = ['titulo', 'data', 'tipo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Verifica se tem hora (pode ser 'hora' ou 'horaInicio')
        if 'hora' not in data and 'horaInicio' not in data:
            return jsonify({'error': 'Campo obrigatório: hora ou horaInicio'}), 400
        
        # Normaliza para usar horaInicio internamente
        if 'hora' in data and 'horaInicio' not in data:
            data['horaInicio'] = data['hora']
        
        # Adiciona metadados
        data['vendedorId'] = current_user.id
        data['empresaId'] = current_user.empresa_id
        data['criadoEm'] = datetime.now(tz_brasil)
        if 'status' not in data:
            data['status'] = 'pendente'
        data['notificado'] = False
        
        # Salva no Firestore
        doc_ref = db.collection('compromissos').add(data)
        compromisso_id = doc_ref[1].id
        
        # Registra atividade
        db.collection('atividades').add({
            'tipo': 'compromisso_criado',
            'vendedorId': current_user.id,
            'empresaId': current_user.empresa_id,
            'compromissoId': compromisso_id,
            'descricao': f'Novo compromisso: {data["titulo"]}',
            'data': datetime.now(tz_brasil)
        })
        
        return jsonify({'id': compromisso_id, 'message': 'Compromisso criado com sucesso'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compromissos/<compromisso_id>', methods=['PUT'])
@api_login_required
def update_compromisso(compromisso_id):
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        
        # Normaliza campos de hora
        if 'horaInicio' in data and 'hora' not in data:
            data['hora'] = data['horaInicio']
        if 'hora' in data and 'horaInicio' not in data:
            data['horaInicio'] = data['hora']
        
        data['atualizadoEm'] = datetime.now(tz_brasil)
        
        db.collection('compromissos').document(compromisso_id).update(data)
        
        return jsonify({'message': 'Compromisso atualizado com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compromissos/<compromisso_id>', methods=['DELETE'])
@api_login_required
def delete_compromisso(compromisso_id):
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        db.collection('compromissos').document(compromisso_id).delete()
        
        return jsonify({'message': 'Compromisso excluído com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - PEDIDOS (CORRIGIDO) ============
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
            
            # Busca nome do cliente
            if pedido.get('clienteId'):
                cliente_doc = db.collection('clientes').document(pedido['clienteId']).get()
                if cliente_doc.exists:
                    pedido['clienteNome'] = cliente_doc.to_dict().get('fantasia', 'Cliente')
            
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
        
        # Validação flexível
        if 'clienteId' not in data:
            return jsonify({'error': 'Campo obrigatório: clienteId'}), 400
        
        # Calcula valor total se não fornecido
        if 'valorTotal' not in data and 'itens' in data:
            data['valorTotal'] = sum(item.get('subtotal', item.get('quantidade', 1) * item.get('preco', 0)) for item in data['itens'])
        
        if 'valorTotal' not in data:
            return jsonify({'error': 'Campo obrigatório: valorTotal ou itens com preço'}), 400
        
        # Adiciona metadados
        data['vendedorId'] = current_user.id
        data['empresaId'] = current_user.empresa_id
        data['numero'] = f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        data['data'] = datetime.now(tz_brasil)
        data['status'] = data.get('status', 'pendente')
        
        # Busca configuração de comissão da empresa
        comissao_percentual = 5  # Padrão
        if current_user.empresa_id:
            empresa_doc = db.collection('empresas').document(current_user.empresa_id).get()
            if empresa_doc.exists:
                config = empresa_doc.to_dict().get('configuracoes', {})
                comissao_percentual = config.get('comissaoPadrao', 5)
        
        data['comissaoPercentual'] = comissao_percentual
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
            'empresaId': current_user.empresa_id,
            'pedidoId': pedido_id,
            'clienteId': data['clienteId'],
            'valor': data['valorTotal'],
            'descricao': f'Novo pedido: {data["numero"]}',
            'data': datetime.now(tz_brasil)
        })
        
        return jsonify({
            'id': pedido_id,
            'numero': data['numero'],
            'comissao': data['comissao'],
            'message': 'Pedido criado com sucesso'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pedidos/<pedido_id>', methods=['PUT'])
@api_login_required
def update_pedido(pedido_id):
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        data['atualizadoEm'] = datetime.now(tz_brasil)
        
        # Recalcula comissão se valor alterado
        if 'valorTotal' in data:
            pedido_doc = db.collection('pedidos').document(pedido_id).get()
            if pedido_doc.exists:
                percentual = pedido_doc.to_dict().get('comissaoPercentual', 5)
                data['comissao'] = data['valorTotal'] * (percentual / 100)
        
        db.collection('pedidos').document(pedido_id).update(data)
        
        return jsonify({'message': 'Pedido atualizado com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - CLIENTES ============
@app.route('/api/clientes', methods=['GET'])
@api_login_required
def get_clientes():
    try:
        if not db:
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
                    'latitude': -23.5629,
                    'longitude': -46.6674,
                    'status': 'ativo',
                    'ultimoPedido': '2025-01-10',
                    'totalCompras': 45000
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
        
        # Geocodificação
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
        
        data['vendedorId'] = current_user.id
        data['empresaId'] = current_user.empresa_id
        data['criadoEm'] = datetime.now(tz_brasil)
        data['status'] = 'ativo'
        data['totalCompras'] = 0
        data['numeroCompras'] = 0
        
        doc_ref = db.collection('clientes').add(data)
        cliente_id = doc_ref[1].id
        
        db.collection('atividades').add({
            'tipo': 'cliente_criado',
            'vendedorId': current_user.id,
            'empresaId': current_user.empresa_id,
            'clienteId': cliente_id,
            'descricao': f'Novo cliente: {data.get("fantasia", data.get("razaoSocial"))}',
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

@app.route('/api/clientes/<cliente_id>', methods=['DELETE'])
@api_login_required
def delete_cliente(cliente_id):
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        db.collection('clientes').document(cliente_id).delete()
        
        return jsonify({'message': 'Cliente excluído com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - METAS (MELHORADO) ============
@app.route('/api/metas', methods=['GET'])
@api_login_required
def get_metas():
    try:
        if not db:
            return jsonify({
                'pessoais': [
                    {
                        'id': '1',
                        'tipo': 'vendas',
                        'valor': 150000,
                        'realizado': 125000,
                        'percentual': 83.3,
                        'periodo': 'mensal',
                        'mes': datetime.now().month,
                        'ano': datetime.now().year
                    }
                ],
                'empresa': {
                    'metaMensal': 500000,
                    'realizado': 420000,
                    'percentual': 84
                }
            }), 200
        
        # Metas pessoais do usuário
        metas_ref = db.collection('metas').where('vendedorId', '==', current_user.id)
        metas_pessoais = []
        
        for doc in metas_ref.stream():
            meta = doc.to_dict()
            meta['id'] = doc.id
            
            # Calcula realizado
            if meta.get('tipo') == 'vendas':
                inicio_mes = datetime.now(tz_brasil).replace(day=1)
                pedidos = db.collection('pedidos').where('vendedorId', '==', current_user.id).where('data', '>=', inicio_mes).get()
                meta['realizado'] = sum([p.to_dict().get('valorTotal', 0) for p in pedidos])
                meta['percentual'] = (meta['realizado'] / meta['valor'] * 100) if meta['valor'] else 0
            
            metas_pessoais.append(meta)
        
        # Meta da empresa (sem expor dados individuais de outros vendedores)
        empresa_meta = None
        if current_user.empresa_id:
            empresa_doc = db.collection('empresas').document(current_user.empresa_id).get()
            if empresa_doc.exists:
                config = empresa_doc.to_dict().get('configuracoes', {})
                meta_empresa = config.get('metaMensal', 0)
                
                # Calcula total da empresa
                inicio_mes = datetime.now(tz_brasil).replace(day=1)
                pedidos_empresa = db.collection('pedidos').where('empresaId', '==', current_user.empresa_id).where('data', '>=', inicio_mes).get()
                total_empresa = sum([p.to_dict().get('valorTotal', 0) for p in pedidos_empresa])
                
                empresa_meta = {
                    'metaMensal': meta_empresa,
                    'realizado': total_empresa,
                    'percentual': (total_empresa / meta_empresa * 100) if meta_empresa else 0
                }
        
        return jsonify({
            'pessoais': metas_pessoais,
            'empresa': empresa_meta
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metas', methods=['POST'])
@api_login_required
def create_meta():
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
            
        data = request.json
        
        data['vendedorId'] = current_user.id
        data['empresaId'] = current_user.empresa_id
        data['criadoEm'] = datetime.now(tz_brasil)
        
        doc_ref = db.collection('metas').add(data)
        
        return jsonify({'id': doc_ref[1].id, 'message': 'Meta criada com sucesso'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metas/ranking', methods=['GET'])
@api_login_required
def get_ranking():
    """Ranking da empresa - APENAS vendedores que optaram por aparecer"""
    try:
        if not db:
            return jsonify([]), 200
        
        if not current_user.empresa_id:
            return jsonify({'error': 'Usuário não vinculado a empresa'}), 400
        
        # Busca vendedores da empresa que permitiram aparecer no ranking
        usuarios_ref = db.collection('usuarios').where('empresaAtual', '==', current_user.empresa_id)
        
        ranking = []
        inicio_mes = datetime.now(tz_brasil).replace(day=1)
        
        for user_doc in usuarios_ref.stream():
            user_data = user_doc.to_dict()
            
            # Verifica se usuário permite aparecer no ranking
            config = user_data.get('configuracoes', {})
            if not config.get('privacidadeRanking', True):  # Se False, aparece no ranking
                # Calcula vendas do mês
                pedidos = db.collection('pedidos').where('vendedorId', '==', user_doc.id).where('data', '>=', inicio_mes).get()
                total = sum([p.to_dict().get('valorTotal', 0) for p in pedidos])
                
                ranking.append({
                    'nome': user_data.get('nome'),
                    'cargo': user_data.get('cargo'),
                    'vendas': total,
                    'isCurrentUser': user_doc.id == current_user.id
                })
        
        # Ordena por vendas
        ranking.sort(key=lambda x: x['vendas'], reverse=True)
        
        # Adiciona posição
        for i, item in enumerate(ranking):
            item['posicao'] = i + 1
        
        return jsonify(ranking), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - RELATÓRIOS (COMPLETO) ============
@app.route('/api/relatorios/vendas', methods=['GET'])
@api_login_required
def relatorio_vendas():
    try:
        if not db:
            return jsonify({
                'resumo': {
                    'totalVendas': 125000,
                    'quantidadePedidos': 45,
                    'ticketMedio': 2777.78,
                    'comissaoTotal': 6250
                },
                'porPeriodo': [
                    {'data': '2025-01-01', 'valor': 15000},
                    {'data': '2025-01-02', 'valor': 18000}
                ]
            }), 200
        
        # Parâmetros
        data_inicio = request.args.get('dataInicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        data_fim = request.args.get('dataFim', datetime.now().strftime('%Y-%m-%d'))
        
        # Busca pedidos
        pedidos_ref = db.collection('pedidos').where('vendedorId', '==', current_user.id)
        pedidos = list(pedidos_ref.stream())
        
        # Calcula métricas
        total_vendas = 0
        comissao_total = 0
        vendas_por_dia = {}
        
        for doc in pedidos:
            pedido = doc.to_dict()
            valor = pedido.get('valorTotal', 0)
            total_vendas += valor
            comissao_total += pedido.get('comissao', 0)
            
            data = pedido.get('data')
            if hasattr(data, 'strftime'):
                data_str = data.strftime('%Y-%m-%d')
            else:
                data_str = str(data)[:10]
            
            if data_str not in vendas_por_dia:
                vendas_por_dia[data_str] = 0
            vendas_por_dia[data_str] += valor
        
        qtd_pedidos = len(pedidos)
        ticket_medio = total_vendas / qtd_pedidos if qtd_pedidos > 0 else 0
        
        return jsonify({
            'resumo': {
                'totalVendas': total_vendas,
                'quantidadePedidos': qtd_pedidos,
                'ticketMedio': ticket_medio,
                'comissaoTotal': comissao_total
            },
            'porPeriodo': [{'data': k, 'valor': v} for k, v in sorted(vendas_por_dia.items())]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relatorios/clientes', methods=['GET'])
@api_login_required
def relatorio_clientes():
    try:
        if not db:
            return jsonify({
                'resumo': {
                    'totalClientes': 45,
                    'clientesAtivos': 38,
                    'clientesInativos': 7,
                    'novosNoMes': 5
                },
                'porStatus': [
                    {'status': 'ativo', 'quantidade': 38},
                    {'status': 'inativo', 'quantidade': 7}
                ],
                'melhoresClientes': [
                    {'nome': 'Elegance Store', 'totalCompras': 45000, 'pedidos': 12}
                ]
            }), 200
        
        # Busca clientes
        clientes_ref = db.collection('clientes').where('vendedorId', '==', current_user.id)
        clientes = list(clientes_ref.stream())
        
        total = len(clientes)
        ativos = 0
        inativos = 0
        novos = 0
        melhores = []
        
        inicio_mes = datetime.now(tz_brasil).replace(day=1)
        
        for doc in clientes:
            cliente = doc.to_dict()
            
            if cliente.get('status') == 'ativo':
                ativos += 1
            else:
                inativos += 1
            
            criado = cliente.get('criadoEm')
            if criado and hasattr(criado, 'replace'):
                if criado >= inicio_mes:
                    novos += 1
            
            melhores.append({
                'nome': cliente.get('fantasia', cliente.get('razaoSocial')),
                'totalCompras': cliente.get('totalCompras', 0),
                'pedidos': cliente.get('numeroCompras', 0)
            })
        
        # Top 10 clientes
        melhores.sort(key=lambda x: x['totalCompras'], reverse=True)
        melhores = melhores[:10]
        
        return jsonify({
            'resumo': {
                'totalClientes': total,
                'clientesAtivos': ativos,
                'clientesInativos': inativos,
                'novosNoMes': novos
            },
            'porStatus': [
                {'status': 'ativo', 'quantidade': ativos},
                {'status': 'inativo', 'quantidade': inativos}
            ],
            'melhoresClientes': melhores
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relatorios/produtos', methods=['GET'])
@api_login_required
def relatorio_produtos():
    try:
        if not db:
            return jsonify({
                'resumo': {
                    'totalProdutosVendidos': 230,
                    'produtosUnicos': 15,
                    'valorMedio': 150.00
                },
                'maisVendidos': [
                    {'nome': 'Produto A', 'quantidade': 50, 'valorTotal': 7500},
                    {'nome': 'Produto B', 'quantidade': 45, 'valorTotal': 6750}
                ]
            }), 200
        
        # Busca pedidos com itens
        pedidos_ref = db.collection('pedidos').where('vendedorId', '==', current_user.id)
        
        produtos_vendidos = {}
        total_itens = 0
        
        for doc in pedidos_ref.stream():
            pedido = doc.to_dict()
            itens = pedido.get('itens', [])
            
            for item in itens:
                nome = item.get('nome', item.get('produto', 'Produto'))
                qtd = item.get('quantidade', 1)
                valor = item.get('subtotal', item.get('preco', 0) * qtd)
                
                if nome not in produtos_vendidos:
                    produtos_vendidos[nome] = {'quantidade': 0, 'valorTotal': 0}
                
                produtos_vendidos[nome]['quantidade'] += qtd
                produtos_vendidos[nome]['valorTotal'] += valor
                total_itens += qtd
        
        # Converte para lista ordenada
        mais_vendidos = []
        for nome, dados in produtos_vendidos.items():
            mais_vendidos.append({
                'nome': nome,
                'quantidade': dados['quantidade'],
                'valorTotal': dados['valorTotal']
            })
        
        mais_vendidos.sort(key=lambda x: x['quantidade'], reverse=True)
        
        valor_total = sum([p['valorTotal'] for p in mais_vendidos])
        valor_medio = valor_total / total_itens if total_itens > 0 else 0
        
        return jsonify({
            'resumo': {
                'totalProdutosVendidos': total_itens,
                'produtosUnicos': len(produtos_vendidos),
                'valorMedio': valor_medio
            },
            'maisVendidos': mais_vendidos[:20]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relatorios/comissoes', methods=['GET'])
@api_login_required
def relatorio_comissoes():
    try:
        if not db:
            return jsonify({
                'resumo': {
                    'comissaoTotal': 6250,
                    'comissaoPaga': 4500,
                    'comissaoPendente': 1750,
                    'percentualMedio': 5
                },
                'porMes': [
                    {'mes': '2025-01', 'valor': 6250, 'status': 'pendente'}
                ],
                'detalhado': [
                    {'pedido': 'PED-001', 'valor': 10000, 'comissao': 500, 'percentual': 5, 'status': 'pago'}
                ]
            }), 200
        
        # Busca pedidos
        pedidos_ref = db.collection('pedidos').where('vendedorId', '==', current_user.id)
        
        comissao_total = 0
        comissao_paga = 0
        comissao_pendente = 0
        comissoes_mes = {}
        detalhado = []
        percentuais = []
        
        for doc in pedidos_ref.stream():
            pedido = doc.to_dict()
            comissao = pedido.get('comissao', 0)
            comissao_total += comissao
            
            status_comissao = pedido.get('comissaoStatus', 'pendente')
            if status_comissao == 'pago':
                comissao_paga += comissao
            else:
                comissao_pendente += comissao
            
            # Agrupa por mês
            data = pedido.get('data')
            if hasattr(data, 'strftime'):
                mes = data.strftime('%Y-%m')
            else:
                mes = str(data)[:7]
            
            if mes not in comissoes_mes:
                comissoes_mes[mes] = 0
            comissoes_mes[mes] += comissao
            
            percentuais.append(pedido.get('comissaoPercentual', 5))
            
            detalhado.append({
                'pedido': pedido.get('numero', doc.id),
                'valor': pedido.get('valorTotal', 0),
                'comissao': comissao,
                'percentual': pedido.get('comissaoPercentual', 5),
                'status': status_comissao
            })
        
        percentual_medio = sum(percentuais) / len(percentuais) if percentuais else 0
        
        return jsonify({
            'resumo': {
                'comissaoTotal': comissao_total,
                'comissaoPaga': comissao_paga,
                'comissaoPendente': comissao_pendente,
                'percentualMedio': percentual_medio
            },
            'porMes': [{'mes': k, 'valor': v} for k, v in sorted(comissoes_mes.items())],
            'detalhado': detalhado[:50]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - MAPA (MELHORADO) ============
@app.route('/api/mapa/clientes', methods=['GET'])
@api_login_required
def get_mapa_clientes():
    try:
        if not db:
            return jsonify([
                {
                    'id': '1',
                    'nome': 'Elegance Store',
                    'latitude': -23.5629,
                    'longitude': -46.6674,
                    'endereco': 'Rua Oscar Freire, 1234',
                    'telefone': '(11) 98765-4321',
                    'status': 'ativo',
                    'ultimaVisita': '2025-01-10'
                }
            ]), 200
        
        clientes_ref = db.collection('clientes').where('vendedorId', '==', current_user.id)
        
        clientes_mapa = []
        for doc in clientes_ref.stream():
            cliente = doc.to_dict()
            if cliente.get('latitude') and cliente.get('longitude'):
                endereco = cliente.get('endereco', {})
                clientes_mapa.append({
                    'id': doc.id,
                    'nome': cliente.get('fantasia', cliente.get('razaoSocial')),
                    'latitude': cliente.get('latitude'),
                    'longitude': cliente.get('longitude'),
                    'endereco': f"{endereco.get('logradouro', '')}, {endereco.get('numero', '')} - {endereco.get('cidade', '')}",
                    'telefone': cliente.get('telefone', ''),
                    'status': cliente.get('status', 'ativo'),
                    'ultimaVisita': cliente.get('ultimaVisita'),
                    'totalCompras': cliente.get('totalCompras', 0)
                })
        
        return jsonify(clientes_mapa), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mapa/configuracoes', methods=['GET'])
@api_login_required
def get_mapa_config():
    """Retorna configurações de personalização do mapa"""
    try:
        if not db:
            return jsonify({
                'tipoMapa': 'streets',
                'corMarcador': '#667eea',
                'mostrarRaio': False,
                'raioKm': 5,
                'agruparMarcadores': True,
                'mostrarTrafico': False
            }), 200
        
        user_doc = db.collection('usuarios').document(current_user.id).get()
        if user_doc.exists:
            config = user_doc.to_dict().get('configMapa', {})
            return jsonify(config), 200
        
        return jsonify({}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mapa/configuracoes', methods=['PUT'])
@api_login_required
def update_mapa_config():
    """Atualiza configurações do mapa"""
    try:
        if not db:
            return jsonify({'error': 'Sistema em modo DEMO'}), 400
        
        data = request.json
        
        db.collection('usuarios').document(current_user.id).update({
            'configMapa': data
        })
        
        return jsonify({'message': 'Configurações salvas'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mapa/otimizar-rota', methods=['POST'])
@api_login_required
def otimizar_rota():
    try:
        data = request.json
        cliente_ids = data.get('clienteIds', [])
        
        if not db or not cliente_ids:
            return jsonify({
                'rota': cliente_ids,
                'distanciaTotal': 45.2,
                'tempoEstimado': 180,
                'economia': {
                    'distancia': 12.5,
                    'tempo': 35
                }
            }), 200
        
        # Busca coordenadas dos clientes
        clientes_coords = []
        for cid in cliente_ids:
            cliente_doc = db.collection('clientes').document(cid).get()
            if cliente_doc.exists:
                cliente = cliente_doc.to_dict()
                if cliente.get('latitude') and cliente.get('longitude'):
                    clientes_coords.append({
                        'id': cid,
                        'lat': cliente.get('latitude'),
                        'lng': cliente.get('longitude'),
                        'nome': cliente.get('fantasia')
                    })
        
        # Algoritmo simples de otimização (nearest neighbor)
        if len(clientes_coords) > 1:
            otimizado = [clientes_coords[0]]
            restantes = clientes_coords[1:]
            
            while restantes:
                ultimo = otimizado[-1]
                mais_proximo = min(restantes, key=lambda x: geodesic(
                    (ultimo['lat'], ultimo['lng']),
                    (x['lat'], x['lng'])
                ).km)
                otimizado.append(mais_proximo)
                restantes.remove(mais_proximo)
            
            # Calcula distância total
            distancia_total = 0
            for i in range(len(otimizado) - 1):
                distancia_total += geodesic(
                    (otimizado[i]['lat'], otimizado[i]['lng']),
                    (otimizado[i+1]['lat'], otimizado[i+1]['lng'])
                ).km
            
            # Estima tempo (média 30km/h em área urbana + 10min por parada)
            tempo_estimado = (distancia_total / 30 * 60) + (len(otimizado) * 10)
            
            return jsonify({
                'rota': [c['id'] for c in otimizado],
                'rotaDetalhada': otimizado,
                'distanciaTotal': round(distancia_total, 2),
                'tempoEstimado': int(tempo_estimado),
                'economia': {
                    'distancia': round(distancia_total * 0.2, 2),
                    'tempo': int(tempo_estimado * 0.15)
                }
            }), 200
        
        return jsonify({
            'rota': cliente_ids,
            'distanciaTotal': 0,
            'tempoEstimado': 0,
            'economia': {'distancia': 0, 'tempo': 0}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ API - DASHBOARD ============
@app.route('/api/dashboard/stats', methods=['GET'])
@api_login_required
def get_dashboard_stats():
    try:
        if not db:
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
        compromissos_hoje = len(list(compromissos_ref.where('data', '==', str(hoje)).get()))
        
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
                'hoje': compromissos_hoje,
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
                'empresaAtual': current_user.empresa_id,
                'empresas': current_user.empresas
            }), 200
        
        user_doc = db.collection('usuarios').document(current_user.id).get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            user_data['id'] = current_user.id
            del user_data['senha']
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
        
        if 'senha' in data:
            del data['senha']
        if 'email' in data:
            del data['email']
        
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
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    css_file = 'static/css/style.css'
    if not os.path.exists(css_file):
        with open(css_file, 'w') as f:
            f.write('/* Custom CSS */')
    
    js_file = 'static/js/app.js'
    if not os.path.exists(js_file):
        with open(js_file, 'w') as f:
            f.write('console.log("App loaded");')
    
    app.run(debug=True, host='0.0.0.0', port=5000)