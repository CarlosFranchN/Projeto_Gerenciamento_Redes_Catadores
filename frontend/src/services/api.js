import axios from 'axios';
import { ASSOCIACOES, PRODUCAO_MENSAL } from '../data/index.js';
import { showWarning } from '../utils/toast.js';

// 1. Definição da URL
const API_URL = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000/api/'
  : 'https://projeto-gerenciamento-redes-catadores.onrender.com/';

// 2. Instância do Axios
const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

// 3. O INTERCEPTADOR: A mágica que coloca o Token em todas as requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token'); // Tem que bater com o nome salvo no login!
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// =============== FUNÇÕES DE AUTENTICAÇÃO ===============

export const login = async (username, password) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    
    // Salva o token no LocalStorage
    localStorage.setItem('auth_token', response.data.access_token);
    return { success: true, token: response.data.access_token };
    
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'Erro ao fazer login';
    return { success: false, error: errorMessage };
  }
};

export const getToken = () => localStorage.getItem('auth_token');
export const setToken = (token) => localStorage.setItem('auth_token', token);
export const removeToken = () => localStorage.removeItem('auth_token');

// =============== CONSULTAS PÚBLICAS ===============

export async function getAssociacoes() {
  try {
    const response = await api.get('associacoes/?skip=0&limit=100&ativo=true');
    return response.data.items || [];
  } catch (error) {
    showWarning('Usando dados locais (API indisponível)');
    return ASSOCIACOES;
  }
}

export async function getProducao(ano = 2024) {
  try {
    const response = await api.get(`producao/?ano=${ano}`);
    return response.data;
  } catch (error) {
    return PRODUCAO_MENSAL;
  }
}

export async function getGrupos() {
  try {
    const response = await api.get('grupos/');
    return response.data.items || [];
  } catch (error) {
    showWarning('Usando dados locais (API indisponível)');
    const module = await import('../data/grupos.js');
    return module.GRUPOS;
  }
}

export async function getMunicipios() {
  try {
    const response = await api.get('municipios/');
    return response.data.items || [];
  } catch (error) {
    const module = await import('../data/municipios.js');
    return module.MUNICIPIOS;
  }
}

// =============== EXMPLO DE CRUD (Super Limpo) ===============

export const createAssociacao = async (data) => {
  try {
    const response = await api.post('associacoes/', data);
    return { success: true, data: response.data };
  } catch (err) {
    // TRATAMENTO DE ERRO 422 PARA ASSOCIAÇÕES
    let errorMessage = 'Erro ao criar associação';
    
    if (err.response && err.response.data && err.response.data.detail) {
      const detail = err.response.data.detail;
      
      if (Array.isArray(detail)) {
        errorMessage = detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ');
      } else if (typeof detail === 'string') {
        errorMessage = detail;
      }
    }
    
    // Se for Erro 401, avisamos o usuário que ele precisa relogar
    if (err.response && err.response.status === 401) {
      errorMessage = 'Sua sessão expirou. Por favor, saiga do sistema e faça login novamente.';
    }
    
    return { success: false, error: errorMessage };
  }
};

export const createAfiliado = async (data) => {
  try {
    const response = await api.post('afiliados/', data);
    return { success: true, data: response.data };
  } catch (err) {
    return { success: false, error: 'Erro ao cadastrar afiliado' };
  }
};

export const createProducao = async (data) => {
  try {
    const response = await api.post('producao/', data);
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao registrar produção';
    
    if (err.response && err.response.data && err.response.data.detail) {
      const detail = err.response.data.detail;
      
      if (Array.isArray(detail)) {
        errorMessage = detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ');
      } else if (typeof detail === 'string') {
        errorMessage = detail;
      }
    }
    
    if (err.response && err.response.status === 401) {
      errorMessage = 'Sua sessão expirou. Por favor, faça login novamente.';
    }
    
    return { success: false, error: errorMessage };
  }
};

export const deleteAssociacao = async (id) => {
  try {
    await api.delete(`associacoes/${id}`);
    return { success: true };
  } catch (err) {
    return { success: false, error: err.response?.data?.detail || 'Erro ao excluir' };
  }
};

export const updateAssociacao = async (id, data) => {
  try {
    // Note que passamos o ID na URL e os dados no corpo da requisição
    const response = await api.put(`associacoes/${id}`, data); 
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao atualizar associação';
    
    if (err.response && err.response.data && err.response.data.detail) {
      const detail = err.response.data.detail;
      if (Array.isArray(detail)) {
        errorMessage = detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ');
      } else if (typeof detail === 'string') {
        errorMessage = detail;
      }
    }
    return { success: false, error: errorMessage };
  }
};

// =============== CRUD DE GRUPOS ===============

export const createGrupo = async (data) => {
  try {
    const response = await api.post('grupos/', data);
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao criar grupo';
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail;
      errorMessage = Array.isArray(detail) 
        ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') 
        : detail;
    }
    return { success: false, error: errorMessage };
  }
};

export const updateGrupo = async (id, data) => {
  try {
    const response = await api.put(`grupos/${id}`, data);
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao atualizar grupo';
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail;
      errorMessage = Array.isArray(detail) 
        ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') 
        : detail;
    }
    return { success: false, error: errorMessage };
  }
};

export const deleteGrupo = async (id) => {
  try {
    await api.delete(`grupos/${id}`);
    return { success: true };
  } catch (err) {
    return { success: false, error: err.response?.data?.detail || 'Erro ao excluir grupo' };
  }
};

// =============== CRUD DE MUNICÍPIOS ===============

export const createMunicipio = async (data) => {
  try {
    const response = await api.post('municipios/', data);
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao cadastrar município';
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail;
      errorMessage = Array.isArray(detail) 
        ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') 
        : detail;
    }
    return { success: false, error: errorMessage };
  }
};

export const updateMunicipio = async (id, data) => {
  try {
    const response = await api.put(`municipios/${id}`, data);
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao atualizar município';
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail;
      errorMessage = Array.isArray(detail) 
        ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') 
        : detail;
    }
    return { success: false, error: errorMessage };
  }
};

export const deleteMunicipio = async (id) => {
  try {
    await api.delete(`municipios/${id}`);
    return { success: true };
  } catch (err) {
    return { success: false, error: err.response?.data?.detail || 'Erro ao excluir município' };
  }
};

export default api;