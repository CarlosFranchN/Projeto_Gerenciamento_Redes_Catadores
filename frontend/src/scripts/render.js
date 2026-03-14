// frontend/src/scripts/render.js

import {
  getAssociacoes,
  getProducao,
  getGrupos,
  getMunicipios
} from '../services/api.js';

import {
  formatCurrency,
  formatNumber,
  formatCNPJ,
  formatPhone,
  showLoading,
  hideLoading,
  setContent,
  clearContent
} from '../utils/index.js';

// =============== ASSOCIAÇÕES ===============
export async function renderAssociacoes() {
  const gridRede = document.querySelector('#rede .grid.sm\\:grid-cols-2');
  const modalAssoc = document.getElementById('tab-associacoes');
  
  if (gridRede) showLoading(gridRede, 'grid');
  if (modalAssoc) showLoading(modalAssoc, 'grid');
  
  try {
    const associacoes = await getAssociacoes();
    
    const html = associacoes.map(assoc => `
      <div class="rounded-xl border bg-white p-4 clickable-card cursor-pointer transition hover:-translate-y-0.5 hover:border-green-200 hover:shadow-md shadow-sm focus-visible:ring-2 focus-visible:ring-green-600/50 ring-offset-2"
           tabindex="0"
           data-nome="${assoc.nome}">
        <div class="font-semibold text-green-700">${assoc.nome}</div>
        <div class="text-sm text-gray-600">
          ${formatCNPJ(assoc.cnpj)} — ${assoc.bairro || '—'}
        </div>
      </div>
    `).join('');
    
    if (gridRede) setContent(gridRede, html);
    if (modalAssoc) setContent(modalAssoc, html);
    
    wireCardClicks();
    
  } catch (error) {
    console.error('Erro ao renderizar associações:', error);
    if (gridRede) hideLoading(gridRede);
    if (modalAssoc) hideLoading(modalAssoc);
  }
}
// =============== PRODUÇÃO ===============
export async function renderProducao() {
  const tabelaBody = document.querySelector('#tabelaProducao tbody');
  const canvas = document.getElementById('graficoMensal');
  const totalEl = document.getElementById('totalProducao');
  
  if (tabelaBody) {
    // Mostra skeleton no tbody (não na tabela toda)
    tabelaBody.innerHTML = `
      <tr><td colspan="2" class="px-4 py-2">
        <div class="animate-pulse space-y-2">
          <div class="h-4 bg-gray-200 rounded w-3/4"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          <div class="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </td></tr>
    `;
  }
  
  try {
    const producao = await getProducao();
    
    if (!producao || producao.length === 0) {
      throw new Error('Dados de produção vazios');
    }
    
    const total = producao.reduce((acc, item) => acc + item.kg, 0);
    
    // Atualiza total
    if (totalEl) {
      totalEl.textContent = formatNumber(total) + ' kg';
    }
    
    // Renderiza linhas
    const rows = producao.map(item => `
      <tr class="odd:bg-white even:bg-neutral-50">
        <td class="px-4 py-2">${item.mes}</td>
        <td class="px-4 py-2">${formatNumber(item.kg)}</td>
      </tr>
    `).join('');
    
    const totalRow = `
      <tr class="bg-green-50 font-semibold">
        <td class="px-4 py-2">Total</td>
        <td class="px-4 py-2">${formatNumber(total)}</td>
      </tr>
    `;
    
    if (tabelaBody) {
      tabelaBody.innerHTML = rows + totalRow;
    }
    
    // Renderiza gráfico
    if (canvas && window.Chart) {
      renderGrafico(canvas, producao);
    }
    
    console.log('✅ Produção renderizada:', producao.length, 'meses');
    
  } catch (error) {
    console.error('Erro ao renderizar produção:', error);
    showError('Não foi possível carregar a produção');
    if (tabelaBody) {
      tabelaBody.innerHTML = `
        <tr><td colspan="2" class="px-4 py-2 text-center text-red-600">
          Erro ao carregar dados. Atualize a página.
        </td></tr>
      `;
    }
  }
}

