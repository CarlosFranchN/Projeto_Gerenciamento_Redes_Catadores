import logo from '../../assets/logo.png';

export default function Hero() {
  return (
    <section className="bg-gradient-to-br from-green-800 to-green-600 text-white overflow-hidden">
      {/* Reduzi o gap no celular e aumentei no desktop */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 items-center py-12 sm:py-20 px-6">
        
        {/* TEXTOS E BOTÕES */}
        <div className="text-center md:text-left order-2 md:order-1">
          {/* Ajuste fino na escada de fontes: text-3xl -> 4xl -> 5xl -> 6xl */}
          <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold mb-4 leading-tight">
            Transformando resíduos em renda e dignidade ♻
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-green-50 mb-8 max-w-xl mx-auto md:mx-0">
            Catadores e catadoras organizados em prol da coleta seletiva, inclusão socioeconômica e preservação ambiental em todo o Ceará.
          </p>
          
          {/* BOTÕES: Empilhados (flex-col) no mobile, lado a lado (sm:flex-row) no tablet/pc */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            <a href="#projetos" className="w-full sm:w-auto text-center inline-block bg-yellow-400 hover:bg-yellow-300 text-green-900 font-bold px-6 py-3 rounded-full transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
              Conheça iniciativas
            </a>
            <a href="#contato" className="w-full sm:w-auto text-center inline-block bg-white/10 hover:bg-white/20 border border-white/30 font-bold px-6 py-3 rounded-full transition-all backdrop-blur-sm">
              Seja parceiro(a)
            </a>
          </div>
        </div>

        {/* IMAGEM */}
        <div className="flex justify-center md:justify-end order-1 md:order-2 mb-4 md:mb-0">
          {/* w-56 (celular), w-72 (tablet), w-96 (desktop). Ajuste fluido perfeito! */}
          <img 
            src={logo} 
            alt="Logo Rede de Catadores" 
            className="w-56 h-56 sm:w-72 sm:h-72 lg:w-96 lg:h-96 object-cover bg-white p-2 drop-shadow-2xl rounded-2xl" 
          />
        </div>
        
      </div>
    </section>
  );
}