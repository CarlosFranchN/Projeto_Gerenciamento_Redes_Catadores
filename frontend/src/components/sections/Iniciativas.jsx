import foto1 from '../../assets/foto1.png';
import foto2 from '../../assets/foto2.png';
import foto4 from '../../assets/foto4.png';

export default function Iniciativas() {
  return (
    <section id="projetos" className="bg-green-100 py-16 px-6">
      <div className="max-w-7xl mx-auto">
        <h3 className="text-3xl font-bold text-center text-green-800 mb-10">Nossas Iniciativas</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-2xl shadow-md p-6 border border-green-100">
            <img src={foto1} alt="Fachada do galpão" className="rounded-xl mb-4 w-full h-48 object-cover" loading="lazy" />
            <h4 className="text-xl font-semibold mb-2 text-green-700">Coleta Seletiva com Inclusão</h4>
            <p className="text-gray-700">Estruturas, rotas e parcerias com participação direta dos catadores(as).</p>
          </div>
          <div className="bg-white rounded-2xl shadow-md p-6 border border-green-100">
            <img src={foto4} alt="Oficina" className="rounded-xl mb-4 w-full h-48 object-cover" loading="lazy" />
            <h4 className="text-xl font-semibold mb-2 text-green-700">Educação & Oficinas</h4>
            <p className="text-gray-700">Formações em reciclagem, segurança do trabalho, gestão e economia solidária.</p>
          </div>
          <div className="bg-white rounded-2xl shadow-md p-6 border border-green-100">
            <img src={foto2} alt="Triagem" className="rounded-xl mb-4 w-full h-48 object-cover" loading="lazy" />
            <h4 className="text-xl font-semibold mb-2 text-green-700">Beneficiamento & Artesanato</h4>
            <p className="text-gray-700">Do beneficiamento ao reuso criativo: renda e valorização dos materiais.</p>
          </div>
        </div>
      </div>
    </section>
  );
}