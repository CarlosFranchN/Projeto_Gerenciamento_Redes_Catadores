import logo from '../../assets/logo.png';

export default function Navbar({ onOpenLogin, onOpenAfiliados }) {
  return (
    <header className="bg-green-700 text-white shadow-md sticky top-0 z-40">
      <nav className="max-w-7xl mx-auto flex justify-between items-center p-4">
        <div className="flex items-center gap-2">
          <img src={logo} alt="Logo" className="w-9 h-9 rounded-md" />
          <h1 className="font-bold text-lg sm:text-xl leading-tight">Rede de Catadores do Estado do Ceará</h1>
        </div>
        <ul className="flex gap-4 sm:gap-6 font-medium items-center">
          <li><a href="#sobre" className="hover:text-yellow-300 hidden sm:block">Sobre</a></li>
          <li><a href="#projetos" className="hover:text-yellow-300 hidden sm:block">Iniciativas</a></li>
          <li><a href="#rede" className="hover:text-yellow-300 hidden sm:block">Nossa Rede</a></li>
          <li>
            <button
                onClick={onOpenAfiliados} 
                className="bg-white/10 hover:bg-white/20 border border-white/20 rounded-full px-3 py-1">
              Afiliados
            </button>
          </li>
          <li>
            <button 
              onClick={onOpenLogin} 
              className="hover:text-yellow-300 font-semibold"
            >
              Login
            </button>
          </li>
        </ul>
      </nav>
    </header>
  );
}