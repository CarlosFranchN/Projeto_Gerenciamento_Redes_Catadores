import { useState, useEffect } from 'react';
import { getAssociacoes, getGrupos, getMunicipios } from '../../services/api';

export default function AfiliadosModal({ isOpen, onClose }) {
  const [activeTab, setActiveTab] = useState('associacoes');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Efeito para carregar os dados sempre que a aba mudar ou o modal abrir
  useEffect(() => {
    if (!isOpen) return;

    async function fetchData() {
      setLoading(true);
      try {
        let result = [];
        if (activeTab === 'associacoes') result = await getAssociacoes();
        if (activeTab === 'grupos') result = await getGrupos();
        if (activeTab === 'municipios') result = await getMunicipios();
        
        setData(result);
      } catch (error) {
        console.error("Erro ao carregar afiliados:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [activeTab, isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 z-50 p-4 overflow-y-auto flex items-center justify-center animate-in fade-in duration-300">
      <div className="max-w-5xl w-full bg-white rounded-2xl shadow-2xl border border-neutral-200 p-6 relative">
        
        {/* Botão Fechar */}
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 rounded-full w-9 h-9 grid place-items-center border hover:bg-red-50 hover:text-red-600 text-gray-500 transition-all z-10"
        >
          ✖
        </button>

        <div className="flex flex-col gap-1 mb-6">
          <h3 className="text-2xl font-bold text-green-800">Afiliados da Rede</h3>
          <p className="text-gray-600 text-sm">Explore as entidades, grupos e municípios que compõem nossa força.</p>
        </div>

        {/* Sistema de Abas */}
        <div className="flex flex-wrap gap-2 mb-6 p-1 bg-gray-100 rounded-xl w-fit">
          {[
            { id: 'associacoes', label: 'Associações' },
            { id: 'grupos', label: 'Grupos de Trabalho' },
            { id: 'municipios', label: 'Municípios' }
          ].map((tab) => (
            <button 
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-5 py-2 rounded-lg font-medium transition-all ${
                activeTab === tab.id 
                ? 'bg-white text-green-700 shadow-sm' 
                : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Listagem de Dados */}
        <div className="min-h-[350px] max-h-[500px] overflow-y-auto border rounded-2xl p-4 bg-gray-50">
          {loading ? (
            <div className="flex flex-col items-center justify-center h-[300px] gap-3">
              <div className="w-10 h-10 border-4 border-green-600 border-t-transparent rounded-full animate-spin"></div>
              <p className="text-gray-500 font-medium">Consultando base de dados...</p>
            </div>
          ) : data.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {data.map((item) => (
                <div key={item.id} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm hover:border-green-300 transition-colors">
                  <h4 className="font-bold text-green-700 uppercase text-sm mb-2">{item.nome}</h4>
                  <div className="space-y-1 text-sm text-gray-600">
                    {item.cnpj && <p><strong>CNPJ:</strong> {item.cnpj}</p>}
                    {item.bairro && <p><strong>Bairro:</strong> {item.bairro}</p>}
                    {item.cidade && <p><strong>Local:</strong> {item.cidade} - {item.uf}</p>}
                    {item.qtd_integrantes !== undefined && <p><strong>Pessoas Integrantes:</strong> {item.qtd_integrantes}</p>}
                    {item.populacao && <p><strong>População:</strong> {item.populacao.toLocaleString()} hab.</p>}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-20 text-gray-400">
              Nenhum registro encontrado para esta categoria.
            </div>
          )}
        </div>

        <div className="mt-6 flex justify-between items-center">
          <p className="text-xs text-neutral-500 italic">
            Fonte: Dados integrados do Sistema de Gestão de Resíduos (SGR) — 2024.
          </p>
          <button 
            onClick={onClose}
            className="bg-green-700 hover:bg-green-800 text-white px-6 py-2 rounded-lg font-semibold transition"
          >
            Entendido
          </button>
        </div>
      </div>
    </div>
  );
}