// Estado da aplicação
let currentScreen = 'home';
let clientes = [];
let compromissos = [];
let selectedClient = null;

// Inicializa a aplicação
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    navigateTo('home');
});

// Carrega dados do backend
async function loadData() {
    try {
        // Carrega clientes
        const clientesResponse = await axios.get('/api/clientes');
        clientes = clientesResponse.data;
        
        // Carrega compromissos
        const compromissosResponse = await axios.get('/api/compromissos');
        compromissos = compromissosResponse.data;
        
        // Atualiza a tela atual
        renderCurrentScreen();
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        showError('Erro ao carregar dados. Verifique sua conexão com o Firebase.');
    }
}

// Navegação entre telas
function navigateTo(screen) {
    currentScreen = screen;
    
    // Atualiza navegação ativa
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
    
    renderCurrentScreen();
}

// Renderiza a tela atual
function renderCurrentScreen() {
    const content = document.getElementById('app-content');
    
    switch(currentScreen) {
        case 'home':
            renderHomeScreen(content);
            break;
        case 'clients':
            renderClientsScreen(content);
            break;
        case 'map':
            renderMapScreen(content);
            break;
        case 'calendar':
            renderCalendarScreen(content);
            break;
        case 'goals':
            renderGoalsScreen(content);
            break;
    }
}

