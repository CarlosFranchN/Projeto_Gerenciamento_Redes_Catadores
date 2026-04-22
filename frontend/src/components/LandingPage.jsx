import { useState } from 'react';
import Navbar from './layout/Navbar';
import Hero from './sections/Hero';
import Sobre from './sections/Sobre';
import Iniciativas from './sections/Iniciativas';
import Rede from './sections/Rede';
import Contato from './sections/Contato';
import Footer from './layout/Footer';
import LoginModal from './LoginModal';

export default function LandingPage({ onLoginSuccess }) {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  return (
    <div className="bg-green-50 text-gray-800 min-h-screen">
      
      {/* Passamos a função de abrir o modal como uma "prop" para a Navbar */}
      <Navbar onOpenLogin={() => setIsLoginModalOpen(true)} />
      
      <Hero />
      <Sobre />
      <Iniciativas />
      <Rede />
      <Contato />
      <Footer />

      <LoginModal 
        isOpen={isLoginModalOpen} 
        onClose={() => setIsLoginModalOpen(false)} 
        onLoginSuccess={onLoginSuccess} 
      />

    </div>
  );
}