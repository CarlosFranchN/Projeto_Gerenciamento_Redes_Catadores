import { useState, useEffect } from 'react';
import { Calendar, TrendingUp, DollarSign, FileDown, BarChart3, TableProperties } from 'lucide-react';
import { getProducao } from '../../services/api';

// Importações do Chart.js
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

// Registrando os componentes do gráfico
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function HistoricoProducao() {
  const [dados, setDados] = useState([]);
  const [anoFiltro, setAnoFiltro] = useState(new Date().getFullYear());
  const [loading, setLoading] = useState(true);
  const [modoVisualizacao, setModoVisualizacao] = useState('grafico'); // 'grafico' ou 'tabela'

  const mesesNome = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
  const mesesCompletos = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];

  useEffect(() => {
    const buscarDados = async () => {
      setLoading(true);
      const res = await getProducao(anoFiltro);
      setDados(Array.isArray(res) ? res : []);
      setLoading(false);
    };
    buscarDados();
  }, [anoFiltro]);

  const totalKG = dados.reduce((acc, item) => acc + (item.peso_kg || 0), 0);
  const totalValor = dados.reduce((acc, item) => acc + (item.valor_gerado || 0), 0);

  // === PREPARANDO DADOS PARA O GRÁFICO ===
  // Cria um array de 12 posições zeradas e preenche com os dados que vieram do banco
  const dadosGraficoKG = new Array(12).fill(0);
  dados.forEach(item => {
    if (item.mes >= 1 && item.mes <= 12) {
      dadosGraficoKG[item.mes - 1] = item.peso_kg;
    }
  });

  const chartData = {
    labels: mesesNome,
    datasets: [
      {
        label: 'Produção em KG',
        data: dadosGraficoKG,
        backgroundColor: 'rgba(22, 163, 74, 0.8)', // Verde Tailwind (green-600)
        borderRadius: 8, // Barras arredondadas
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        callbacks: {
          label: (context) => `${context.raw.toLocaleString('pt-BR')} KG`
        }
      }
    },
    scales: {
      y: { beginAtZero: true, grid: { borderDash: [4, 4] } },
      x: { grid: { display: false } }
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* CABEÇALHO, FILTROS E TOGGLE */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-black text-gray-800 tracking-tight">Análise de Resultados</h2>
          <p className="text-gray-500 font-medium">Acompanhe o desempenho da associação.</p>
        </div>
        
        <div className="flex items-center gap-4">
          {/* Toggle Gráfico/Tabela */}
          <div className="flex bg-gray-200 p-1 rounded-xl">
            <button 
              onClick={() => setModoVisualizacao('grafico')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-bold transition-all ${modoVisualizacao === 'grafico' ? 'bg-white text-green-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
            >
              <BarChart3 size={18} /> Gráfico
            </button>
            <button 
              onClick={() => setModoVisualizacao('tabela')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-bold transition-all ${modoVisualizacao === 'tabela' ? 'bg-white text-green-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
            >
              <TableProperties size={18} /> Tabela
            </button>
          </div>

          {/* Filtro de Ano */}
          <div className="flex items-center gap-2 bg-white p-2 rounded-xl shadow-sm border border-gray-200">
            <Calendar size={20} className="text-green-600 ml-2" />
            <select 
              value={anoFiltro}
              onChange={(e) => setAnoFiltro(e.target.value)}
              className="bg-transparent font-bold text-gray-700 outline-none pr-4 cursor-pointer"
            >
              <option value="2026">2026</option>
              <option value="2025">2025</option>
              <option value="2024">2024</option>
              <option value="2023">2023</option>
            </select>
          </div>
        </div>
      </div>

      {/* CARDS DE RESUMO OPERACIONAL */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-8 rounded-3xl shadow-xl shadow-green-100 text-white relative overflow-hidden">
          <TrendingUp className="absolute right-[-10px] bottom-[-10px] size-32 opacity-10" />
          <p className="text-green-100 font-bold uppercase tracking-wider text-xs">Total Triado em {anoFiltro}</p>
          <h3 className="text-4xl font-black mt-2">{totalKG.toLocaleString('pt-BR')} <span className="text-xl font-medium">KG</span></h3>
        </div>

        <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col justify-center">
          <p className="text-gray-400 font-bold uppercase tracking-wider text-xs">Valor Total Gerado</p>
          <div className="flex items-baseline gap-2 mt-2">
            <span className="text-green-600 font-bold text-xl">R$</span>
            <h3 className="text-4xl font-black text-gray-800">
              {totalValor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </h3>
          </div>
        </div>
      </div>

      {/* ÁREA DE CONTEÚDO (GRÁFICO OU TABELA) */}
      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden p-6">
        {loading ? (
          <div className="h-64 flex items-center justify-center text-gray-400 italic">Carregando dados...</div>
        ) : modoVisualizacao === 'grafico' ? (
          /* VISUALIZAÇÃO 1: GRÁFICO */
          <div className="h-96 w-full pt-4">
            <Bar data={chartData} options={chartOptions} />
          </div>
        ) : (
          /* VISUALIZAÇÃO 2: TABELA */
          <div>
            <div className="flex justify-end mb-4">
              <button className="text-sm font-bold text-green-700 hover:bg-green-50 px-4 py-2 rounded-xl transition-all flex items-center gap-2">
                <FileDown size={18} /> Exportar
              </button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-gray-50/50 text-gray-400 text-xs uppercase font-black tracking-widest border-b border-gray-100">
                  <tr>
                    <th className="px-6 py-4">Mês</th>
                    <th className="px-6 py-4">Quantidade (KG)</th>
                    <th className="px-6 py-4">Faturamento</th>
                    <th className="px-6 py-4">Observações</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {dados.length > 0 ? (
                    dados.sort((a,b) => a.mes - b.mes).map((item, index) => (
                      <tr key={index} className="hover:bg-green-50/30 transition-colors">
                        <td className="px-6 py-4 font-bold text-gray-700">{mesesCompletos[item.mes]}</td>
                        <td className="px-6 py-4 font-bold text-green-700">
                          {item.peso_kg.toLocaleString('pt-BR')} kg
                        </td>
                        <td className="px-6 py-4 font-semibold text-gray-600">
                          R$ {item.valor_gerado.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                        </td>
                        <td className="px-6 py-4 text-gray-500 text-sm italic">
                          {item.observado || "—"}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="4" className="px-6 py-12 text-center text-gray-400">Nenhum registro encontrado.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}