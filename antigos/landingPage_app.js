import {
  renderAssociacoes,
  renderProducao,
  renderGrupos,
  renderMunicipios,
  closeAssocDetail,
  openAssocDetailFromCard 
} from './scripts/render.js';

import { setToken, removeToken, login } from './services/api.js';
import { validateLogin, validateContactForm } from './utils/index.js';
import { showSuccess, showError, showWarning } from './utils/toast.js';

// =============== REFERÊNCIAS DOS ELEMENTOS ===============
const modalLogin = document.getElementById('modalLogin');
const btnLogin = document.getElementById('btnLogin');
const closeLogin = document.getElementById('closeLogin');
const formLogin = document.getElementById('formLogin');

const modalAfiliados = document.getElementById('modalAfiliados');
const btnAfiliados = document.getElementById('btnAfiliados');
const btnVerAfiliados = document.getElementById('btnVerAfiliados');
const btnFecharAfiliados = document.getElementById('btnFecharAfiliados');

const assocDetail = document.getElementById('assocDetail');
const closeAssocDetailBtn = document.getElementById('closeAssocDetail');
const assocTitleEl = document.getElementById('assocTitle');
const assocLeaderEl = document.getElementById('assocLeader');
const assocPhoneEl = document.getElementById('assocPhone');
const assocAddrEl = document.getElementById('assocAddress');
const assocCNPJEl = document.getElementById('assocCNPJ');

const formContato = document.getElementById('formContato');

const tabBtns = document.querySelectorAll('.tab-btn');
const panes = document.querySelectorAll('.tab-pane');

// Debug
console.log('🔍 Debug Elementos:', {
  modalLogin: !!modalLogin,
  modalAfiliados: !!modalAfiliados,
  assocDetail: !!assocDetail,
  btnAfiliados: !!btnAfiliados,
  btnVerAfiliados: !!btnVerAfiliados
});

// =============== INICIALIZAÇÃO ===============
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Iniciando aplicação...');
  renderAssociacoes();
  renderProducao();
  renderGrupos();
  renderMunicipios();
});

// =============== FUNÇÃO: enhanceClickableCard ===============
// (Estava faltando! Era do código inline antigo)
function enhanceClickableCard(card, onActivate) {
  card.classList.add(
    'clickable-card',
    'cursor-pointer',
    'transition',
    'hover:-translate-y-0.5',
    'active:translate-y-0',
    'hover:border-green-200',
    'hover:shadow-md',
    'shadow-sm',
    'bg-white',
    'focus-visible:ring-2',
    'focus-visible:ring-green-600/50',
    'ring-offset-2',
    'ring-offset-white'
  );
  card.setAttribute('role', 'button');
  card.setAttribute('tabindex', '0');
  
  const press = (x, y) => {
    card.style.setProperty('--x', x + 'px');
    card.style.setProperty('--y', y + 'px');
    card.classList.add('is-pressed');
    setTimeout(() => card.classList.remove('is-pressed'), 220);
  };
  
  card.addEventListener('mousedown', (e) => {
    const r = card.getBoundingClientRect();
    press(e.clientX - r.left, e.clientY - r.top);
  });
  
  card.addEventListener('click', () => onActivate && onActivate());
  
  card.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      const r = card.getBoundingClientRect();
      press(r.width / 2, r.height / 2);
      onActivate && onActivate();
    }
  });
}



// =============== LOGIN ===============
btnLogin?.addEventListener('click', () => {
  if (modalLogin) {
    modalLogin.classList.remove('hidden');
    document.getElementById('loginUser')?.focus();
  } else {
    showError('Modal de login não encontrado');
  }
});

closeLogin?.addEventListener('click', () => modalLogin?.classList.add('hidden'));

modalLogin?.addEventListener('click', (e) => {
  if (e.target === modalLogin) modalLogin.classList.add('hidden');
});

formLogin?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('loginUser')?.value || '';
  const password = document.getElementById('loginPass')?.value || '';
  
  const validation = validateLogin(username, password);
  if (!validation.valid) {
    showError(Object.values(validation.errors)[0]);
    return;
  }

  const btn = formLogin.querySelector('button[type="submit"]');
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
});

