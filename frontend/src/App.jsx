import { useState } from 'react';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Se estiver logado, mostra o painel fechado
  if (isAuthenticated) {
    return <Dashboard onLogout={() => setIsAuthenticated(false)} />;
  }

  // Se não estiver, mostra o site público (Landing Page)
  return <LandingPage onLoginSuccess={() => setIsAuthenticated(true)} />;
}

