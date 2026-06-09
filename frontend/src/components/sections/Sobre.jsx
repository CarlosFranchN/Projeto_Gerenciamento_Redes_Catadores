import foto5 from '../../assets/foto5.jpg';

export default function Sobre() {
  return (
    // Redução de padding no mobile e ajuste de margens laterais
    <section id="sobre" className="max-w-7xl mx-auto py-12 sm:py-16 px-4 sm:px-6">
      <div className="grid lg:grid-cols-2 gap-10 lg:gap-12 items-center">
        
        {/* TEXTO E DADOS (No celular desce, no PC fica na esquerda) */}
        <div className="order-2 lg:order-1">
          <h3 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-green-800 mb-4 sm:mb-6">
            Quem Somos
          </h3>
          <p className="mb-4 text-base sm:text-lg text-gray-700 leading-relaxed">
            A Rede de Catadores(as) de Materiais Recicláveis do Estado do Ceará iniciou sua articulação no início dos anos 2000 e se formalizou em 2007. Com o respaldo da <strong className="text-green-800">Lei 12.305/2010</strong>, qualificou-se para atuar como co-gestora do gerenciamento de resíduos.
          </p>
          <p className="text-base sm:text-lg text-gray-700 leading-relaxed">
            Hoje, a rede representa <strong className="text-green-800">17 organizações</strong> em Fortaleza e diversas filiações no interior. Defendemos políticas públicas para infraestrutura, EPIs, logística, qualificação e inclusão socioeconômica na coleta seletiva.
          </p>
          
          {/* CARDS DE INFORMAÇÃO */}
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            <div className="rounded-2xl border border-green-200 bg-green-50 p-4 transition-colors hover:bg-green-100">
              <div className="text-xs sm:text-sm font-bold text-green-700 uppercase tracking-wider mb-1">Coordenação Geral</div>
              <div className="font-semibold text-gray-800 text-sm sm:text-base">Leina Mara Rodrigues da Silva Duarte</div>
            </div>
            
            <div className="rounded-2xl border border-green-200 bg-green-50 p-4 transition-colors hover:bg-green-100">
              <div className="text-xs sm:text-sm font-bold text-green-700 uppercase tracking-wider mb-1">CNPJ</div>
              <div className="font-semibold text-gray-800 text-sm sm:text-base">09.000.185/0001-09</div>
            </div>
            
            <div className="rounded-2xl border border-green-200 bg-green-50 p-4 transition-colors hover:bg-green-100">
              <div className="text-xs sm:text-sm font-bold text-green-700 uppercase tracking-wider mb-1">Sede</div>
              <div className="font-semibold text-gray-800 text-sm sm:text-base">Rua Valdemar Holanda, 474 — João XXIII, Fortaleza/CE</div>
            </div>
            
            <div className="rounded-2xl border border-green-200 bg-green-50 p-4 transition-colors hover:bg-green-100">
              <div className="text-xs sm:text-sm font-bold text-green-700 uppercase tracking-wider mb-1">E-mail</div>
              {/* O break-all impede que e-mails muito compridos quebrem a tela no celular */}
              <div className="font-semibold text-gray-800 text-sm sm:text-base break-all">redeestadual.catadores@gmail.com</div>
            </div>
          </div>
        </div>

        {/* IMAGEM E DESTAQUE (No celular sobe, no PC fica na direita) */}
        <div className="order-1 lg:order-2 rounded-3xl shadow-lg overflow-hidden border border-green-100 bg-white transition-all hover:shadow-xl hover:-translate-y-1">
          {/* Altura responsiva da imagem */}
          <img src={foto5} alt="Equipe de reciclagem" className="w-full h-56 sm:h-72 lg:h-80 object-cover" />
          <div className="p-6 sm:p-8">
            <h4 className="text-xl sm:text-2xl font-bold text-green-800 mb-3 flex items-center gap-2">
              <span className="text-2xl">🤝</span> Programa Auxílio Catador
            </h4>
            <p className="text-gray-600 text-sm sm:text-base leading-relaxed">
              Em parceria com a SEMA desde 2019, o programa repassa apoio financeiro aos catadores(as) associados, estimulando a coleta seletiva e fortalecendo o associativismo.
            </p>
          </div>
        </div>
        
      </div>
    </section>
  );
}