function renderGrafico(canvas, producao) {
  const ctx = canvas.getContext('2d');
  
  // Destroi gráfico existente se houver
  const existingChart = Chart.getChart(canvas);
  if (existingChart) {
    existingChart.destroy();
  }
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: producao.map(item => item.mes),
      datasets: [{
        label: 'Kg por mês',
        data: producao.map(item => item.kg),
        borderWidth: 1,
        borderRadius: 8,
        backgroundColor: 'rgba(16, 185, 129, 0.6)',
        borderColor: 'rgba(16, 185, 129, 1)',
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => formatNumber(ctx.parsed.y) + ' kg',
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(0,0,0,0.06)' },
          ticks: {
            callback: (v) => formatNumber(v) + ' kg',
          },
        },
        x: { grid: { display: false } },
      },
    },
  });
}

// =============== GRUPOS ===============
export async function renderGrupos() {
  const modalGrupos = document.getElementById('tab-grupos');
  
  if (modalGrupos) showLoading(modalGrupos, 'grid');
  
  try {
    const grupos = await getGrupos();
    
    const html = grupos.map(grupo => `
      <div class="rounded-xl border p-3">
        <div class="font-semibold text-green-700">${grupo.nome}</div>
        <div class="text-sm text-gray-600">${grupo.integrantes} integrantes</div>
      </div>
    `).join('');
    
    if (modalGrupos) setContent(modalGrupos, html);
    
  } catch (error) {
    console.error('Erro ao renderizar grupos:', error);
    if (modalGrupos) hideLoading(modalGrupos);
  }
}

// =============== MUNICÍPIOS ===============
export async function renderMunicipios() {
  const modalMunicipios = document.getElementById('tab-municipios');
  
  if (modalMunicipios) showLoading(modalMunicipios, 'grid');
  
  try {
    const municipios = await getMunicipios();
    
    const html = municipios.map(municipio => `
      <div class="rounded-xl border p-3">
        <div class="font-semibold text-green-700">${municipio.nome}</div>
        <div class="text-sm text-gray-600">${municipio.grupos} grupos/associações</div>
      </div>
    `).join('');
    
    if (modalMunicipios) setContent(modalMunicipios, html);
    
  } catch (error) {
    console.error('Erro ao renderizar municípios:', error);
    if (modalMunicipios) hideLoading(modalMunicipios);
  }
}

// =============== CLICK NOS CARDS ===============
function wireCardClicks() {
  const cards = document.querySelectorAll('.clickable-card[data-nome]');
  
  cards.forEach(card => {
    card.addEventListener('click', () => {
      const nome = card.dataset.nome;
      openAssocDetailByName(nome);
    });
    
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const nome = card.dataset.nome;
        openAssocDetailByName(nome);
      }
    });
  });
}

// =============== DETALHE DA ASSOCIAÇÃO ===============
export function openAssocDetailByName(nome) {
  const assocDetail = document.getElementById('assocDetail');
  const assocTitleEl = document.getElementById('assocTitle');
  const assocLeaderEl = document.getElementById('assocLeader');
  const assocPhoneEl = document.getElementById('assocPhone');
  const assocAddrEl = document.getElementById('assocAddress');
  const assocCNPJEl = document.getElementById('assocCNPJ');
  
  if (!assocDetail) return;
  
  assocTitleEl.textContent = nome.toUpperCase();
  assocLeaderEl.textContent = '—';
  assocPhoneEl.textContent = '—';
  assocAddrEl.textContent = '—';
  assocCNPJEl.textContent = '—';
  
  assocDetail.classList.remove('hidden');
}

export function closeAssocDetail() {
  const assocDetail = document.getElementById('assocDetail');
  if (assocDetail) {
    assocDetail.classList.add('hidden');
  }
}