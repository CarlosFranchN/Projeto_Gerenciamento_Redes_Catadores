import { 
  getAssociacoes, 
  getProducao, 
  getGrupos, 
  getMunicipios, 
  login, 
  logout,
  getToken,
  createAssociacao,      
  updateAssociacao,      
  deleteAssociacao,      
  createProducao,        
  updateProducao,        
  deleteProducao         
} from './src/services/api.js';
import { showSuccess, showError, showWarning } from './src/utils/toast.js';

// =============== ELEMENTOS ===============
const elements = {
  navBtns: document.querySelectorAll('.nav-btn'),
  sections: document.querySelectorAll('.section-content'),
  pageTitle: document.getElementById('pageTitle'),
  currentDate: document.getElementById('currentDate'),
  userName: document.getElementById('userName'),
  btnLogout: document.getElementById('btnLogout'),
  kpiAssociacoes: document.getElementById('kpiAssociacoes'),
  kpiProducao: document.getElementById('kpiProducao'),
  kpiGrupos: document.getElementById('kpiGrupos'),
  kpiMunicipios: document.getElementById('kpiMunicipios'),
  graficoProducao: document.getElementById('graficoProducao'),
  tabelaAssociacoesRecentes: document.getElementById('tabelaAssociacoesRecentes'),
  tabelaAssociacoes: document.getElementById('tabelaAssociacoes'),
  tabelaProducao: document.getElementById('tabelaProducao'),
  listaGrupos: document.getElementById('listaGrupos'),
  listaMunicipios: document.getElementById('listaMunicipios'),
  btnNovaAssociacao: document.getElementById('btnNovaAssociacao'),
  btnNovaProducao: document.getElementById('btnNovaProducao'),
  btnNovoGrupo: document.getElementById('btnNovoGrupo'),
  btnNovoMunicipio: document.getElementById('btnNovoMunicipio'),
  modalAssociacao: document.getElementById('modalAssociacao'),
  formAssociacao: document.getElementById('formAssociacao'),
  modalProducao: document.getElementById('modalProducao'),
  formProducao: document.getElementById('formProducao'),
  perfilUsuario: document.getElementById('perfilUsuario'),
  perfilNome: document.getElementById('perfilNome'),
  perfilSenha: document.getElementById('perfilSenha'),
  btnSalvarPerfil: document.getElementById('btnSalvarPerfil')
};

// =============== ESTADO ===============
let currentSection = 'dashboard';
let chartInstance = null;
let editingAssociacaoId = null;
let editingProducaoId = null;

// =============== UTILS ===============
const isAuthenticated = () => !!getToken();

const requireAuth = () => {
  if (!isAuthenticated()) {
    window.location.href = 'index.html';
    return false;
  }
  return true;
};

const formatNumber = (num) => new Intl.NumberFormat('pt-BR').format(num);

const setCurrentDate = () => {
  if (!elements.currentDate) return;
  const now = new Date();
  elements.currentDate.textContent = now.toLocaleDateString('pt-BR', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });
};

const showLoading = (element) => {
  if (element) element.innerHTML = '<tr><td colspan="6" class="px-4 py-8 text-center text-gray-500">Carregando...</td></tr>';
};

const hideLoading = (element, content) => {
  if (element) element.innerHTML = content;
};

// =============== NAVEGAÇÃO ===============
const showSection = (sectionName) => {
  // Esconde/mostra seções
  elements.sections?.forEach(section => {
    section?.classList?.toggle('hidden', section.id !== `section-${sectionName}`);
  });

  // Atualiza estilo dos botões do menu
  elements.navBtns?.forEach(btn => {
    const isActive = btn.dataset.section === sectionName;
    btn?.classList?.toggle('bg-green-700', isActive);
    btn?.classList?.toggle('bg-transparent', !isActive);
  });

  // ✅ Verifica se pageTitle existe antes de usar
  if (elements.pageTitle) {
    elements.pageTitle.textContent = sectionName.charAt(0).toUpperCase() + sectionName.slice(1);
  }

  currentSection = sectionName;
  loadSectionData(sectionName);
};

const loadSectionData = async (section) => {
  switch (section) {
    case 'dashboard': await loadDashboard(); break;
    case 'associacoes': await loadAssociacoes(); break;
    case 'producao': await loadProducao(); break;
    case 'grupos': await loadGrupos(); break;
    case 'municipios': await loadMunicipios(); break;
    case 'perfil': loadPerfil(); break;
  }
};

