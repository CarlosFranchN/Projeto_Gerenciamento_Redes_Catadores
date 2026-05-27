import { useState, useEffect } from 'react';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';

// Importamos as ferramentas que criamos no nosso novo api.js (com Axios)
import { getToken, removeToken } from './services/api'; 

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true); 
  
  // 🔥 NOVO ESTADO: Define qual tela mostrar. Começa SEMPRE na landing page.
  const [currentView, setCurrentView] = useState('landing'); 

  // 1. Assim que o site abre, checa o token
  useEffect(() => {
    const token = getToken(); 
    if (token) {
      setIsAuthenticated(true);
    }
    setIsCheckingAuth(false);
  }, []);

  // 2. Função de Sair
  const handleLogout = () => {
    removeToken(); 
    setIsAuthenticated(false);
    setCurrentView('landing'); // Garante que volte para a Landing Page ao sair
  };

  if (isCheckingAuth) {
    return <div className="min-h-screen flex items-center justify-center bg-green-50">Carregando...</div>;
  }

  // 3. Só mostra o Dashboard se tiver token E o usuário quiser ver o dashboard
  if (isAuthenticated && currentView === 'dashboard') {
    return <Dashboard onLogout={handleLogout} />;
  }

  // 4. Por padrão, a Landing Page domina a tela inicial!
  return (
    <LandingPage 
      // Quando logar no modal, fica autenticado e é redirecionado
      onLoginSuccess={() => {
        setIsAuthenticated(true);
        setCurrentView('dashboard');
      }} 
      
      // Enviamos essas props para o botão da Landing Page se adaptar
      isAuthenticated={isAuthenticated}
      onGoToDashboard={() => setCurrentView('dashboard')}
    />
  );
}