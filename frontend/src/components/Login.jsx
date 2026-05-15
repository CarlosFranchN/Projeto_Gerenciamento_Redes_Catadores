import { useState } from 'react';
import api from '../services/api';

export default function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // O FastAPI usa formato Form Data para o login padrão OAuth2
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await api.post('/auth/token', formData);
      
      // Salva o token e avisa o App.jsx
      localStorage.setItem('token', response.data.access_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      
      onLoginSuccess();
    } catch (err) {
      setError('Usuário ou senha inválidos');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h2>Acesso Administrativo</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <input 
            type="text" 
            placeholder="Usuário" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input 
            type="password" 
            placeholder="Senha" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit" style={{ width: '100%', padding: '10px', background: '#2ecc71', color: 'white', border: 'none', cursor: 'pointer' }}>
          Entrar
        </button>
      </form>
    </div>
  );
}