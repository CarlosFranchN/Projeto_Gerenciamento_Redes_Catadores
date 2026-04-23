import { useState, useEffect } from 'react';
import { getProducao, getAssociacoes } from '../../services/api';

// Importações obrigatórias do Chart.js para o React
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

// Precisamos "registrar" os elementos do gráfico antes de usar
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Rede() {
  // Estados para guardar os dados da API
  const [dadosProducao, setDadosProducao] = useState([]);
  const [associacoes, setAssociacoes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // O useEffect roda automaticamente assim que o componente aparece na tela
useEffect(() => {
    async function carregarDados() {
      setIsLoading(true);
      try {
        // 🆕 Fazemos as duas chamadas em paralelo para ser mais rápido
        const [respostaProducao, respostaAssoc] = await Promise.all([
          getProducao(2024),
          getAssociacoes()
        ]);

        // Lógica do Gráfico
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

        // 🆕 Lógica das Associações (pegamos apenas as 6 primeiras para não quebrar o layout)
        setAssociacoes(respostaAssoc);

      } catch (error) {
        console.error("Erro ao carregar dados da Rede:", error);
      } finally {
        setIsLoading(false);
      }
    }

    carregarDados();
  }, []);

  // Configuração visual do Gráfico
  const chartData = {
    labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
    datasets: [
      {
        label: 'Produção (kg)',
        data: dadosProducao,
        backgroundColor: 'rgba(16, 185, 129, 0.8)', // Verde 500 do Tailwind
        borderRadius: 4, // Deixa as barrinhas arredondadas em cima
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false, // Esconde a legenda que fica em cima
      },
    },
  };

  // Calcula o total para exibir no texto
  const totalKg = dadosProducao.reduce((acc, val) => acc + val, 0);

  return (
    <section id="rede" className="max-w-7xl mx-auto py-16 px-6">
      <div className="grid lg:grid-cols-2 gap-8">
        
{/* Lado Esquerdo: Associações (AGORA DINÂMICO! 🚀) */}
        <div className="grid sm:grid-cols-2 gap-4">
  {isLoading ? (
    [1, 2, 3, 4].map(i => (
      <div key={i} className="p-4 border rounded-xl bg-gray-50 animate-pulse h-24"></div>
    ))
  ) : (
    // O .slice(1) pula o primeiro item da lista (a Rede de Catadores)
    associacoes.slice(1).map((assoc) => (
      <div key={assoc.id} className="p-4 border rounded-xl bg-white shadow-sm hover:border-green-300 transition-all hover:shadow-md">
        <h4 className="font-bold text-green-700 uppercase text-sm mb-1">{assoc.nome}</h4>
        <div className="text-xs text-gray-500 space-y-1">
          <p><strong>CNPJ:</strong> {assoc.cnpj || 'Em processo'}</p>
          <p><strong>Bairro:</strong> {assoc.bairro || 'Fortaleza'}</p>
          {assoc.qtd_integrantes > 0 && (
             <p className="text-green-600 font-semibold">
               {assoc.qtd_integrantes} Integrantes
             </p>
          )}
        </div>
      </div>
    ))
  )}
</div>

        {/* Lado Direito: O Gráfico 🚀 */}
        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <h4 className="text-xl font-semibold text-green-700 mb-2">Produção (amostra 2024)</h4>
          <p className="text-gray-700 mb-4">
            Registros mensais da <strong>Rede</strong>, totalizando <strong>{totalKg.toLocaleString('pt-BR')} kg</strong>.
          </p>
          
          <div className="overflow-hidden rounded-xl border bg-neutral-50 p-4 h-[300px]">
            {isLoading ? (
              <div className="flex items-center justify-center h-full text-gray-500 animate-pulse">
                Carregando dados da API...
              </div>
            ) : (
              <Bar data={chartData} options={chartOptions} />
            )}
          </div>
          
        </div>
      </div>
    </section>
  );
}