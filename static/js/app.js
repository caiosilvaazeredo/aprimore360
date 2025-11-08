const { useState } = React;

        // Ícones SVG modernos
        const Icons = {
            Home: () => (
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
            ),
            Users: () => (
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
            ),
            Map: () => (
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
            ),
            Calendar: () => (
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
            ),
            Chart: () => (
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
            ),
            Search: () => (
                <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            ),
            Plus: () => (
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
                </svg>
            ),
            Phone: () => (
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
            ),
            MapPin: () => (
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
            ),
            Brain: () => (
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
            ),
            ArrowLeft: () => (
                <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
            ),
            Close: () => (
                <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
                </svg>
            ),
            Edit: () => (
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
            ),
        };

        // Dados mockados
        let clientesData = [
            {
                id: 1,
                razaoSocial: "Boutique Elegance Ltda",
                fantasia: "Elegance Store",
                cnpj: "12.345.678/0001-90",
                telefone: "(11) 98765-4321",
                cidade: "São Paulo",
                bairro: "Jardins",
                status: "atual",
                ultimaColecao: "Verão 2025",
                ultimoDesconto: "5% Financeiro",
                dataFaturamento: "15/10/2025",
                prazo: "30 dias",
                marcas: ["Marca A", "Marca B"],
                lat: 35,
                lng: 25
            },
            {
                id: 2,
                razaoSocial: "Fashion Point Comércio",
                fantasia: "Fashion Point",
                cnpj: "98.765.432/0001-10",
                telefone: "(11) 97654-3210",
                cidade: "São Paulo",
                bairro: "Vila Madalena",
                status: "ultima",
                ultimaColecao: "Inverno 2024",
                ultimoDesconto: "10% Showroom",
                dataFaturamento: "20/09/2025",
                prazo: "45 dias",
                marcas: ["Marca C"],
                lat: 50,
                lng: 50
            },
            {
                id: 3,
                razaoSocial: "Style House Brasil SA",
                fantasia: "Style House",
                cnpj: "11.222.333/0001-44",
                telefone: "(11) 96543-2109",
                cidade: "São Paulo",
                bairro: "Moema",
                status: "ausente",
                ultimaColecao: "Primavera 2024",
                ultimoDesconto: "3% Antecipação",
                dataFaturamento: "05/08/2025",
                prazo: "60 dias",
                marcas: ["Marca A", "Marca D"],
                lat: 15,
                lng: 70
            }
        ];

        let compromissosData = [
            { id: 1, data: '2025-10-20', hora: '09:00', cliente: 'Elegance Store', tipo: 'visita' },
            { id: 2, data: '2025-10-20', hora: '14:00', cliente: 'Fashion Point', tipo: 'visita' },
            { id: 3, data: '2025-10-21', hora: '10:00', cliente: 'Style House', tipo: 'visita' },
        ];

        function App() {
            const [currentScreen, setCurrentScreen] = useState('home');
            const [selectedClient, setSelectedClient] = useState(null);
            const [showClientModal, setShowClientModal] = useState(false);
            const [showAppointmentModal, setShowAppointmentModal] = useState(false);
            const [editingAppointment, setEditingAppointment] = useState(null);
            const [clientes, setClientes] = useState(clientesData);
            const [compromissos, setCompromissos] = useState(compromissosData);

            const handleAddClient = (newClient) => {
                const cliente = {
                    ...newClient,
                    id: clientes.length + 1,
                    status: 'atual',
                    lat: Math.random() * 80 + 10,
                    lng: Math.random() * 80 + 10
                };
                setClientes([...clientes, cliente]);
                setShowClientModal(false);
            };

            const handleAddAppointment = (appointment) => {
                if (editingAppointment) {
                    setCompromissos(compromissos.map(c => 
                        c.id === editingAppointment.id ? {...appointment, id: c.id} : c
                    ));
                } else {
                    setCompromissos([...compromissos, {...appointment, id: compromissos.length + 1}]);
                }
                setShowAppointmentModal(false);
                setEditingAppointment(null);
            };

            const renderScreen = () => {
                switch(currentScreen) {
                    case 'home':
                        return <HomeScreen 
                            onNavigate={setCurrentScreen} 
                            onAddClient={() => setShowClientModal(true)}
                            clientes={clientes}
                        />;
                    case 'clients':
                        return <ClientsScreen 
                            clientes={clientes}
                            onClientSelect={(client) => {
                                setSelectedClient(client);
                                setCurrentScreen('clientDetail');
                            }}
                            onAddClient={() => setShowClientModal(true)}
                        />;
                    case 'clientDetail':
                        return <ClientDetailScreen 
                            client={selectedClient} 
                            onBack={() => setCurrentScreen('clients')} 
                        />;
                    case 'map':
                        return <MapScreen 
                            clientes={clientes}
                            onClientSelect={(client) => {
                                setSelectedClient(client);
                                setCurrentScreen('clientDetail');
                            }} 
                        />;
                    case 'calendar':
                        return <CalendarScreen 
                            compromissos={compromissos}
                            onAddAppointment={() => setShowAppointmentModal(true)}
                            onEditAppointment={(apt) => {
                                setEditingAppointment(apt);
                                setShowAppointmentModal(true);
                            }}
                        />;
                    case 'goals':
                        return <GoalsScreen />;
                    default:
                        return <HomeScreen onNavigate={setCurrentScreen} />;
                }
            };

            return (
                <>
                    <div className="status-bar">
                        <span>9:41</span>
                        <span>5G ●●●●</span>
                    </div>
                    <div className="app-content" style={{paddingBottom: currentScreen === 'clientDetail' ? '0' : '65px'}}>
                        {renderScreen()}
                    </div>
                    {currentScreen !== 'clientDetail' && (
                        <div className="bottom-nav">
                            <div className={`nav-item ${currentScreen === 'home' ? 'active' : ''}`} onClick={() => setCurrentScreen('home')}>
                                <Icons.Home />
                                <span style={{fontSize: '11px'}}>Início</span>
                            </div>
                            <div className={`nav-item ${currentScreen === 'clients' ? 'active' : ''}`} onClick={() => setCurrentScreen('clients')}>
                                <Icons.Users />
                                <span style={{fontSize: '11px'}}>Clientes</span>
                            </div>
                            <div className={`nav-item ${currentScreen === 'map' ? 'active' : ''}`} onClick={() => setCurrentScreen('map')}>
                                <Icons.Map />
                                <span style={{fontSize: '11px'}}>Mapa</span>
                            </div>
                            <div className={`nav-item ${currentScreen === 'calendar' ? 'active' : ''}`} onClick={() => setCurrentScreen('calendar')}>
                                <Icons.Calendar />
                                <span style={{fontSize: '11px'}}>Agenda</span>
                            </div>
                            <div className={`nav-item ${currentScreen === 'goals' ? 'active' : ''}`} onClick={() => setCurrentScreen('goals')}>
                                <Icons.Chart />
                                <span style={{fontSize: '11px'}}>Metas</span>
                            </div>
                        </div>
                    )}
                    {showClientModal && (
                        <ClientModal 
                            onClose={() => setShowClientModal(false)}
                            onSave={handleAddClient}
                        />
                    )}
                    {showAppointmentModal && (
                        <AppointmentModal 
                            onClose={() => {
                                setShowAppointmentModal(false);
                                setEditingAppointment(null);
                            }}
                            onSave={handleAddAppointment}
                            clientes={clientes}
                            appointment={editingAppointment}
                        />
                    )}
                </>
            );
        }

        function ClientModal({ onClose, onSave }) {
            const [formData, setFormData] = useState({
                razaoSocial: '',
                fantasia: '',
                cnpj: '',
                telefone: '',
                cidade: '',
                bairro: '',
                marcas: [],
                ultimoDesconto: '',
                prazo: '30 dias'
            });

            const handleSubmit = (e) => {
                e.preventDefault();
                onSave(formData);
            };

            return (
                <div className="modal-overlay" onClick={onClose}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
                            <h2 style={{margin: 0, fontSize: '20px', fontWeight: 'bold'}}>Novo Cliente</h2>
                            <button onClick={onClose} style={{background: 'none', border: 'none', cursor: 'pointer'}}>
                                <Icons.Close />
                            </button>
                        </div>
                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label className="form-label">Razão Social *</label>
                                <input 
                                    className="form-input" 
                                    required
                                    value={formData.razaoSocial}
                                    onChange={(e) => setFormData({...formData, razaoSocial: e.target.value})}
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">Nome Fantasia *</label>
                                <input 
                                    className="form-input" 
                                    required
                                    value={formData.fantasia}
                                    onChange={(e) => setFormData({...formData, fantasia: e.target.value})}
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">CNPJ *</label>
                                <input 
                                    className="form-input" 
                                    required
                                    placeholder="00.000.000/0000-00"
                                    value={formData.cnpj}
                                    onChange={(e) => setFormData({...formData, cnpj: e.target.value})}
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">Telefone *</label>
                                <input 
                                    className="form-input" 
                                    required
                                    placeholder="(00) 00000-0000"
                                    value={formData.telefone}
                                    onChange={(e) => setFormData({...formData, telefone: e.target.value})}
                                />
                            </div>
                            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px'}}>
                                <div className="form-group">
                                    <label className="form-label">Cidade *</label>
                                    <input 
                                        className="form-input" 
                                        required
                                        value={formData.cidade}
                                        onChange={(e) => setFormData({...formData, cidade: e.target.value})}
                                    />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Bairro *</label>
                                    <input 
                                        className="form-input" 
                                        required
                                        value={formData.bairro}
                                        onChange={(e) => setFormData({...formData, bairro: e.target.value})}
                                    />
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Prazo de Pagamento</label>
                                <select 
                                    className="form-select"
                                    value={formData.prazo}
                                    onChange={(e) => setFormData({...formData, prazo: e.target.value})}
                                >
                                    <option>30 dias</option>
                                    <option>45 dias</option>
                                    <option>60 dias</option>
                                    <option>90 dias</option>
                                </select>
                            </div>
                            <div style={{display: 'flex', gap: '10px', marginTop: '20px'}}>
                                <button type="button" className="btn-secondary" onClick={onClose} style={{flex: 1}}>
                                    Cancelar
                                </button>
                                <button type="submit" className="btn-primary" style={{flex: 1}}>
                                    Salvar Cliente
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            );
        }

        function AppointmentModal({ onClose, onSave, clientes, appointment }) {
            const [formData, setFormData] = useState(appointment || {
                data: '',
                hora: '',
                cliente: '',
                tipo: 'visita',
                observacoes: ''
            });

            const handleSubmit = (e) => {
                e.preventDefault();
                onSave(formData);
            };

            return (
                <div className="modal-overlay" onClick={onClose}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
                            <h2 style={{margin: 0, fontSize: '20px', fontWeight: 'bold'}}>
                                {appointment ? 'Editar Compromisso' : 'Novo Compromisso'}
                            </h2>
                            <button onClick={onClose} style={{background: 'none', border: 'none', cursor: 'pointer'}}>
                                <Icons.Close />
                            </button>
                        </div>
                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label className="form-label">Cliente *</label>
                                <select 
                                    className="form-select"
                                    required
                                    value={formData.cliente}
                                    onChange={(e) => setFormData({...formData, cliente: e.target.value})}
                                >
                                    <option value="">Selecione um cliente</option>
                                    {clientes.map(c => (
                                        <option key={c.id} value={c.fantasia}>{c.fantasia}</option>
                                    ))}
                                </select>
                            </div>
                            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px'}}>
                                <div className="form-group">
                                    <label className="form-label">Data *</label>
                                    <input 
                                        type="date"
                                        className="form-input" 
                                        required
                                        value={formData.data}
                                        onChange={(e) => setFormData({...formData, data: e.target.value})}
                                    />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Hora *</label>
                                    <input 
                                        type="time"
                                        className="form-input" 
                                        required
                                        value={formData.hora}
                                        onChange={(e) => setFormData({...formData, hora: e.target.value})}
                                    />
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Tipo</label>
                                <select 
                                    className="form-select"
                                    value={formData.tipo}
                                    onChange={(e) => setFormData({...formData, tipo: e.target.value})}
                                >
                                    <option value="visita">Visita</option>
                                    <option value="ligacao">Ligação</option>
                                    <option value="reuniao">Reunião</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Observações</label>
                                <textarea 
                                    className="form-input" 
                                    rows="3"
                                    value={formData.observacoes}
                                    onChange={(e) => setFormData({...formData, observacoes: e.target.value})}
                                />
                            </div>
                            <div style={{display: 'flex', gap: '10px', marginTop: '20px'}}>
                                <button type="button" className="btn-secondary" onClick={onClose} style={{flex: 1}}>
                                    Cancelar
                                </button>
                                <button type="submit" className="btn-primary" style={{flex: 1}}>
                                    Salvar
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            );
        }

        function HomeScreen({ onNavigate, onAddClient, clientes }) {
            return (
                <>
                    <div className="header">
                        <h2 style={{margin: 0, fontSize: '24px', fontWeight: 'bold'}}>Olá, Vendedor!</h2>
                        <p style={{margin: '5px 0 0 0', opacity: 0.9}}>Sexta-feira, 17 de Outubro</p>
                        <div className="search-box">
                            <Icons.Search />
                            <input type="text" placeholder="Buscar clientes, cidades..." />
                        </div>
                    </div>

                    <div className="ai-suggestion">
                        <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                            <Icons.Brain />
                            <strong style={{marginLeft: '10px'}}>Sugestão da IA</strong>
                        </div>
                        <p style={{margin: 0, fontSize: '14px'}}>
                            Rota otimizada hoje: Visite Fashion Point (manhã) e Elegance Store (tarde). 
                            Economia de 45 min e 12km. Probabilidade de venda: 85%
                        </p>
                    </div>

                    <div style={{padding: '15px', paddingBottom: '100px'}}>
                        <h3 style={{fontSize: '18px', fontWeight: '600', marginBottom: '15px'}}>Resumo do Dia</h3>
                        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px'}}>
                            <div className="metric-card">
                                <div style={{fontSize: '28px', fontWeight: 'bold', color: '#667eea'}}>4</div>
                                <div style={{fontSize: '12px', color: '#666', marginTop: '5px'}}>Visitas Agendadas</div>
                            </div>
                            <div className="metric-card">
                                <div style={{fontSize: '28px', fontWeight: 'bold', color: '#10b981'}}>87%</div>
                                <div style={{fontSize: '12px', color: '#666', marginTop: '5px'}}>Meta Mensal</div>
                            </div>
                            <div className="metric-card">
                                <div style={{fontSize: '28px', fontWeight: 'bold', color: '#f59e0b'}}>12</div>
                                <div style={{fontSize: '12px', color: '#666', marginTop: '5px'}}>Clientes Ausentes</div>
                            </div>
                            <div className="metric-card">
                                <div style={{fontSize: '28px', fontWeight: 'bold', color: '#8b5cf6'}}>R$ 45k</div>
                                <div style={{fontSize: '12px', color: '#666', marginTop: '5px'}}>Vendas Semana</div>
                            </div>
                        </div>

                        <h3 style={{fontSize: '18px', fontWeight: '600', margin: '20px 0 15px 0'}}>Ações Rápidas</h3>
                        <div style={{display: 'grid', gap: '10px'}}>
                            <div className="action-button" onClick={onAddClient}>
                                <div style={{display: 'flex', alignItems: 'center', gap: '15px'}}>
                                    <div className="action-icon" style={{background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white'}}>
                                        <Icons.Plus />
                                    </div>
                                    <div>
                                        <div style={{fontWeight: '600', fontSize: '15px'}}>Novo Cliente</div>
                                        <div style={{fontSize: '12px', color: '#666'}}>Adicionar cliente à carteira</div>
                                    </div>
                                </div>
                                <svg width="20" height="20" fill="none" stroke="#ccc" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                </svg>
                            </div>
                            <div className="action-button" onClick={() => onNavigate('map')}>
                                <div style={{display: 'flex', alignItems: 'center', gap: '15px'}}>
                                    <div className="action-icon" style={{background: '#10b981', color: 'white'}}>
                                        <Icons.MapPin />
                                    </div>
                                    <div>
                                        <div style={{fontWeight: '600', fontSize: '15px'}}>Ver Rotas do Dia</div>
                                        <div style={{fontSize: '12px', color: '#666'}}>Otimizar trajeto</div>
                                    </div>
                                </div>
                                <svg width="20" height="20" fill="none" stroke="#ccc" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                </svg>
                            </div>
                        </div>

                        <h3 style={{fontSize: '18px', fontWeight: '600', margin: '20px 0 15px 0'}}>Próximas Visitas</h3>
                        {clientes.slice(0, 2).map(client => (
                            <div key={client.id} className="client-card" onClick={() => {
                                onNavigate('clientDetail');
                            }}>
                                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
                                    <div>
                                        <h4 style={{margin: 0, fontSize: '16px', fontWeight: '600'}}>{client.fantasia}</h4>
                                        <p style={{margin: '5px 0', fontSize: '13px', color: '#666'}}>
                                            📍 {client.cidade} - {client.bairro}
                                        </p>
                                    </div>
                                    <span className={`status-badge status-${client.status}`}>
                                        {client.status === 'atual' ? 'Atual' : client.status === 'ultima' ? 'Última' : 'Ausente'}
                                    </span>
                                </div>
                                <div style={{marginTop: '10px', fontSize: '12px', color: '#888', display: 'flex', alignItems: 'center', gap: '5px'}}>
                                    <Icons.Phone /> {client.telefone}
                                </div>
                            </div>
                        ))}
                    </div>
                </>
            );
        }

        function ClientsScreen({ clientes, onClientSelect, onAddClient }) {
            const [searchTerm, setSearchTerm] = useState('');

            const filteredClients = clientes.filter(client =>
                client.fantasia.toLowerCase().includes(searchTerm.toLowerCase()) ||
                client.cidade.toLowerCase().includes(searchTerm.toLowerCase())
            );

            return (
                <>
                    <div className="header">
                        <h2 style={{margin: 0, fontSize: '24px', fontWeight: 'bold'}}>Meus Clientes</h2>
                        <div className="search-box">
                            <Icons.Search />
                            <input 
                                type="text" 
                                placeholder="Buscar clientes..." 
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>

                    <div style={{padding: '15px', paddingBottom: '100px'}}>
                        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px'}}>
                            <span style={{fontSize: '14px', color: '#666'}}>{filteredClients.length} clientes encontrados</span>
                            <button className="btn-primary" onClick={onAddClient} style={{padding: '8px 16px', fontSize: '12px'}}>
                                + Novo Cliente
                            </button>
                        </div>

                        {filteredClients.map(client => (
                            <div key={client.id} className="client-card" onClick={() => onClientSelect(client)}>
                                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start'}}>
                                    <div style={{flex: 1}}>
                                        <h4 style={{margin: 0, fontSize: '16px', fontWeight: '600'}}>{client.fantasia}</h4>
                                        <p style={{margin: '3px 0', fontSize: '12px', color: '#999'}}>{client.razaoSocial}</p>
                                        <p style={{margin: '5px 0', fontSize: '13px', color: '#666'}}>
                                            📍 {client.cidade} - {client.bairro}
                                        </p>
                                        {client.marcas && client.marcas.length > 0 && (
                                            <div style={{marginTop: '8px', display: 'flex', gap: '8px', flexWrap: 'wrap'}}>
                                                {client.marcas.map((marca, idx) => (
                                                    <span key={idx} style={{
                                                        background: '#f3f4f6',
                                                        padding: '3px 8px',
                                                        borderRadius: '10px',
                                                        fontSize: '10px',
                                                        color: '#666'
                                                    }}>
                                                        {marca}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                    <span className={`status-badge status-${client.status}`}>
                                        {client.status === 'atual' ? 'Atual' : client.status === 'ultima' ? 'Última' : 'Ausente'}
                                    </span>
                                </div>
                                {client.ultimaColecao && (
                                    <div style={{
                                        marginTop: '12px',
                                        paddingTop: '12px',
                                        borderTop: '1px solid #f0f0f0',
                                        fontSize: '11px',
                                        color: '#888',
                                        display: 'flex',
                                        justifyContent: 'space-between'
                                    }}>
                                        <span>Último pedido: {client.ultimaColecao}</span>
                                        <span>{client.ultimoDesconto}</span>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </>
            );
        }

        function ClientDetailScreen({ client, onBack }) {
            if (!client) return <div>Cliente não encontrado</div>;

            return (
                <div style={{background: 'white', minHeight: '100%', paddingBottom: '20px'}}>
                    <div className="header-with-back">
                        <button onClick={onBack} className="back-button">
                            <Icons.ArrowLeft />
                        </button>
                        <div style={{flex: 1}}>
                            <h2 style={{margin: 0, fontSize: '22px', fontWeight: 'bold'}}>{client.fantasia}</h2>
                            <p style={{margin: '5px 0 0 0', opacity: 0.9, fontSize: '14px'}}>{client.razaoSocial}</p>
                        </div>
                    </div>

                    <div style={{padding: '20px'}}>
                        <div style={{background: '#f9fafb', padding: '15px', borderRadius: '12px', marginBottom: '20px'}}>
                            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '12px'}}>
                                <span style={{color: '#666', fontSize: '14px'}}>Status</span>
                                <span className={`status-badge status-${client.status}`}>
                                    {client.status === 'atual' ? 'Cliente Atual' : client.status === 'ultima' ? 'Última Coleção' : 'Ausente'}
                                </span>
                            </div>
                            <div style={{display: 'grid', gap: '10px', fontSize: '14px'}}>
                                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                    <span style={{color: '#666'}}>CNPJ</span>
                                    <strong>{client.cnpj}</strong>
                                </div>
                                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                    <span style={{color: '#666'}}>Telefone</span>
                                    <strong>{client.telefone}</strong>
                                </div>
                                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                    <span style={{color: '#666'}}>Localização</span>
                                    <strong>{client.cidade} - {client.bairro}</strong>
                                </div>
                            </div>
                        </div>

                        {client.ultimaColecao && (
                            <>
                                <h3 style={{fontSize: '16px', fontWeight: '600', marginBottom: '12px'}}>Histórico de Vendas</h3>
                                <div style={{background: 'white', border: '1px solid #e5e7eb', borderRadius: '12px', padding: '15px', marginBottom: '20px'}}>
                                    <div style={{marginBottom: '15px'}}>
                                        <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '5px'}}>
                                            <span style={{fontSize: '14px', color: '#666'}}>Última Coleção</span>
                                            <strong style={{fontSize: '14px'}}>{client.ultimaColecao}</strong>
                                        </div>
                                        <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '5px'}}>
                                            <span style={{fontSize: '14px', color: '#666'}}>Último Desconto</span>
                                            <strong style={{fontSize: '14px', color: '#10b981'}}>{client.ultimoDesconto}</strong>
                                        </div>
                                        {client.dataFaturamento && (
                                            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '5px'}}>
                                                <span style={{fontSize: '14px', color: '#666'}}>Data Faturamento</span>
                                                <strong style={{fontSize: '14px'}}>{client.dataFaturamento}</strong>
                                            </div>
                                        )}
                                        {client.prazo && (
                                            <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                                <span style={{fontSize: '14px', color: '#666'}}>Prazo</span>
                                                <strong style={{fontSize: '14px'}}>{client.prazo}</strong>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </>
                        )}

                        {client.marcas && client.marcas.length > 0 && (
                            <>
                                <h3 style={{fontSize: '16px', fontWeight: '600', marginBottom: '12px'}}>Marcas Compradas</h3>
                                <div style={{display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap'}}>
                                    {client.marcas.map((marca, idx) => (
                                        <span key={idx} style={{
                                            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                            color: 'white',
                                            padding: '8px 16px',
                                            borderRadius: '20px',
                                            fontSize: '13px',
                                            fontWeight: '500'
                                        }}>
                                            {marca}
                                        </span>
                                    ))}
                                </div>
                            </>
                        )}

                        <h3 style={{fontSize: '16px', fontWeight: '600', marginBottom: '12px'}}>Localização</h3>
                        <div style={{
                            width: '100%',
                            height: '200px',
                            background: 'linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)',
                            borderRadius: '12px',
                            marginBottom: '20px',
                            position: 'relative',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
                            backgroundSize: '20px 20px'
                        }}>
                            <div style={{textAlign: 'center'}}>
                                <div style={{fontSize: '50px'}}>📍</div>
                                <div style={{fontSize: '13px', fontWeight: '600', color: '#374151', marginTop: '8px'}}>
                                    {client.cidade} - {client.bairro}
                                </div>
                            </div>
                        </div>

                        <div style={{display: 'grid', gap: '10px'}}>
                            <button className="btn-primary" style={{width: '100%'}}>
                                💬 Enviar WhatsApp
                            </button>
                            <button className="btn-primary" style={{width: '100%'}}>
                                🗺️ Abrir no Waze
                            </button>
                            <button className="btn-primary" style={{width: '100%'}}>
                                📅 Agendar Visita
                            </button>
                        </div>
                    </div>
                </div>
            );
        }

        function MapScreen({ clientes, onClientSelect }) {
            return (
                <>
                    <div className="header">
                        <h2 style={{margin: 0, fontSize: '24px', fontWeight: 'bold'}}>Mapa de Clientes</h2>
                        <p style={{margin: '5px 0 0 0', opacity: 0.9, fontSize: '13px'}}>São Paulo - Zona Sul</p>
                    </div>

                    <div style={{position: 'relative'}}>
                        <div className="map-container">
                            {/* Ruas horizontais */}
                            <div className="street street-h" style={{top: '20%'}}></div>
                            <div className="street street-h" style={{top: '40%'}}></div>
                            <div className="street street-h" style={{top: '60%'}}></div>
                            <div className="street street-h" style={{top: '80%'}}></div>
                            
                            {/* Ruas verticais */}
                            <div className="street street-v" style={{left: '25%'}}></div>
                            <div className="street street-v" style={{left: '50%'}}></div>
                            <div className="street street-v" style={{left: '75%'}}></div>
                            
                            {/* Pins dos clientes */}
                            {clientes.map(client => (
                                <div
                                    key={client.id}
                                    className="map-pin"
                                    style={{
                                        left: `${client.lng}%`,
                                        top: `${client.lat}%`,
                                        background: client.status === 'atual' ? '#10b981' : client.status === 'ultima' ? '#f59e0b' : '#ef4444',
                                        boxShadow: `0 0 0 8px ${client.status === 'atual' ? 'rgba(16, 185, 129, 0.2)' : client.status === 'ultima' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(239, 68, 68, 0.2)'}`
                                    }}
                                    onClick={() => onClientSelect(client)}
                                    title={client.fantasia}
                                >
                                    📍
                                </div>
                            ))}
                            
                            {/* Legenda */}
                            <div style={{
                                position: 'absolute',
                                bottom: '15px',
                                left: '15px',
                                background: 'white',
                                padding: '12px',
                                borderRadius: '10px',
                                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                                fontSize: '11px',
                                fontWeight: '500'
                            }}>
                                <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '5px'}}>
                                    <div style={{width: '12px', height: '12px', borderRadius: '50%', background: '#10b981'}}></div>
                                    <span>Atual</span>
                                </div>
                                <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '5px'}}>
                                    <div style={{width: '12px', height: '12px', borderRadius: '50%', background: '#f59e0b'}}></div>
                                    <span>Última Coleção</span>
                                </div>
                                <div style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
                                    <div style={{width: '12px', height: '12px', borderRadius: '50%', background: '#ef4444'}}></div>
                                    <span>Ausente</span>
                                </div>
                            </div>
                        </div>

                        <div className="ai-suggestion" style={{margin: '15px'}}>
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '8px'}}>
                                <Icons.Brain />
                                <strong style={{marginLeft: '8px', fontSize: '14px'}}>Rota Inteligente</strong>
                            </div>
                            <p style={{margin: 0, fontSize: '13px'}}>
                                Sequência ideal: Elegance → Fashion Point → Style House<br/>
                                Economia: 25km e 40min
                            </p>
                            <button className="btn-primary" style={{marginTop: '12px', width: '100%', padding: '10px'}}>
                                🚗 Iniciar Navegação no Waze
                            </button>
                        </div>

                        <div style={{padding: '0 15px 100px 15px'}}>
                            <h3 style={{fontSize: '16px', fontWeight: '600', marginBottom: '12px'}}>Clientes Próximos</h3>
                            {clientes.map(client => (
                                <div key={client.id} className="client-card" onClick={() => onClientSelect(client)}>
                                    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                                        <div>
                                            <h4 style={{margin: 0, fontSize: '15px', fontWeight: '600'}}>{client.fantasia}</h4>
                                            <p style={{margin: '5px 0 0 0', fontSize: '12px', color: '#666'}}>
                                                📍 {client.cidade} - {client.bairro}
                                            </p>
                                        </div>
                                        <div style={{textAlign: 'right'}}>
                                            <span className={`status-badge status-${client.status}`} style={{fontSize: '10px'}}>
                                                {client.status === 'atual' ? 'Atual' : client.status === 'ultima' ? 'Última' : 'Ausente'}
                                            </span>
                                            <div style={{fontSize: '11px', color: '#888', marginTop: '5px'}}>
                                                {(Math.random() * 5 + 0.5).toFixed(1)} km
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </>
            );
        }

        function CalendarScreen({ compromissos, onAddAppointment, onEditAppointment }) {
            const agrupadosPorData = {};
            compromissos.forEach(c => {
                if (!agrupadosPorData[c.data]) {
                    agrupadosPorData[c.data] = [];
                }
                agrupadosPorData[c.data].push(c);
            });

            return (
                <>
                    <div className="header">
                        <h2 style={{margin: 0, fontSize: '24px', fontWeight: 'bold'}}>Agenda Semanal</h2>
                        <p style={{margin: '5px 0 0 0', opacity: 0.9, fontSize: '13px'}}>Semana de 20 a 24 de Outubro</p>
                    </div>

                    <div className="ai-suggestion" style={{margin: '15px'}}>
                        <div style={{display: 'flex', alignItems: 'center', marginBottom: '8px'}}>
                            <Icons.Brain />
                            <strong style={{marginLeft: '8px', fontSize: '14px'}}>Otimização da Semana</strong>
                        </div>
                        <p style={{margin: 0, fontSize: '13px'}}>
                            Quarta-feira tem baixa taxa de conversão no histórico. Recomendo focar em follow-ups por WhatsApp e agendar visitas presenciais para quinta.
                        </p>
                    </div>

                    <div style={{padding: '15px', paddingBottom: '100px'}}>
                        <button className="btn-primary" onClick={onAddAppointment} style={{width: '100%', marginBottom: '20px'}}>
                            + Adicionar Compromisso
                        </button>

                        {Object.keys(agrupadosPorData).sort().map((data, idx) => (
                            <div key={idx} className="calendar-day" style={{marginBottom: '15px'}}>
                                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px'}}>
                                    <strong style={{fontSize: '15px'}}>
                                        {new Date(data + 'T00:00:00').toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: '2-digit' })}
                                    </strong>
                                    <span style={{fontSize: '12px', color: '#667eea', fontWeight: '600'}}>
                                        {agrupadosPorData[data].length} {agrupadosPorData[data].length === 1 ? 'compromisso' : 'compromissos'}
                                    </span>
                                </div>
                                {agrupadosPorData[data].map((compromisso, i) => (
                                    <div 
                                        key={i} 
                                        onClick={() => onEditAppointment(compromisso)}
                                        style={{
                                            background: '#f9fafb',
                                            padding: '12px',
                                            borderRadius: '8px',
                                            marginTop: '8px',
                                            fontSize: '13px',
                                            borderLeft: '3px solid #667eea',
                                            cursor: 'pointer',
                                            transition: 'background 0.2s'
                                        }}
                                        onMouseEnter={(e) => e.currentTarget.style.background = '#f3f4f6'}
                                        onMouseLeave={(e) => e.currentTarget.style.background = '#f9fafb'}
                                    >
                                        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                                            <strong>{compromisso.hora} - {compromisso.cliente}</strong>
                                            <Icons.Edit />
                                        </div>
                                        {compromisso.observacoes && (
                                            <div style={{fontSize: '11px', color: '#666', marginTop: '5px'}}>
                                                {compromisso.observacoes}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        ))}

                        <div style={{marginTop: '25px', padding: '15px', background: 'white', borderRadius: '12px', border: '1px solid #e5e7eb'}}>
                            <h3 style={{fontSize: '16px', fontWeight: '600', marginBottom: '12px'}}>Configurações</h3>
                            <div style={{fontSize: '13px', color: '#666', lineHeight: '1.8'}}>
                                ⏱️ Tempo médio por visita: 45 min<br/>
                                🚗 Tempo de deslocamento: 30 min<br/>
                                🍽️ Intervalo de almoço: 12:00 - 13:30<br/>
                                📱 Notificações: 15 min antes
                            </div>
                        </div>
                    </div>
                </>
            );
        }

        function GoalsScreen() {
            return (
                <>
                    <div className="header">
                        <h2 style={{margin: 0, fontSize: '24px', fontWeight: 'bold'}}>Metas & Performance</h2>
                        <p style={{margin: '5px 0 0 0', opacity: 0.9, fontSize: '13px'}}>Outubro 2025</p>
                    </div>

                    <div style={{padding: '15px', paddingBottom: '100px'}}>
                        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '20px'}}>
                            <div className="metric-card">
                                <div style={{fontSize: '32px', fontWeight: 'bold', color: '#667eea'}}>87%</div>
                                <div style={{fontSize: '12px', color: '#666', marginTop: '5px'}}>Meta de Vendas</div>
                                <div style={{width: '100%', height: '4px', background: '#e5e7eb', borderRadius: '2px', marginTop: '8px'}}>
                                    <div style={{width: '87%', height: '100%', background: '#667eea', borderRadius: '2px'}}></div>
                                </div>
                            </div>
                            <div className="metric-card">
                                <div style={{fontSize: '32px', fontWeight: 'bold', color: '#10b981'}}>24/30</div>
                                <div style={{fontSize: '12px', color: '#666', marginTop: '5px'}}>Clientes Ativos</div>
                                <div style={{width: '100%', height: '4px', background: '#e5e7eb', borderRadius: '2px', marginTop: '8px'}}>
                                    <div style={{width: '80%', height: '100%', background: '#10b981', borderRadius: '2px'}}></div>
                                </div>
                            </div>
                            <div className="metric-card">
                                <div style={{fontSize: '32px', fontWeight: 'bold', color: '#f59e0b'}}>8/12</div>
                                <div style={{fontSize: '12px', color: '#666', marginTop: '5px'}}>Cidades Visitadas</div>
                                <div style={{width: '100%', height: '4px', background: '#e5e7eb', borderRadius: '2px', marginTop: '8px'}}>
                                    <div style={{width: '67%', height: '100%', background: '#f59e0b', borderRadius: '2px'}}></div>
                                </div>
                            </div>
                            <div className="metric-card">
                                <div style={{fontSize: '32px', fontWeight: 'bold', color: '#8b5cf6'}}>R$ 180k</div>
                                <div style={{fontSize: '12px', color: '#666', marginTop: '5px'}}>Faturamento</div>
                                <div style={{fontSize: '10px', color: '#10b981', marginTop: '5px'}}>+15% vs mês anterior</div>
                            </div>
                        </div>

                        <div className="ai-suggestion">
                            <div style={{display: 'flex', alignItems: 'center', marginBottom: '10px'}}>
                                <Icons.Brain />
                                <strong style={{marginLeft: '10px'}}>Insights da IA</strong>
                            </div>
                            <div style={{fontSize: '13px', lineHeight: '1.6'}}>
                                <p style={{margin: '0 0 8px 0'}}>
                                    <strong>📊 Análise:</strong> Marca A tem 92% de conversão em Moema vs 65% em outros bairros. Priorize Moema nas próximas semanas.
                                </p>
                                <p style={{margin: '0 0 8px 0'}}>
                                    <strong>🎯 Recomendação:</strong> Clientes ausentes há 3+ meses têm 45% de chance de reativação com desconto de 8-10%.
                                </p>
                                <p style={{margin: 0}}>
                                    <strong>📈 Previsão:</strong> Com o ritmo atual, você atingirá 95% da meta até dia 28.
                                </p>
                            </div>
                        </div>

                        <h3 style={{fontSize: '18px', fontWeight: '600', margin: '20px 0 15px 0'}}>Performance por Marca</h3>
                        {['Marca A', 'Marca B', 'Marca C'].map((marca, idx) => {
                            const percentuais = [92, 78, 65];
                            const colors = ['#10b981', '#667eea', '#f59e0b'];
                            return (
                                <div key={idx} style={{
                                    background: 'white',
                                    padding: '15px',
                                    borderRadius: '12px',
                                    marginBottom: '10px',
                                    boxShadow: '0 1px 4px rgba(0,0,0,0.1)'
                                }}>
                                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px'}}>
                                        <strong style={{fontSize: '14px'}}>{marca}</strong>
                                        <span style={{fontSize: '14px', color: colors[idx], fontWeight: '600'}}>
                                            {percentuais[idx]}%
                                        </span>
                                    </div>
                                    <div style={{width: '100%', height: '6px', background: '#e5e7eb', borderRadius: '3px'}}>
                                        <div style={{
                                            width: `${percentuais[idx]}%`,
                                            height: '100%',
                                            background: colors[idx],
                                            borderRadius: '3px'
                                        }}></div>
                                    </div>
                                </div>
                            );
                        })}

                        <h3 style={{fontSize: '18px', fontWeight: '600', margin: '20px 0 15px 0'}}>Performance por Região</h3>
                        <div style={{background: 'white', padding: '15px', borderRadius: '12px', boxShadow: '0 1px 4px rgba(0,0,0,0.1)'}}>
                            <div style={{fontSize: '13px', lineHeight: '2'}}>
                                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                    <span>Jardins</span>
                                    <strong style={{color: '#10b981'}}>R$ 65k</strong>
                                </div>
                                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                    <span>Vila Madalena</span>
                                    <strong style={{color: '#667eea'}}>R$ 52k</strong>
                                </div>
                                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                    <span>Moema</span>
                                    <strong style={{color: '#f59e0b'}}>R$ 48k</strong>
                                </div>
                                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                    <span>Outros</span>
                                    <strong style={{color: '#888'}}>R$ 15k</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </>
            );
        }

        ReactDOM.render(<App />, document.getElementById('root'));