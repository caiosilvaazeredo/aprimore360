# App de Gestão Comercial - Flask + Firebase

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no Firebase (Google Cloud)
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Firebase

#### 2.1. Acessar o Console do Firebase
1. Acesse: https://console.firebase.google.com/
2. Selecione seu projeto: `representante-comercial-c1098`

#### 2.2. Criar Service Account
1. No Console do Firebase, clique em **Configurações** (ícone de engrenagem) > **Configurações do projeto**
2. Vá para a aba **Contas de serviço**
3. Clique em **Gerar nova chave privada**
4. Um arquivo JSON será baixado (ex: `representante-comercial-xxxxx.json`)

#### 2.3. Configurar variáveis de ambiente
1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

2. Abra o arquivo JSON baixado e preencha o `.env` com as informações:
   ```
   FIREBASE_PROJECT_ID=representante-comercial-c1098
   FIREBASE_PRIVATE_KEY_ID=valor_do_private_key_id
   FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nCOLE_AQUI_A_CHAVE_COMPLETA\n-----END PRIVATE KEY-----\n"
   FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@representante-comercial-c1098.iam.gserviceaccount.com
   FIREBASE_CLIENT_ID=valor_do_client_id
   SECRET_KEY=sua_chave_secreta_aqui
   ```

**IMPORTANTE:** 
- A `FIREBASE_PRIVATE_KEY` deve estar entre aspas duplas
- Mantenha os `\n` no lugar das quebras de linha
- Não compartilhe o arquivo `.env` com ninguém

### 3. Habilitar Firestore

1. No Console do Firebase, vá em **Firestore Database**
2. Clique em **Criar banco de dados**
3. Escolha **Modo de produção** (você pode ajustar as regras depois)
4. Selecione a localização (ex: `southamerica-east1`)
5. Clique em **Ativar**

### 4. Configurar regras do Firestore (Opcional)

Se quiser permitir acesso público temporário para testes:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

**ATENÇÃO:** Para produção, configure regras de segurança apropriadas!

## ▶️ Executar a aplicação

```bash
python app.py
```

A aplicação estará disponível em: http://localhost:5000

## 📁 Estrutura do Projeto

```
.
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── .env                   # Variáveis de ambiente (não commitar!)
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo git
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   └── templates/
│       └── index.html
```

## 🔥 API Endpoints

### Clientes
- `GET /api/clientes` - Lista todos os clientes
- `GET /api/clientes/<id>` - Busca um cliente específico
- `POST /api/clientes` - Cria novo cliente
- `PUT /api/clientes/<id>` - Atualiza cliente
- `DELETE /api/clientes/<id>` - Remove cliente

### Compromissos
- `GET /api/compromissos` - Lista todos os compromissos
- `POST /api/compromissos` - Cria novo compromisso
- `PUT /api/compromissos/<id>` - Atualiza compromisso
- `DELETE /api/compromissos/<id>` - Remove compromisso

### Estatísticas
- `GET /api/stats` - Retorna estatísticas gerais

## 🐛 Troubleshooting

### Erro: "Failed to initialize Firebase"
- Verifique se o arquivo `.env` está configurado corretamente
- Confirme que você baixou a chave privada do Firebase
- Verifique se a `FIREBASE_PRIVATE_KEY` está formatada corretamente

### Erro: "Module not found"
- Execute: `pip install -r requirements.txt`

### Erro: "Port already in use"
- Altere a porta no `app.py`: `app.run(port=8000)`

## 📝 Próximos Passos

1. Implementar autenticação de usuários
2. Adicionar validações de formulário
3. Implementar upload de imagens
4. Adicionar geolocalização real
5. Implementar notificações push
6. Deploy em produção (Heroku, Google Cloud, etc.)

## 🔒 Segurança

**NUNCA** commite:
- Arquivo `.env`
- Chaves privadas do Firebase
- Credenciais de qualquer tipo

Use sempre `.gitignore` apropriado!

## 📄 Licença

Este projeto é apenas para fins educacionais.
