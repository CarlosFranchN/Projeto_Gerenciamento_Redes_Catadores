import { useState } from 'react';
import Navbar from './layout/Navbar';
import Footer from './layout/Footer';
import Hero from './sections/Hero';
import Sobre from './sections/Sobre';
import Iniciativas from './sections/Iniciativas';
import Rede from './sections/Rede';
import Contato from './sections/Contato';
import LoginModal from './modals/LoginModal';
import AfiliadosModal from './modals/AfiliadosModal';

// 1. Recebemos a "chave" (onLoginSuccess) que veio lá do App.jsx
export default function LandingPage({ onLoginSuccess }) {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isAfiliadosModalOpen, setIsAfiliadosModalOpen] = useState(false);

  return (
    <div className="bg-green-50 text-gray-800 min-h-screen">
      
      <Navbar 
        onOpenLogin={() => setIsLoginModalOpen(true)}
        onOpenAfiliados={() => setIsAfiliadosModalOpen(true)}
      />
      
      <main>
        <Hero />
        <Sobre />
        <Iniciativas />
        <Rede />
        <Contato />
      </main>

      <Footer />

      {/* 2. Aqui passamos a "chave" para dentro do Modal */}
      <LoginModal 
        isOpen={isLoginModalOpen} 
        onClose={() => setIsLoginModalOpen(false)} 
        onLoginSuccess={onLoginSuccess} 
      />

      <AfiliadosModal 
        isOpen={isAfiliadosModalOpen} 
        onClose={() => setIsAfiliadosModalOpen(false)} 
      />
    </div>
  );
}