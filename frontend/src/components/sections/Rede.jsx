import { useState, useEffect } from 'react';
import { getProducao, getAssociacoes } from '../../services/api';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Rede() {
  const [dadosProducao, setDadosProducao] = useState([]);
  const [associacoes, setAssociacoes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingGrafico, setIsLoadingGrafico] = useState(false); // Loading suave exclusivo para a troca de anos
  
  // 1. NOVO ESTADO: Monitora o ano selecionado pelo usuário
  const [anoSelecionado, setAnoSelecionado] = useState(2024);
  const [isModalAberta, setIsModalAberta] = useState(false);

  // Lista de anos disponíveis no sistema para o filtro
  const anosDisponiveis = [2024, 2025, 2026];

  // Efeito 1: Carrega as associações apenas uma vez quando o componente monta
  useEffect(() => {
    async function carregarAssoc() {
      try {
        const respostaAssoc = await getAssociacoes();
        setAssociacoes(Array.isArray(respostaAssoc) ? respostaAssoc : []);
      } catch (error) {
        console.error("Erro ao carregar associações:", error);
      }
    }
    carregarAssoc();
  }, []);

  // 2. NOVO EFFECT VINCULADO AO ANO: Dispara toda vez que 'anoSelecionado' muda
  useEffect(() => {
    async function carregarMetricasAno() {
      setIsLoadingGrafico(true);
      try {
        // Passamos o ano dinamicamente para a API do seu backend
        const respostaProducao = await getProducao(anoSelecionado);

        let valoresMensais = new Array(12).fill(0);
        if (Array.isArray(respostaProducao)) {
          respostaProducao.forEach((item, index) => {
            if (item.mes && item.peso_kg) {
              valoresMensais[item.mes - 1] += parseFloat(item.peso_kg);
            } else if (typeof item === 'number') {
              valoresMensais[index] = item;
            }
          });
        }
        setDadosProducao(valoresMensais);
      } catch (error) {
        console.error(`Erro ao carregar produção do ano ${anoSelecionado}:`, error);
      } finally {
        setIsLoadingGrafico(false);
        setIsLoading(false); // Desativa o esqueleto inicial
      }
    }

    carregarMetricasAno();
  }, [anoSelecionado]); // <-- A mágica de UX está nessa dependência

  const chartData = {
    labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
    datasets: [
      {
        label: 'Produção (kg)',
        data: dadosProducao,
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
        borderRadius: 4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  const totalKg = dadosProducao.reduce((acc, val) => acc + val, 0);

  return (
    <>
      <section id="rede" className="max-w-7xl mx-auto py-16 px-6 relative">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-extrabold text-green-800 mb-4">
            A Força da Nossa Rede
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Conheça algumas das associações integradas que movem a reciclagem no Ceará e acompanhe o impacto real da nossa produção.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 items-start">
          
          {/* LADO ESQUERDO: Lista de Associações (Mantido) */}
          <div>
            <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center gap-2">
              <span className="bg-green-100 text-green-700 p-2 rounded-lg">🏢</span> 
              Associações Parceiras
            </h3>
            
            <div className="grid sm:grid-cols-2 gap-4">
              {isLoading ? (
                [1, 2, 3, 4, 5, 6].map(i => (
                  <div key={i} className="p-4 border border-gray-100 rounded-xl bg-gray-50 animate-pulse h-32"></div>
                ))
              ) : associacoes.length > 1 ? (
                associacoes.slice(1, 7).map((assoc) => (
                  <div key={assoc.id} className="flex flex-col justify-between p-4 border border-gray-200 rounded-xl bg-white shadow-sm hover:border-green-400 transition-all hover:shadow-md duration-300">
                    <div>
                      <h4 className="font-bold text-green-700 uppercase text-sm mb-2 line-clamp-2" title={assoc.nome}>
                        {assoc.nome}
                      </h4>
                      <div className="text-sm text-gray-600 space-y-1">
                        <p><strong className="text-gray-800">CNPJ:</strong> {assoc.cnpj || 'Em processo'}</p>
                        <p><strong className="text-gray-800">Bairro:</strong> {assoc.bairro || 'Não informado'}</p>
                      </div>
                    </div>
                    {assoc.qtd_integrantes > 0 && (
                      <div className="mt-3">
                        <span className="text-xs font-semibold text-green-700 bg-green-50 px-2.5 py-1 rounded-md border border-green-100">
                          {assoc.qtd_integrantes} Integrantes
                        </span>
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="col-span-2 flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-200 rounded-xl text-gray-500 bg-gray-50">
                  <p>Nenhuma associação cadastrada no momento.</p>
                </div>
              )}
            </div>

            {!isLoading && associacoes.length > 7 && (
              <div className="mt-6 text-center sm:text-left">
                <button
                  onClick={() => setIsModalAberta(true)}
                  className="px-6 py-2.5 bg-green-50 text-green-700 font-semibold rounded-lg border border-green-200 hover:bg-green-100 hover:border-green-300 transition-all"
                >
                  Ver todas as {associacoes.length - 1} Associações →
                </button>
              </div>
            )}
          </div>

          {/* LADO DIREITO: Gráfico Dinâmico com Filtro */}
          <div className="sticky top-8">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <h3 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
                <span className="bg-green-100 text-green-700 p-2 rounded-lg">📈</span> 
                Produção da Rede
              </h3>
              
              {/* 3. COMPONENTE VISUAL DO SELECT */}
              <div className="flex items-center gap-2 bg-neutral-100 px-3 py-1.5 rounded-xl border border-neutral-200 w-fit">
                <label htmlFor="filtro-ano" className="text-xs font-bold text-gray-500 uppercase tracking-wider">Ano:</label>
                <select
                  id="filtro-ano"
                  value={anoSelecionado}
                  onChange={(e) => setAnoSelecionado(parseInt(e.target.value))}
                  className="bg-transparent text-sm font-bold text-green-800 outline-none pr-1 cursor-pointer"
                >
                  {anosDisponiveis.map(ano => (
                    <option key={ano} value={ano}>{ano}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="rounded-2xl border bg-white p-6 shadow-sm">
              <h4 className="text-lg font-semibold text-green-700 mb-1">Amostra do Ano de {anoSelecionado}</h4>
              <p className="text-sm text-gray-600 mb-6">
                Registros mensais acumulados, totalizando <strong className="text-gray-800 text-base">{totalKg.toLocaleString('pt-BR')} kg</strong> de material coletado.
              </p>
              
              <div className="overflow-hidden rounded-xl border bg-neutral-50 p-4 h-[320px] relative">
                {/* Loader exclusivo para quando o gráfico estiver recalculando */}
                {isLoadingGrafico ? (
                  <div className="absolute inset-0 bg-neutral-50/70 backdrop-blur-[1px] flex flex-col items-center justify-center text-green-700 space-y-2 z-10">
                    <div className="w-8 h-8 border-4 border-green-200 border-t-green-600 rounded-full animate-spin"></div>
                    <p className="text-xs font-medium">Atualizando gráfico...</p>
                  </div>
                ) : null}

                {isLoading ? (
                  <div className="flex items-center justify-center h-full text-gray-400">
                    Carregando dados...
                  </div>
                ) : (
                  <Bar data={chartData} options={chartOptions} />
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* MODAL DE VER TODAS AS ASSOCIAÇÕES (Mantido) */}
      {isModalAberta && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-200">
          <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <div>
                <h3 className="text-xl font-bold text-gray-800">Todas as Associações Parceiras</h3>
                <p className="text-sm text-gray-500">Listagem completa da rede cadastrada.</p>
              </div>
              <button
                onClick={() => setIsModalAberta(false)}
                className="text-gray-400 hover:text-red-500 hover:bg-red-50 p-2 rounded-lg transition-colors text-xl leading-none"
              >
                ✕
              </button>
            </div>

            <div className="p-6 overflow-y-auto flex-1 bg-gray-50/50">
              <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
                {associacoes.slice(1).map((assoc) => (
                  <div key={assoc.id} className="flex flex-col justify-between p-4 border border-gray-200 rounded-xl bg-white shadow-sm hover:border-green-400 transition-colors">
                    <div>
                      <h4 className="font-bold text-green-700 uppercase text-xs mb-2 line-clamp-2" title={assoc.nome}>
                        {assoc.nome}
                      </h4>
                      <div className="text-xs text-gray-600 space-y-1">
                        <p><strong className="text-gray-800">CNPJ:</strong> {assoc.cnpj || 'Não cadastrado'}</p>
                        <p><strong className="text-gray-800">Bairro:</strong> {assoc.bairro || 'Não informado'}</p>
                      </div>
                    </div>
                    {assoc.qtd_integrantes > 0 && (
                      <div className="mt-3">
                        <span className="text-[10px] font-semibold text-green-700 bg-green-50 px-2 py-1 rounded border border-green-100">
                          {assoc.qtd_integrantes} Integrantes
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="px-6 py-4 border-t border-gray-100 bg-white flex justify-end">
              <button onClick={() => setIsModalAberta(false)} className="px-6 py-2 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors">
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}