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

export default function LandingPage({ onLoginSuccess }) {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isAfiliadosModalOpen, setIsAfiliadosModalOpen] = useState(false);

  return (
    <div className="bg-green-50 text-gray-800 min-h-screen">
      
      <Navbar 
      onOpenLogin={() => setIsLoginModalOpen(true)}
      onOpenAfiliados={() => setIsAfiliadosModalOpen(true)}/>
      
      <main>
        <Hero />
        <Sobre />
        <Iniciativas />
        <Rede />
        <Contato />
      </main>

      <Footer />

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