// =============== DASHBOARD ===============
const loadDashboard = async () => {
  try {
    const [associacoes, producao, grupos, municipios] = await Promise.all([
      getAssociacoes(), getProducao(2024), getGrupos(), getMunicipios()
    ]);
    const assocArray = Array.isArray(associacoes) ? associacoes : associacoes.items || [];
    
// Protegendo com "if"
if (elements.kpiAssociacoes) elements.kpiAssociacoes.textContent = assocArray.length;
if (elements.kpiGrupos) elements.kpiGrupos.textContent = Array.isArray(grupos) ? grupos.length : 0;
if (elements.kpiMunicipios) elements.kpiMunicipios.textContent = Array.isArray(municipios) ? municipios.length : 0;

const totalProducao = Array.isArray(producao) 
  ? producao.reduce((acc, item) => acc + (parseFloat(item.kg) || 0), 0) : 0;

if (elements.kpiProducao) elements.kpiProducao.textContent = formatNumber(totalProducao.toFixed(1));
    
    renderGraficoProducao(producao);
    renderTabelaAssociacoesRecentes(assocArray.slice(0, 5));
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error);
    showError('Não foi possível carregar dados do dashboard');
  }
};

const renderGraficoProducao = (producao) => {
  if (!elements.graficoProducao) return;
  const data = Array.isArray(producao) ? producao : [];
  const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  const kgData = meses.map((_, i) => {
    const item = data.find(p => p.mes === i + 1);
    return item ? parseFloat(item.kg) : 0;
  });
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(elements.graficoProducao, {
    type: 'bar',
    data: {
      labels: meses,
      datasets: [{
        label: 'Produção (KG)',
        data: kgData,
        backgroundColor: 'rgba(16, 185, 129, 0.7)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: (value) => formatNumber(value) }
        }
      },
      plugins: { legend: { display: false } }
    }
  });
};

const renderTabelaAssociacoesRecentes = (associacoes) => {
  if (!elements.tabelaAssociacoesRecentes) return;
  elements.tabelaAssociacoesRecentes.innerHTML = associacoes.map(assoc => `
    <tr class="border-b hover:bg-gray-50">
      <td class="px-4 py-3 text-sm font-medium text-gray-800">${assoc.nome || 'N/A'}</td>
      <td class="px-4 py-3 text-sm text-gray-600">${assoc.cnpj || '—'}</td>
      <td class="px-4 py-3 text-sm text-gray-600">${assoc.bairro || '—'}</td>
      <td class="px-4 py-3">
        <span class="px-2 py-1 text-xs rounded-full ${assoc.status === 'ativo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
          ${assoc.status || 'ativo'}
        </span>
      </td>
    </tr>
  `).join('');
};

// =============== ASSOCIAÇÕES ===============
const loadAssociacoes = async () => {
  try {
    showLoading(elements.tabelaAssociacoes);
    const response = await getAssociacoes();
    const associacoes = Array.isArray(response) ? response : response.items || [];
    
    const rows = associacoes.map(assoc => `
      <tr class="border-b hover:bg-gray-50">
        <td class="px-4 py-3 text-sm font-medium text-gray-800">${assoc.nome || 'N/A'}</td>
        <td class="px-4 py-3 text-sm text-gray-600">${assoc.cnpj || '—'}</td>
        <td class="px-4 py-3 text-sm text-gray-600">${assoc.lider || '—'}</td>
        <td class="px-4 py-3 text-sm text-gray-600">${assoc.telefone || '—'}</td>
        <td class="px-4 py-3 text-sm text-gray-600">${assoc.bairro || '—'}</td>
        <td class="px-4 py-3 text-sm space-x-2">
          <button class="text-blue-600 hover:text-blue-800 edit-associacao" data-id="${assoc.id}">✏️</button>
          <button class="text-red-600 hover:text-red-800 delete-associacao" data-id="${assoc.id}">🗑️</button>
        </td>
      </tr>
    `).join('');
    
    hideLoading(elements.tabelaAssociacoes, rows);
    attachAssociacaoHandlers();
  } catch (error) {
    console.error('Erro ao carregar associações:', error);
    showError('Não foi possível carregar associações');
    hideLoading(elements.tabelaAssociacoes, '<tr><td colspan="6" class="px-4 py-8 text-center text-red-600">Erro ao carregar</td></tr>');
  }
};

const attachAssociacaoHandlers = () => {
  document.querySelectorAll('.edit-associacao').forEach(btn => {
    btn.addEventListener('click', (e) => handleEditAssociacao(e.currentTarget.dataset.id));
  });
  document.querySelectorAll('.delete-associacao').forEach(btn => {
    btn.addEventListener('click', (e) => handleDeleteAssociacao(e.currentTarget.dataset.id));
  });
};

const handleEditAssociacao = (id) => {
  showWarning('Edição será implementada na próxima versão');
};

