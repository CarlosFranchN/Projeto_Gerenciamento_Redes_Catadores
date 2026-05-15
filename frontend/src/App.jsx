import { useState, useEffect } from 'react';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';

// Importamos as ferramentas que criamos no nosso novo api.js (com Axios)
import { getToken, removeToken } from './services/api'; 

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true); // Evita piscar a tela de login ao dar F5

  // 1. Assim que o site abre, ele checa se já existe um token salvo
  useEffect(() => {
    const token = getToken(); 
    if (token) {
      setIsAuthenticated(true);
    }
    setIsCheckingAuth(false); // Terminou de checar
  }, []);

  // 2. Função para o botão de "Sair" lá do Dashboard
  const handleLogout = () => {
    removeToken(); // Limpa o token do navegador
    setIsAuthenticated(false); // Volta para a Landing Page
  };

  // Se ainda estiver checando o token ao dar F5, não mostra nada (ou mostra um loading)
  if (isCheckingAuth) {
    return <div className="min-h-screen flex items-center justify-center bg-green-50">Carregando...</div>;
  }

  // 3. Se logou com sucesso ou já tinha token, mostra o painel fechado!
  if (isAuthenticated) {
    return <Dashboard onLogout={handleLogout} />;
  }

  // 4. Se não tem token, mostra o site público e passa a "chave" para o modal
  return <LandingPage onLoginSuccess={() => setIsAuthenticated(true)} />;
}