// Tela Home
function renderHomeScreen(container) {
    const clientesAtivos = clientes.filter(c => c.status === 'atual').length;
    const clientesAusentes = clientes.filter(c => c.status === 'ausente').length;
    
    container.innerHTML = `
        <div class="header">
            <h2>Olá, Vendedor!</h2>
            <p>Gerencie sua carteira de clientes</p>
        </div>
        
        <div style="padding: 20px;">
            <h3 style="font-size: 18px; margin-bottom: 15px;">Resumo</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                <div class="metric-card">
                    <div class="value" style="color: #667eea;">${clientes.length}</div>
                    <div class="label">Total Clientes</div>
                </div>
                <div class="metric-card">
                    <div class="value" style="color: #10b981;">${clientesAtivos}</div>
                    <div class="label">Clientes Ativos</div>
                </div>
                <div class="metric-card">
                    <div class="value" style="color: #f59e0b;">${clientesAusentes}</div>
                    <div class="label">Clientes Ausentes</div>
                </div>
                <div class="metric-card">
                    <div class="value" style="color: #8b5cf6;">${compromissos.length}</div>
                    <div class="label">Compromissos</div>
                </div>
            </div>
            
            <button class="btn-primary" onclick="showClientModal()" style="width: 100%; margin-bottom: 20px;">
                + Novo Cliente
            </button>
            
            <h3 style="font-size: 18px; margin-bottom: 15px;">Clientes Recentes</h3>
            ${clientes.slice(0, 3).map(cliente => `
                <div class="client-card" onclick="showClientDetail('${cliente.id}')">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <h4 style="margin: 0; font-size: 16px;">${cliente.fantasia}</h4>
                            <p style="margin: 5px 0; font-size: 13px; color: #666;">
                                📍 ${cliente.cidade} - ${cliente.bairro}
                            </p>
                        </div>
                        <span class="status-badge status-${cliente.status || 'atual'}">
                            ${cliente.status === 'atual' ? 'Atual' : cliente.status === 'ultima' ? 'Última' : 'Ausente'}
                        </span>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

// Tela de Clientes
function renderClientsScreen(container) {
    container.innerHTML = `
        <div class="header">
            <h2>Meus Clientes</h2>
            <div class="search-box">
                <input type="text" placeholder="Buscar clientes..." onkeyup="filterClients(this.value)">
            </div>
        </div>
        
        <div style="padding: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <span style="font-size: 14px; color: #666;">${clientes.length} clientes</span>
                <button class="btn-primary" onclick="showClientModal()" style="padding: 8px 16px; font-size: 12px;">
                    + Novo
                </button>
            </div>
            
            <div id="clients-list">
                ${renderClientsList(clientes)}
            </div>
        </div>
    `;
}

function renderClientsList(clientsList) {
    return clientsList.map(cliente => `
        <div class="client-card" onclick="showClientDetail('${cliente.id}')">
            <div style="display: flex; justify-content: space-between;">
                <div style="flex: 1;">
                    <h4 style="margin: 0; font-size: 16px;">${cliente.fantasia}</h4>
                    <p style="margin: 3px 0; font-size: 12px; color: #999;">${cliente.razaoSocial}</p>
                    <p style="margin: 5px 0; font-size: 13px; color: #666;">
                        📍 ${cliente.cidade} - ${cliente.bairro}
                    </p>
                </div>
                <span class="status-badge status-${cliente.status || 'atual'}">
                    ${cliente.status === 'atual' ? 'Atual' : cliente.status === 'ultima' ? 'Última' : 'Ausente'}
                </span>
            </div>
        </div>
    `).join('');
}

function filterClients(query) {
    const filtered = clientes.filter(c => 
        c.fantasia.toLowerCase().includes(query.toLowerCase()) ||
        c.cidade.toLowerCase().includes(query.toLowerCase())
    );
    document.getElementById('clients-list').innerHTML = renderClientsList(filtered);
}

// Modal de Cliente
function showClientModal(clienteId = null) {
    const cliente = clienteId ? clientes.find(c => c.id === clienteId) : null;
    
    const modalHtml = `
        <div class="modal-overlay" onclick="closeModal(event)">
            <div class="modal-content" onclick="event.stopPropagation()">
                <h2 style="margin-bottom: 20px;">${cliente ? 'Editar Cliente' : 'Novo Cliente'}</h2>
                <form onsubmit="saveClient(event, '${clienteId || ''}')">
                    <div class="form-group">
                        <label class="form-label">Razão Social *</label>
                        <input type="text" class="form-input" name="razaoSocial" value="${cliente?.razaoSocial || ''}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Nome Fantasia *</label>
                        <input type="text" class="form-input" name="fantasia" value="${cliente?.fantasia || ''}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">CNPJ *</label>
                        <input type="text" class="form-input" name="cnpj" value="${cliente?.cnpj || ''}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Telefone *</label>
                        <input type="text" class="form-input" name="telefone" value="${cliente?.telefone || ''}" required>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div class="form-group">
                            <label class="form-label">Cidade *</label>
                            <input type="text" class="form-input" name="cidade" value="${cliente?.cidade || ''}" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Bairro *</label>
                            <input type="text" class="form-input" name="bairro" value="${cliente?.bairro || ''}" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Status</label>
                        <select class="form-input" name="status">
                            <option value="atual" ${cliente?.status === 'atual' ? 'selected' : ''}>Atual</option>
                            <option value="ultima" ${cliente?.status === 'ultima' ? 'selected' : ''}>Última Coleção</option>
                            <option value="ausente" ${cliente?.status === 'ausente' ? 'selected' : ''}>Ausente</option>
                        </select>
                    </div>
                    <div style="display: flex; gap: 10px; margin-top: 20px;">
                        <button type="button" onclick="closeModal()" style="flex: 1; padding: 12px; border-radius: 10px; border: 1px solid #ddd; background: white; cursor: pointer;">
                            Cancelar
                        </button>
                        <button type="submit" class="btn-primary" style="flex: 1;">
                            Salvar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

async function saveClient(event, clienteId) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        if (clienteId) {
            await axios.put(`/api/clientes/${clienteId}`, data);
        } else {
            await axios.post('/api/clientes', data);
        }
        
        closeModal();
        await loadData();
        showSuccess('Cliente salvo com sucesso!');
    } catch (error) {
        console.error('Erro ao salvar cliente:', error);
        showError('Erro ao salvar cliente');
    }
}

function closeModal(event) {
    if (!event || event.target.classList.contains('modal-overlay')) {
        document.querySelector('.modal-overlay')?.remove();
    }
}

// Outras telas (simplificado)
function renderMapScreen(container) {
    container.innerHTML = `
        <div class="header">
            <h2>Mapa de Clientes</h2>
        </div>
        <div style="padding: 20px; text-align: center;">
            <p>Funcionalidade de mapa em desenvolvimento</p>
        </div>
    `;
}

function renderCalendarScreen(container) {
    container.innerHTML = `
        <div class="header">
            <h2>Agenda</h2>
        </div>
        <div style="padding: 20px;">
            <button class="btn-primary" onclick="showAppointmentModal()" style="width: 100%; margin-bottom: 20px;">
                + Novo Compromisso
            </button>
            ${compromissos.map(c => `
                <div class="client-card">
                    <strong>${c.cliente}</strong><br>
                    <span style="font-size: 13px; color: #666;">${c.data} às ${c.hora}</span>
                </div>
            `).join('')}
        </div>
    `;
}

function renderGoalsScreen(container) {
    container.innerHTML = `
        <div class="header">
            <h2>Metas & Performance</h2>
        </div>
        <div style="padding: 20px; text-align: center;">
            <p>Dashboard de metas em desenvolvimento</p>
        </div>
    `;
}

// Funções auxiliares
function showSuccess(message) {
    alert(message); // Substituir por toast/notification
}

function showError(message) {
    alert(message); // Substituir por toast/notification
}

function showAppointmentModal() {
    // Implementar modal de compromisso
    alert('Modal de compromisso em desenvolvimento');
}

function showClientDetail(clienteId) {
    selectedClient = clientes.find(c => c.id === clienteId);
    if (selectedClient) {
        showClientModal(clienteId);
    }
}
