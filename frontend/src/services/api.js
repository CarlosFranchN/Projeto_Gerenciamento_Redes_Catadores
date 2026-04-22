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
  ? 'http://127.0.0.1:8000/api/'
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
      fetch(`${API_URL}associacoes/?skip=0&limit=100&ativo=true`),
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
    showWarning('Usando dados locais (API indisponível)');
    // Importa e retorna diretamente do arquivo local
    const module = await import('../data/grupos.js');
    return module.GRUPOS;
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
    // Fallback para dados estáticos
    import('../data/municipios.js').then(module => {
      return module.MUNICIPIOS;
    });
  }
}
export const login = async (username, password) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const res = await fetch(`${API_URL}token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro no login' };
    }
    
    const data = await res.json();
    localStorage.setItem('auth_token', data.access_token);
    return { success: true, token: data.access_token };
    
  } catch (err) {
    return { success: false, error: err.message };
  }
};

export const setToken = (token) => {
  localStorage.setItem('auth_token', token);
};

export const getToken = () => localStorage.getItem('auth_token');

export const logout = () => {
  localStorage.removeItem('auth_token');
};

export const removeToken = () => {
  localStorage.removeItem('auth_token');  // ← Mesma chave das outras funções
};

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

// =============== CRUD ASSOCIAÇÕES ===============
export const createAssociacao = async (data) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}associacoes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao criar' };
    }
    
    return { success: true, data: await res.json() };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

export const updateAssociacao = async (id, data) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}associacoes/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao atualizar' };
    }
    
    return { success: true, data: await res.json() };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

export const deleteAssociacao = async (id) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}associacoes/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao excluir' };
    }
    
    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

// =============== CRUD PRODUÇÃO ===============
export const createProducao = async (data) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}producao/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao criar' };
    }
    
    return { success: true, data: await res.json() };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

export const updateProducao = async (id, data) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}producao/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao atualizar' };
    }
    
    return { success: true, data: await res.json() };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

export const deleteProducao = async (id) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}producao/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao excluir' };
    }
    
    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

// =============== CRUD GRUPOS ===============
export const createGrupo = async (data) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}grupos/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao criar' };
    }
    
    return { success: true, data: await res.json() };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

export const deleteGrupo = async (id) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}grupos/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao excluir' };
    }
    
    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

// =============== CRUD MUNICÍPIOS ===============
export const createMunicipio = async (data) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}municipios/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao criar' };
    }
    
    return { success: true, data: await res.json() };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

export const deleteMunicipio = async (id) => {
  const token = getToken();
  try {
    const res = await fetch(`${API_URL}municipios/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao excluir' };
    }
    
    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
};

// =============== PERFIL ===============
export const updatePerfil = async (nome, senha) => {
  const token = getToken();
  try {
    const data = {};
    if (nome) data.nome = nome;
    if (senha) data.hashed_password = senha;
    
    const res = await fetch(`${API_URL}usuarios/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const error = await res.json();
      return { success: false, error: error.detail || 'Erro ao atualizar' };
    }
    
    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
};