import { useState } from 'react';
import logo from '../../assets/logo.png';

export default function Navbar({ onOpenLogin, onOpenAfiliados }) {
  // Estado para controlar se o menu do celular está aberto ou fechado
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Função para fechar o menu automaticamente quando o usuário clica em um link
  const closeMenu = () => setIsMenuOpen(false);

  return (
    <header className="bg-green-700 text-white shadow-md sticky top-0 z-50">
      <nav className="max-w-7xl mx-auto flex justify-between items-center p-4">
        
        {/* LOGO E TÍTULO */}
        <div className="flex items-center gap-3">
          <img src={logo} alt="Logo" className="w-9 h-9 rounded-md bg-white p-0.5" />
          {/* No celular mostra texto menor. O "do Estado..." some em telas muito pequenas para não quebrar o layout */}
          <h1 className="font-bold text-base sm:text-xl leading-tight">
            Rede de Catadores <span className="hidden sm:inline">do Estado do Ceará</span>
          </h1>
        </div>

        {/* LINKS DESKTOP (Escondidos no celular, aparecem a partir do tablet 'md:') */}
        <ul className="hidden md:flex gap-6 font-medium items-center">
          <li><a href="#sobre" className="hover:text-yellow-300 transition-colors">Sobre</a></li>
          <li><a href="#projetos" className="hover:text-yellow-300 transition-colors">Iniciativas</a></li>
          <li><a href="#rede" className="hover:text-yellow-300 transition-colors">Nossa Rede</a></li>
          <li>
            <button
                onClick={onOpenAfiliados} 
                className="bg-white/10 hover:bg-white/20 border border-white/20 rounded-full px-4 py-1.5 transition-all">
              Afiliados
            </button>
          </li>
          <li>
            <button 
              onClick={onOpenLogin} 
              className="bg-yellow-400 text-green-900 hover:bg-yellow-300 px-4 py-1.5 rounded-full font-bold transition-all"
            >
              Login
            </button>
          </li>
        </ul>

        {/* BOTÃO MENU HAMBÚRGUER MOBILE (Só aparece no celular) */}
        <button 
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="md:hidden p-2 text-white hover:text-yellow-300 focus:outline-none"
        >
          {isMenuOpen ? (
            // Ícone de "X" quando o menu está aberto
            <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          ) : (
            // Ícone de 3 tracinhos (Hambúrguer) quando fechado
            <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path>
            </svg>
          )}
        </button>
      </nav>

      {/* PAINEL DROP-DOWN DO MENU MOBILE */}
      {isMenuOpen && (
        <div className="md:hidden bg-green-800 border-t border-green-600 shadow-inner absolute w-full left-0">
          <ul className="flex flex-col p-4 space-y-4 font-medium text-center">
            <li>
              <a href="#sobre" onClick={closeMenu} className="block hover:text-yellow-300">Sobre</a>
            </li>
            <li>
              <a href="#projetos" onClick={closeMenu} className="block hover:text-yellow-300">Iniciativas</a>
            </li>
            <li>
              <a href="#rede" onClick={closeMenu} className="block hover:text-yellow-300">Nossa Rede</a>
            </li>
            <li className="pt-2">
              <button
                onClick={() => { onOpenAfiliados(); closeMenu(); }} 
                className="w-full bg-white/10 hover:bg-white/20 border border-white/20 rounded-full px-4 py-2 transition-all">
                Afiliados
              </button>
            </li>
            <li>
              <button 
                onClick={() => { onOpenLogin(); closeMenu(); }} 
                className="w-full bg-yellow-400 text-green-900 hover:bg-yellow-300 px-4 py-2 rounded-full font-bold transition-all"
              >
                Login
              </button>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}