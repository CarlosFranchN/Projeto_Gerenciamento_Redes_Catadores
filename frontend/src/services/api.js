import axios from 'axios';
import { ASSOCIACOES, PRODUCAO_MENSAL } from '../data/index.js';
import { showWarning } from '../utils/toast.js';

// 1. Definição da URL Base
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// 2. Instância do Axios
export const api = axios.create({
  baseURL: baseURL.endsWith('/api') ? baseURL : `${baseURL}/api`, // Garante o /api no final
  withCredentials: true,
});

// 🔥 O PULO DO GATO: Interceptador que injeta o Token automaticamente em TODAS as requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// =============== FUNÇÕES DE AUTENTICAÇÃO ===============

export const login = async (username, password) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    // Envia os dados de login para o FastAPI
    const response = await api.post('token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    
    // 🔥 Salva o token real e as flags de sessão no LocalStorage
    // (Ajuste 'access_token' se o seu backend retornar com outro nome, ex: response.data.token)
    const token = response.data.access_token || response.data.token;
    
    if (token) {
      localStorage.setItem('token', token);
    }
    
    localStorage.setItem('is_authenticated', 'true');
    
    if (response.data.user) {
      localStorage.setItem('user_data', JSON.stringify(response.data.user));
    }
    
    return { success: true, user: response.data.user };
    
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'Erro ao fazer login';
    return { success: false, error: errorMessage };
  }
};

export const removeToken = async () => {
  try {
    await api.post('logout'); // Avisa o backend se necessário
  } catch (err) {
    console.error('Erro ao fazer logout no servidor', err);
  } finally {
    // 🔥 Limpa absolutamente tudo do navegador no logout
    localStorage.removeItem('token');
    localStorage.removeItem('is_authenticated');
    localStorage.removeItem('user_data');
  }
};

// Mantém a compatibilidade com seu App.jsx para checar se está logado
export const getToken = () => localStorage.getItem('is_authenticated');


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

// =============== CRUD DE ASSOCIAÇÕES ===============

export const createAssociacao = async (data) => {
  try {
    const response = await api.post('associacoes/', data);
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao criar associação';
    
    if (err.response && err.response.data && err.response.data.detail) {
      const detail = err.response.data.detail;
      if (Array.isArray(detail)) {
        errorMessage = detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ');
      } else if (typeof detail === 'string') {
        errorMessage = detail;
      }
    }
    
    if (err.response && err.response.status === 401) {
      errorMessage = 'Sua sessão expirou. Por favor, saia do sistema e faça login novamente.';
    }
    
    return { success: false, error: errorMessage };
  }
};

export const updateAssociacao = async (id, data) => {
  try {
    const response = await api.put(`associacoes/${id}`, data); 
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao atualizar associação';
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail;
      errorMessage = Array.isArray(detail) ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') : detail;
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

// =============== CRUD DE AFILIADOS ===============

export const createAfiliado = async (data) => {
  try {
    const response = await api.post('afiliados/', data);
    return { success: true, data: response.data };
  } catch (err) {
    return { success: false, error: 'Erro ao cadastrar afiliado' };
  }
};

// =============== CRUD DE PRODUÇÃO ===============

export const createProducao = async (data) => {
  try {
    const response = await api.post('producao/', data);
    return { success: true, data: response.data };
  } catch (err) {
    let errorMessage = 'Erro ao registrar produção';
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail;
      errorMessage = Array.isArray(detail) ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') : detail;
    }
    if (err.response?.status === 401) {
      errorMessage = 'Sua sessão expirou. Por favor, faça login novamente.';
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
      errorMessage = Array.isArray(detail) ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') : detail;
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
      errorMessage = Array.isArray(detail) ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') : detail;
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
      errorMessage = Array.isArray(detail) ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') : detail;
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
      errorMessage = Array.isArray(detail) ? detail.map(e => `Campo '${e.loc[e.loc.length - 1]}': ${e.msg}`).join(' | ') : detail;
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