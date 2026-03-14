// frontend/src/services/api.js

import { 
  ASSOCIACOES, 
  PRODUCAO_MENSAL, 
  GRUPOS, 
  MUNICIPIOS 
} from '../data/index.js';

import { showError, showWarning } from '../utils/toast.js';

const API_URL = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000/'
  : 'https://projeto-gerenciamento-redes-catadores.onrender.com/';

const API_TIMEOUT = 5000;

function withTimeout(promise, ms) {
  return Promise.race([
    promise,
    new Promise((_, reject) => 
      setTimeout(() => reject(new Error('Timeout da API')), ms)
    )
  ]);
}

export async function getAssociacoes() {
  try {
    const response = await withTimeout(
      fetch(`${API_URL}associacoes/?limit=100`),
      API_TIMEOUT
    );
    
    if (!response.ok) {
      throw new Error('API retornou erro');
    }
    
    const data = await response.json();
    console.log('✅ Dados carregados da API');
    return data.items || [];
    
  } catch (error) {
    console.warn('⚠️ API indisponível, usando dados locais:', error.message);
    showWarning('Usando dados locais (API indisponível)');
    return ASSOCIACOES;
  }
}

export async function getProducao(ano = 2024) {
  try {
    const response = await withTimeout(
      fetch(`${API_URL}producao/?ano=${ano}`),
      API_TIMEOUT
    );
    
    if (!response.ok) {
      throw new Error('API retornou erro');
    }
    
    const data = await response.json();
    console.log('✅ Produção carregada da API');
    return data;
    
  } catch (error) {
    console.warn('⚠️ API indisponível, usando produção local:', error.message);
    return PRODUCAO_MENSAL;
  }
}

export async function getGrupos() {
  try {
    const response = await withTimeout(
      fetch(`${API_URL}grupos/`),
      API_TIMEOUT
    );
    
    if (!response.ok) throw new Error('API retornou erro');
    
    const data = await response.json();
    console.log('✅ Grupos carregados da API');
    return data;
    
  } catch (error) {
    console.warn('⚠️ API indisponível, usando grupos locais:', error.message);
    return GRUPOS;
  }
}

export async function getMunicipios() {
  try {
    const response = await withTimeout(
      fetch(`${API_URL}municipios/`),
      API_TIMEOUT
    );
    
    if (!response.ok) throw new Error('API retornou erro');
    
    const data = await response.json();
    console.log('✅ Municípios carregados da API');
    return data;
    
  } catch (error) {
    console.warn('⚠️ API indisponível, usando municípios locais:', error.message);
    return MUNICIPIOS;
  }
}

export async function login(username, password) {
  try {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await fetch(`${API_URL}token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Usuário ou senha incorretos');
    }
    
    const data = await response.json();
    return { success: true, token: data.access_token };
    
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export function getToken() {
  return localStorage.getItem('rc_token');
}

export function setToken(token) {
  localStorage.setItem('rc_token', token);
}

export function removeToken() {
  localStorage.removeItem('rc_token');
}

export async function consultarCNPJ(cnpj) {
  const cnpjLimpo = String(cnpj).replace(/\D/g, '');
  
  if (!cnpjLimpo || cnpjLimpo.length !== 14) {
    return null;
  }
  
  try {
    const response = await fetch(`https://brasilapi.com.br/api/cnpj/v1/${cnpjLimpo}`);
    
    if (!response.ok) return null;
    
    const data = await response.json();
    
    return `${data.logradouro}, ${data.numero}${
      data.complemento ? ' (' + data.complemento + ')' : ''
    } — ${data.bairro}, ${data.municipio}/${data.uf}`;
    
  } catch (error) {
    console.warn(`Erro ao consultar CNPJ ${cnpj}:`, error);
    return null;
  }
}