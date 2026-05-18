import axios from 'axios';
import { ASSOCIACOES, PRODUCAO_MENSAL } from '../data/index.js';
import { showWarning } from '../utils/toast.js';

// 1. Definição da URL
// const API_URL = window.location.hostname === 'localhost' || 
//                 window.location.hostname === '127.0.0.1'
//   ? 'http://127.0.0.1:8000/api/'
//   : 'https://projeto-gerenciamento-redes-catadores.onrender.com/';
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// 2. Instância do Axios
// const api = axios.create({
//   baseURL: API_URL,
//   timeout: 5000,
//   // 🔥 MUDANÇA CRUCIAL: Avisa ao Axios para SEMPRE enviar os Cookies HttpOnly
//   withCredentials: true, 
// });
export const api = axios.create({
  baseURL: baseURL.endsWith('/api') ? baseURL : `${baseURL}/api`, // 🔥 Garante o /api no final de qualquer forma!
  withCredentials: true,
});
// ❌ O INTERCEPTADOR FOI REMOVIDO! 
// O navegador agora anexa o Cookie automaticamente em cada requisição.

// =============== FUNÇÕES DE AUTENTICAÇÃO ===============

export const login = async (username, password) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    // O backend agora retorna os dados do usuário e injeta o Cookie na resposta
    const response = await api.post('token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    
    // 🔥 Não salvamos mais o token! Salvamos apenas uma flag inofensiva 
    // para o App.jsx saber que pode renderizar o Dashboard ao dar F5.
    localStorage.setItem('is_authenticated', 'true');
    
    // Você pode salvar os dados do usuário se quiser exibir o nome dele na tela
    if (response.data.user) {
      localStorage.setItem('user_data', JSON.stringify(response.data.user));
    }
    
    return { success: true, user: response.data.user };
    
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'Erro ao fazer login';
    return { success: false, error: errorMessage };
  }
};

// 🔥 ATUALIZADO: O botão "Sair" agora chama a rota /logout do backend para destruir o Cookie
export const removeToken = async () => {
  try {
    await api.post('logout'); // Pede pro FastAPI destruir o Cookie
  } catch (err) {
    console.error('Erro ao fazer logout no servidor', err);
  } finally {
    // Limpa as flags inofensivas do navegador de qualquer forma
    localStorage.removeItem('is_authenticated');
    localStorage.removeItem('user_data');
  }
};

// 🔥 ATUALIZADO: Usamos a flag inofensiva para manter a compatibilidade com seu App.jsx
export const getToken = () => localStorage.getItem('is_authenticated');
// (setToken foi removido pois não faz mais sentido manipularmos o token manualmente)


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

// =============== EXEMPLO DE CRUD (Super Limpo) ===============
// NENHUMA mudança brusca foi necessária aqui para baixo! O Axios cuida de enviar o Cookie.

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
      // Opcional: Você pode chamar o removeToken() aqui e forçar um reload na página
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