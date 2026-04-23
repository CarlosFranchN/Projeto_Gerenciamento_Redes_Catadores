import logo from '../../assets/logo.png';

export default function Hero() {
  return (
    <section className="bg-gradient-to-br from-green-800 to-green-600 text-white">
      <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-10 items-center py-16 sm:py-20 px-6">
        <div className="text-center md:text-left">
          <h2 className="text-4xl md:text-5xl font-extrabold mb-4 leading-tight">
            Transformando resíduos em renda e dignidade ♻
          </h2>
          <p className="text-lg md:text-xl mb-6 max-w-xl mx-auto md:mx-0">
            Catadores e catadoras organizados em prol da coleta seletiva, inclusão socioeconômica e preservação ambiental em todo o Ceará.
          </p>
          <div className="flex gap-3 justify-center md:justify-start">
            <a href="#projetos" className="inline-block bg-yellow-400 hover:bg-yellow-300 text-green-900 font-semibold px-6 py-3 rounded-full transition">
              Conheça nossas iniciativas
            </a>
            <a href="#contato" className="inline-block bg-white/10 hover:bg-white/20 border border-white/30 font-semibold px-6 py-3 rounded-full transition hidden sm:inline-block">
              Seja parceiro(a)
            </a>
          </div>
        </div>
        <div className="flex justify-center md:justify-end">
          <img src={logo} alt="Logo Rede de Catadores" className="w-[320px] h-[320px] sm:w-[360px] sm:h-[360px] drop-shadow-2xl rounded-xl" />
        </div>
      </div>
    </section>
  );
}