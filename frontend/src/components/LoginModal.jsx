import { useState } from 'react';
import { login } from '../services/api';

export default function LoginModal({ isOpen, onClose, onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Se o modal não estiver aberto, não renderiza nada
  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setIsLoading(true);

    const response = await login(username, password);

    if (response.success) {
      onLoginSuccess();
    } else {
      setErrorMsg(response.error || 'Credenciais inválidas. Tente novamente.');
    }
    
    setIsLoading(false);
  };

  return (
    <div className="fixed inset-0 bg-black/60 z-50 p-4 overflow-y-auto flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl border border-neutral-200 p-6 relative">
        
        {/* Cabeçalho do Modal */}
        <div className="flex items-start justify-between gap-4 mb-4">
          <h3 className="text-xl font-bold text-green-800">Acesso Restrito</h3>
          <button 
            onClick={onClose}
            className="rounded-full w-9 h-9 grid place-items-center border hover:bg-neutral-50 text-gray-500"
          >
            ✖
          </button>
        </div>

        {/* Formulário */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Usuário</label>
            <input 
              type="text" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-green-600 outline-none" 
              required 
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Senha</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-green-600 outline-none" 
              required 
            />
          </div>

          {errorMsg && (
            <div className="bg-red-50 border-l-4 border-red-500 p-3 text-sm text-red-700">
              {errorMsg}
            </div>
          )}

          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full bg-green-700 text-white font-semibold px-6 py-3 rounded-lg hover:bg-green-800 transition"
          >
            {isLoading ? 'Autenticando...' : 'Entrar'}
          </button>
        </form>

      </div>
    </div>
  );
}