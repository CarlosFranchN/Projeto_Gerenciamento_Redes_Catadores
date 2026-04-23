import foto5 from '../../assets/foto5.jpg';

export default function Sobre() {
  return (
    <section id="sobre" className="max-w-7xl mx-auto py-16 px-6">
      <div className="grid lg:grid-cols-2 gap-10 items-center">
        <div>
          <h3 className="text-3xl font-bold text-green-800 mb-4">Quem Somos</h3>
          <p className="mb-4 text-lg leading-relaxed">
            A Rede de Catadores(as) de Materiais Recicláveis do Estado do Ceará iniciou sua articulação no início dos anos 2000 e se formalizou em 2007. Com o respaldo da <strong>Lei 12.305/2010</strong>, qualificou-se para atuar como co-gestora do gerenciamento de resíduos.
          </p>
          <p className="text-lg leading-relaxed">
            Hoje, a rede representa <strong>17 organizações</strong> em Fortaleza e diversas filiações no interior. Defendemos políticas públicas para infraestrutura, EPIs, logística, qualificação e inclusão socioeconômica na coleta seletiva.
          </p>
          <div className="mt-6 grid sm:grid-cols-2 gap-3">
            <div className="rounded-2xl border border-green-100 bg-green-50 p-4">
              <div className="text-sm text-green-700">Coordenação Geral</div>
              <div className="font-semibold">Leina Mara Rodrigues da Silva Duarte</div>
            </div>
            <div className="rounded-2xl border border-green-100 bg-green-50 p-4">
              <div className="text-sm text-green-700">CNPJ</div>
              <div className="font-semibold">09.000.185/0001-09</div>
            </div>
            <div className="rounded-2xl border border-green-100 bg-green-50 p-4">
              <div className="text-sm text-green-700">Sede</div>
              <div className="font-semibold">Rua Valdemar Holanda, 474 — João XXIII, Fortaleza/CE</div>
            </div>
            <div className="rounded-2xl border border-green-100 bg-green-50 p-4">
              <div className="text-sm text-green-700">E-mail</div>
              <div className="font-semibold break-all">redeestadual.catadores@gmail.com</div>
            </div>
          </div>
        </div>
        <div className="rounded-2xl shadow-lg overflow-hidden border border-green-100 bg-white">
          <img src={foto5} alt="Equipe de reciclagem" className="w-full h-64 object-cover" />
          <div className="p-6">
            <h4 className="text-xl font-semibold text-green-700 mb-2">Programa Auxílio Catador</h4>
            <p className="text-gray-700">
              Em parceria com a SEMA desde 2019, o programa repassa apoio financeiro aos catadores(as) associados, estimulando a coleta seletiva e fortalecendo o associativismo.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}