// =============== MODAL AFILIADOS ===============
function openAfiliados() {
  console.log('📂 Abrindo modal afiliados');
  modalAfiliados?.classList.remove('hidden');
}

function closeAfiliados() {
  modalAfiliados?.classList.add('hidden');
}

btnAfiliados?.addEventListener('click', openAfiliados);
btnVerAfiliados?.addEventListener('click', openAfiliados);
btnFecharAfiliados?.addEventListener('click', closeAfiliados);

modalAfiliados?.addEventListener('click', (e) => {
  if (e.target === modalAfiliados) closeAfiliados();
});

// =============== WIRE AFILIADOS CLICK ===============
(function wireAfiliadosClick() {
  const paneAssoc = document.getElementById('tab-associacoes');
  if (!paneAssoc) return;
  
  const cards = paneAssoc.querySelectorAll('.rounded-xl.border.p-3');
  
  cards.forEach((card) => {
    const nameEl = card.querySelector('.font-semibold');
    if (!nameEl) return;
    
    const nome = nameEl.textContent.trim();
    const infoEl = card.querySelector('.text-sm.text-gray-600');
    const infoTexto = infoEl ? infoEl.textContent.trim() : '';
    const [cnpj, bairro] = infoTexto.split(' — ');
    
    card.dataset.nome = nome;
    card.dataset.cnpj = cnpj || '—';
    card.dataset.bairro = bairro || '—';
    
    enhanceClickableCard(card, () => {
      tabBtns.forEach((b) => {
        const isAssoc = b.getAttribute('data-tab') === 'tab-associacoes';
        b.classList.toggle('bg-green-600', isAssoc);
        b.classList.toggle('text-white', isAssoc);
        b.classList.toggle('bg-white', !isAssoc);
      });
      panes.forEach((p) => p.classList.toggle('hidden', p.id !== 'tab-associacoes'));
      
      openAssocDetailFromCard(card);
    });
  });
})();

// =============== WIRE GRID REDE ===============
(function wireGridRede() {
  const grid =
    document.querySelector('#rede .grid.sm\\:grid-cols-2') ||
    document.querySelector('#rede .grid');
  if (!grid) return;
  
  const tiles = grid.querySelectorAll('.rounded-xl.border.bg-white.p-4');
  
  tiles.forEach((tile) => {
    const nameEl = tile.querySelector('.font-semibold');
    if (!nameEl) return;
    
    const infoEl = tile.querySelector('.text-sm.text-gray-600');
    const infoTexto = infoEl ? infoEl.textContent.trim() : '';
    const [cnpj, bairro] = infoTexto.split(' — ');
    
    tile.dataset.nome = nameEl.textContent.trim();
    tile.dataset.cnpj = cnpj || '—';
    tile.dataset.bairro = bairro || '—';
    
    enhanceClickableCard(tile, () => {
      openAfiliados();
      setTimeout(() => openAssocDetailFromCard(tile), 80);
    });
  });
})();

// =============== TABS DO MODAL ===============
tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.getAttribute('data-tab');
    tabBtns.forEach(b => {
      const isActive = b === btn;
      b.classList.toggle('bg-green-600', isActive);
      b.classList.toggle('text-white', isActive);
      b.classList.toggle('bg-white', !isActive);
    });
    panes.forEach(p => p.classList.toggle('hidden', p.id !== id));
  });
});

// =============== CONTATO ===============
formContato?.addEventListener('submit', (e) => {
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
  formContato.reset();
});

// =============== DETALHE ASSOCIAÇÃO ===============


closeAssocDetailBtn?.addEventListener('click', closeAssocDetail);

assocDetail?.addEventListener('click', (e) => {
  if (e.target === assocDetail) closeAssocDetail();
});

// ✅ Tecla ESC
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeAssocDetail();
    closeAfiliados();
    modalLogin?.classList.add('hidden');
  }
});