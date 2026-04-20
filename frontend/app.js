import {
  renderAssociacoes,
  renderProducao,
  renderGrupos,
  renderMunicipios,
  closeAssocDetail
} from './src/scripts/render.js';

import { login, setToken } from './src/services/api.js';
import { validateLogin, validateContactForm } from './src/utils/index.js';
import { showSuccess, showError } from './src/utils/toast.js';

// =============== ELEMENTOS ===============
const elements = {
  modalLogin: document.getElementById('modalLogin'),
  btnLogin: document.getElementById('btnLogin'),
  closeLogin: document.getElementById('closeLogin'),
  formLogin: document.getElementById('formLogin'),
  modalAfiliados: document.getElementById('modalAfiliados'),
  btnAfiliados: document.getElementById('btnAfiliados'),
  btnVerAfiliados: document.getElementById('btnVerAfiliados'),
  btnFecharAfiliados: document.getElementById('btnFecharAfiliados'),
  assocDetail: document.getElementById('assocDetail'),
  closeAssocDetail: document.getElementById('closeAssocDetail'),
  formContato: document.getElementById('formContato'),
  tabBtns: document.querySelectorAll('.tab-btn'),
  panes: document.querySelectorAll('.tab-pane')
};

// =============== INICIALIZAÇÃO ===============
document.addEventListener('DOMContentLoaded', () => {
  renderAssociacoes();
  renderProducao();
  renderGrupos();
  renderMunicipios();
});

// =============== MODAL UTILS ===============
const toggleModal = (modal, show) => modal?.classList.toggle('hidden', !show);

const closeModalOnClickOutside = (modal, closeFn) => {
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) closeFn();
  });
};

// =============== LOGIN ===============
const openLogin = () => {
  toggleModal(elements.modalLogin, true);
  document.getElementById('loginUser')?.focus();
};

const closeLogin = () => toggleModal(elements.modalLogin, false);

const handleLoginSubmit = async (e) => {
  e.preventDefault();
  
  const username = document.getElementById('loginUser')?.value || '';
  const password = document.getElementById('loginPass')?.value || '';
  
  const validation = validateLogin(username, password);
  if (!validation.valid) {
    showError(Object.values(validation.errors)[0]);
    return;
  }

  const btn = elements.formLogin.querySelector('button[type="submit"]');
  const originalText = btn.innerText;
  btn.innerText = 'Entrando...';
  btn.disabled = true;

  try {
    const result = await login(username, password);
    
    if (!result.success) {
      showError(result.error);
      return;
    }
    
    setToken(result.token);
    showSuccess('Login realizado com sucesso!');
    setTimeout(() => window.location.href = 'app.html', 1000);
  } catch (err) {
    showError(err.message);
  } finally {
    btn.innerText = originalText;
    btn.disabled = false;
  }
};

// =============== AFILIADOS ===============
const openAfiliados = () => toggleModal(elements.modalAfiliados, true);
const closeAfiliados = () => toggleModal(elements.modalAfiliados, false);

// =============== TABS ===============
const handleTabClick = (e) => {
  const id = e.target.getAttribute('data-tab');
  
  elements.tabBtns.forEach(btn => {
    const isActive = btn === e.target;
    btn.classList.toggle('bg-green-600', isActive);
    btn.classList.toggle('text-white', isActive);
    btn.classList.toggle('bg-white', !isActive);
  });
  
  elements.panes.forEach(pane => {
    pane.classList.toggle('hidden', pane.id !== id);
  });
};

// =============== CONTATO ===============
const handleContactSubmit = (e) => {
  e.preventDefault();
  
  const data = {
    name: document.getElementById('contatoNome')?.value || '',
    email: document.getElementById('contatoEmail')?.value || '',
    message: document.getElementById('contatoMensagem')?.value || ''
  };
  
  const validation = validateContactForm(data);
  if (!validation.valid) {
    showError(Object.values(validation.errors)[0]);
    return;
  }
  
  showSuccess('Mensagem enviada! Obrigado pelo contato.');
  elements.formContato.reset();
};

// =============== ESC KEY ===============
const handleEscapeKey = (e) => {
  if (e.key !== 'Escape') return;
  
  closeAssocDetail();
  closeAfiliados();
  closeLogin();
};

// =============== EVENT LISTENERS ===============
elements.btnLogin?.addEventListener('click', openLogin);
elements.closeLogin?.addEventListener('click', closeLogin);
elements.formLogin?.addEventListener('submit', handleLoginSubmit);
closeModalOnClickOutside(elements.modalLogin, closeLogin);

elements.btnAfiliados?.addEventListener('click', openAfiliados);
elements.btnVerAfiliados?.addEventListener('click', openAfiliados);
elements.btnFecharAfiliados?.addEventListener('click', closeAfiliados);
closeModalOnClickOutside(elements.modalAfiliados, closeAfiliados);

elements.closeAssocDetail?.addEventListener('click', closeAssocDetail);
closeModalOnClickOutside(elements.assocDetail, closeAssocDetail);

elements.tabBtns.forEach(btn => btn.addEventListener('click', handleTabClick));
elements.formContato?.addEventListener('submit', handleContactSubmit);

document.addEventListener('keydown', handleEscapeKey);