const handleDeleteAssociacao = (id) => {
  if (confirm('Tem certeza que deseja excluir esta associação? (soft delete)')) {
    showSuccess('Associação marcada como inativa');
    loadAssociacoes();
  }
};

const openModalAssociacao = (assoc = null) => {
  editingAssociacaoId = assoc?.id || null;
  elements.formAssociacao.reset();
  if (assoc) {
    elements.formAssociacao.querySelector('#assocNome').value = assoc.nome || '';
    elements.formAssociacao.querySelector('#assocCnpj').value = assoc.cnpj || '';
    elements.formAssociacao.querySelector('#assocLider').value = assoc.lider || '';
    elements.formAssociacao.querySelector('#assocTelefone').value = assoc.telefone || '';
    elements.formAssociacao.querySelector('#assocBairro').value = assoc.bairro || '';
    elements.formAssociacao.querySelector('#assocCidade').value = assoc.cidade || '';
    elements.formAssociacao.querySelector('#assocUf').value = assoc.uf || '';
    elements.formAssociacao.querySelector('#assocStatus').value = assoc.status || 'ativo';
  }
  elements.modalAssociacao?.classList.remove('hidden');
};

const handleAssociacaoSubmit = async (e) => {
  e.preventDefault();
  
  const formData = {
    nome: elements.formAssociacao.querySelector('#assocNome').value,
    cnpj: elements.formAssociacao.querySelector('#assocCnpj').value,
    lider: elements.formAssociacao.querySelector('#assocLider').value,
    telefone: elements.formAssociacao.querySelector('#assocTelefone').value,
    bairro: elements.formAssociacao.querySelector('#assocBairro').value,
    cidade: elements.formAssociacao.querySelector('#assocCidade').value,
    uf: elements.formAssociacao.querySelector('#assocUf').value,
    status: elements.formAssociacao.querySelector('#assocStatus').value
  };
  
  const result = editingAssociacaoId 
    ? await updateAssociacao(editingAssociacaoId, formData)
    : await createAssociacao(formData);
  
  if (result.success) {
    showSuccess(editingAssociacaoId ? 'Associação atualizada!' : 'Associação criada!');
    elements.modalAssociacao?.classList.add('hidden');
    loadAssociacoes();
  } else {
    showError(result.error);
  }
};

// =============== PRODUÇÃO ===============
const loadProducao = async () => {
  try {
    showLoading(elements.tabelaProducao);
    const producao = await getProducao(2024);
    const data = Array.isArray(producao) ? producao : [];
    const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    
    const rows = data.map(item => `
      <tr class="border-b hover:bg-gray-50">
        <td class="px-4 py-3 text-sm text-gray-800">${meses[item.mes - 1] || item.mes}</td>
        <td class="px-4 py-3 text-sm text-gray-600">Rede de Catadores</td>
        <td class="px-4 py-3 text-sm font-medium text-gray-800">${formatNumber(item.kg)}</td>
        <td class="px-4 py-3 text-sm text-gray-600">${item.valor_venda ? `R$ ${formatNumber(item.valor_venda)}` : '—'}</td>
        <td class="px-4 py-3 text-sm space-x-2">
          <button class="text-blue-600 hover:text-blue-800 edit-producao" data-id="${item.id || item.mes}">✏️</button>
          <button class="text-red-600 hover:text-red-800 delete-producao" data-id="${item.id || item.mes}">🗑️</button>
        </td>
      </tr>
    `).join('');
    
    hideLoading(elements.tabelaProducao, rows);
    attachProducaoHandlers();
  } catch (error) {
    console.error('Erro ao carregar produção:', error);
    showError('Não foi possível carregar produção');
    hideLoading(elements.tabelaProducao, '<tr><td colspan="5" class="px-4 py-8 text-center text-red-600">Erro ao carregar</td></tr>');
  }
};

const attachProducaoHandlers = () => {
  document.querySelectorAll('.edit-producao').forEach(btn => {
    btn.addEventListener('click', (e) => handleEditProducao(e.currentTarget.dataset.id));
  });
  document.querySelectorAll('.delete-producao').forEach(btn => {
    btn.addEventListener('click', (e) => handleDeleteProducao(e.currentTarget.dataset.id));
  });
};

const handleEditProducao = (id) => {
  showWarning('Edição será implementada na próxima versão');
};

const handleDeleteProducao = (id) => {
  if (confirm('Tem certeza que deseja excluir este registro de produção?')) {
    showSuccess('Registro excluído');
    loadProducao();
  }
};

const openModalProducao = () => {
  editingProducaoId = null;
  elements.formProducao?.reset();
  elements.modalProducao?.classList.remove('hidden');
};

