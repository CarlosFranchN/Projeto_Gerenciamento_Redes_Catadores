import foto1 from '../../assets/foto1.png';
import foto2 from '../../assets/foto2.png';
import foto4 from '../../assets/foto4.png';

export default function Iniciativas() {
  return (
    // Reduzi o padding vertical no mobile (py-12) e mantive grande no desktop (sm:py-16)
    <section id="projetos" className="bg-green-100 py-12 sm:py-16 px-4 sm:px-6">
      <div className="max-w-7xl mx-auto">
        
        {/* Título adaptável: menor no celular, grande no desktop */}
        <h3 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-center text-green-800 mb-8 sm:mb-12">
          Nossas Iniciativas
        </h3>
        
        {/* O Grid Mágico: 1 coluna no mobile, 3 no desktop */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
          
          {/* CARTÃO 1 */}
          <div className="bg-white rounded-2xl shadow-md p-6 border border-green-100 transition-all duration-300 hover:-translate-y-2 hover:shadow-xl group">
            <div className="overflow-hidden rounded-xl mb-4">
              {/* O group-hover faz a imagem dar um leve zoom ao passar o mouse no cartão */}
              <img src={foto1} alt="Fachada do galpão" className="w-full h-48 sm:h-56 object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy" />
            </div>
            <h4 className="text-xl font-bold mb-2 text-green-800">Coleta Seletiva com Inclusão</h4>
            <p className="text-gray-600 leading-relaxed">Estruturas, rotas e parcerias com participação direta dos catadores(as).</p>
          </div>

          {/* CARTÃO 2 */}
          <div className="bg-white rounded-2xl shadow-md p-6 border border-green-100 transition-all duration-300 hover:-translate-y-2 hover:shadow-xl group">
            <div className="overflow-hidden rounded-xl mb-4">
              <img src={foto4} alt="Oficina" className="w-full h-48 sm:h-56 object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy" />
            </div>
            <h4 className="text-xl font-bold mb-2 text-green-800">Educação & Oficinas</h4>
            <p className="text-gray-600 leading-relaxed">Formações em reciclagem, segurança do trabalho, gestão e economia solidária.</p>
          </div>

          {/* CARTÃO 3 */}
          <div className="bg-white rounded-2xl shadow-md p-6 border border-green-100 transition-all duration-300 hover:-translate-y-2 hover:shadow-xl group">
            <div className="overflow-hidden rounded-xl mb-4">
              <img src={foto2} alt="Triagem" className="w-full h-48 sm:h-56 object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy" />
            </div>
            <h4 className="text-xl font-bold mb-2 text-green-800">Beneficiamento & Artesanato</h4>
            <p className="text-gray-600 leading-relaxed">Do beneficiamento ao reuso criativo: renda e valorização dos materiais.</p>
          </div>

        </div>
      </div>
    </section>
  );
}