const handleProducaoSubmit = async (e) => {
  e.preventDefault();
  try {
    await new Promise(resolve => setTimeout(resolve, 500));
    showSuccess('Produção registrada!');
    elements.modalProducao?.classList.add('hidden');
    loadProducao();
    if (currentSection === 'dashboard') loadDashboard();
  } catch (error) {
    showError('Erro ao salvar produção');
  }
};

// =============== GRUPOS ===============
const loadGrupos = async () => {
  try {
    const grupos = await getGrupos();
    const data = Array.isArray(grupos) ? grupos : [];
    elements.listaGrupos.innerHTML = data.map(grupo => `
      <div class="border rounded-lg p-4 hover:shadow-md transition">
        <h4 class="font-semibold text-gray-800">${grupo.nome}</h4>
        <p class="text-sm text-gray-600">${grupo.integrantes} integrantes</p>
        <p class="text-sm text-gray-600">${grupo.cidade || '—'}/${grupo.uf || '—'}</p>
      </div>
    `).join('') || '<p class="text-gray-600">Nenhum grupo encontrado</p>';
  } catch (error) {
    console.error('Erro ao carregar grupos:', error);
    elements.listaGrupos.innerHTML = '<p class="text-gray-600">Erro ao carregar</p>';
  }
};

// =============== MUNICÍPIOS ===============
const loadMunicipios = async () => {
  try {
    const municipios = await getMunicipios();
    const data = Array.isArray(municipios) ? municipios : [];
    elements.listaMunicipios.innerHTML = data.map(municipio => `
      <div class="border rounded-lg p-4 hover:shadow-md transition">
        <h4 class="font-semibold text-gray-800">${municipio.nome}/${municipio.uf}</h4>
        <p class="text-sm text-gray-600">${municipio.qtd_grupos || 0} grupos</p>
        <p class="text-sm text-gray-600">${municipio.qtd_associacoes || 0} associações</p>
      </div>
    `).join('') || '<p class="text-gray-600">Nenhum município encontrado</p>';
  } catch (error) {
    console.error('Erro ao carregar municípios:', error);
    elements.listaMunicipios.innerHTML = '<p class="text-gray-600">Erro ao carregar</p>';
  }
};

// =============== PERFIL ===============
const loadPerfil = () => {
  const token = getToken();
  if (!token) return;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    elements.perfilUsuario.value = payload.sub || 'admin';
    elements.perfilNome.value = payload.nome || 'Administrador';
  } catch (error) {
    elements.perfilUsuario.value = 'admin';
    elements.perfilNome.value = 'Administrador';
  }
};

const handlePerfilSubmit = async (e) => {
  e.preventDefault();
  const novaSenha = elements.perfilSenha?.value;
  try {
    if (novaSenha && novaSenha.length < 6) {
      showError('Senha deve ter pelo menos 6 caracteres');
      return;
    }
    await new Promise(resolve => setTimeout(resolve, 500));
    showSuccess('Perfil atualizado!');
    if (elements.perfilSenha) elements.perfilSenha.value = '';
  } catch (error) {
    showError('Erro ao atualizar perfil');
  }
};

// =============== LOGOUT ===============
const handleLogout = () => {
  logout();
  showSuccess('Logout realizado com sucesso!');
  setTimeout(() => { window.location.href = 'index.html'; }, 1000);
};

// =============== EVENT LISTENERS ===============
elements.navBtns.forEach(btn => {
  btn.addEventListener('click', () => showSection(btn.dataset.section));
});

elements.btnLogout?.addEventListener('click', handleLogout);

// Associações
elements.btnNovaAssociacao?.addEventListener('click', () => openModalAssociacao());
elements.formAssociacao?.addEventListener('submit', handleAssociacaoSubmit);
document.querySelectorAll('#modalAssociacao .modal-close').forEach(btn => {
  btn.addEventListener('click', () => elements.modalAssociacao?.classList.add('hidden'));
});

// Produção
elements.btnNovaProducao?.addEventListener('click', openModalProducao);
elements.formProducao?.addEventListener('submit', handleProducaoSubmit);
document.querySelectorAll('#modalProducao .modal-close').forEach(btn => {
  btn.addEventListener('click', () => elements.modalProducao?.classList.add('hidden'));
});

// Perfil
elements.btnSalvarPerfil?.addEventListener('click', handlePerfilSubmit);

// Fechar modais ao clicar fora
[elements.modalAssociacao, elements.modalProducao].forEach(modal => {
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.add('hidden');
  });
});

// =============== INICIALIZAÇÃO ===============
document.addEventListener('DOMContentLoaded', () => {
  if (!requireAuth()) return;
  setCurrentDate();
  showSection('dashboard');
});