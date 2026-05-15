import { useState } from 'react';
// IMPORTANTE: Adicionei o FileText aqui nos ícones
import { Save, Scale, AlertCircle, Calendar, DollarSign, FileText } from 'lucide-react';
import { createProducao } from '../../services/api';

export default function RegistroProducao() {
  const [loading, setLoading] = useState(false);
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });

  // 1. Adicionado 'observado' ao estado inicial
  const [formData, setFormData] = useState({
    mes: new Date().getMonth() + 1,
    ano: new Date().getFullYear(),
    peso_kg: '',
    valor_gerado: '',
    observado: '' 
  });

  const handleInputChange = (campo, valor) => {
    setFormData({ ...formData, [campo]: valor });
  };

  const handleSalvar = async () => {
    if (!formData.peso_kg) {
      setMensagem({ texto: 'Por favor, informe a quantidade em KG.', tipo: 'erro' });
      return;
    }

    setLoading(true);
    setMensagem({ texto: '', tipo: '' });

    // 2. Os dados que vão para a API agora puxam o texto digitado
    const dadosParaEnviar = {
      id: 0, 
      associacao_id: 1, // FIXO: ID da Associação Principal
      mes: parseInt(formData.mes),
      ano: parseInt(formData.ano),
      categoria: "PET", // A trava silenciosa
      peso_kg: parseFloat(formData.peso_kg),
      valor_gerado: parseFloat(formData.valor_gerado) || 0.0,
      observado: formData.observado || "Registro consolidado do mês" // Pega o texto ou usa um padrão
    };

    const resultado = await createProducao(dadosParaEnviar);

    if (resultado.success) {
      setMensagem({ texto: `Produção de ${formData.peso_kg} KG salva com sucesso!`, tipo: 'sucesso' });
      
      // 3. Limpa os valores para o próximo lançamento
      setFormData(prev => ({
        ...prev,
        peso_kg: '',
        valor_gerado: '',
        observado: ''
      }));
    } else {
      setMensagem({ texto: resultado.error || 'Erro ao salvar o registro mensal.', tipo: 'erro' });
    }
    setLoading(false);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
        
        {/* CABEÇALHO */}
        <div className="mb-8 border-b pb-4">
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <Scale className="text-green-600" />
            Lançamento Mensal Consolidado
          </h2>
          <p className="text-gray-500 mt-1">
            Registre o volume total (KG), o valor financeiro e observações do mês.
          </p>
        </div>

        {/* FEEDBACK DE SUCESSO/ERRO */}
        {mensagem.texto && (
          <div className={`p-4 rounded-xl mb-6 flex items-center gap-3 ${mensagem.tipo === 'erro' ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
            <AlertCircle size={20} />
            <span className="font-semibold">{mensagem.texto}</span>
          </div>
        )}

        <div className="space-y-8">
          
          {/* LINHA 1: PERÍODO */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-gray-50 p-6 rounded-xl border border-gray-100">
            <div className="space-y-2">
              <label className="text-sm font-bold text-gray-700 flex items-center gap-2">
                <Calendar size={16} className="text-green-600"/> Mês de Referência
              </label>
              <select 
                className="w-full border-2 border-gray-200 rounded-xl p-3 focus:ring-green-500 focus:border-green-500 outline-none font-medium text-gray-700"
                value={formData.mes}
                onChange={(e) => handleInputChange('mes', e.target.value)}
              >
                <option value="1">Janeiro</option>
                <option value="2">Fevereiro</option>
                <option value="3">Março</option>
                <option value="4">Abril</option>
                <option value="5">Maio</option>
                <option value="6">Junho</option>
                <option value="7">Julho</option>
                <option value="8">Agosto</option>
                <option value="9">Setembro</option>
                <option value="10">Outubro</option>
                <option value="11">Novembro</option>
                <option value="12">Dezembro</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-bold text-gray-700 flex items-center gap-2">
                <Calendar size={16} className="text-green-600"/> Ano
              </label>
              <input 
                type="number" 
                className="w-full border-2 border-gray-200 rounded-xl p-3 focus:ring-green-500 outline-none font-medium text-gray-700"
                value={formData.ano}
                onChange={(e) => handleInputChange('ano', e.target.value)}
              />
            </div>
          </div>

          {/* LINHA 2: VALORES (KG E R$) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-bold text-gray-700 flex items-center gap-2">
                <Scale size={16} className="text-green-600"/> Quantidade Total (KG)
              </label>
              <div className="relative">
                <input 
                  type="number" min="0" step="0.01" placeholder="Ex: 37655.00"
                  className="w-full border-2 border-gray-200 rounded-xl p-4 focus:border-green-500 outline-none font-black text-xl text-gray-800"
                  value={formData.peso_kg}
                  onChange={(e) => handleInputChange('peso_kg', e.target.value)}
                />
                <span className="absolute right-4 top-4 text-gray-400 font-bold">KG</span>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-bold text-gray-700 flex items-center gap-2">
                <DollarSign size={16} className="text-green-600"/> Dinheiro Arrecadado
              </label>
              <div className="relative">
                <span className="absolute left-4 top-4 text-gray-400 font-bold">R$</span>
                <input 
                  type="number" min="0" step="0.01" placeholder="0.00"
                  className="w-full border-2 border-gray-200 rounded-xl p-4 pl-12 focus:border-green-500 outline-none font-black text-xl text-gray-800"
                  value={formData.valor_gerado}
                  onChange={(e) => handleInputChange('valor_gerado', e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* LINHA 3: OBSERVAÇÕES (NOVO CAMPO) */}
          <div className="space-y-2">
            <label className="text-sm font-bold text-gray-700 flex items-center gap-2">
              <FileText size={16} className="text-green-600"/> Observações do Lote (Opcional)
            </label>
            <textarea 
              rows="3"
              placeholder="Ex: Tivemos problemas com o transporte neste mês, por isso a arrecadação foi um pouco menor..."
              className="w-full border-2 border-gray-200 rounded-xl p-4 focus:border-green-500 outline-none font-medium text-gray-700 resize-none"
              value={formData.observado}
              onChange={(e) => handleInputChange('observado', e.target.value)}
            ></textarea>
          </div>

        </div>

        {/* BOTÃO SALVAR */}
        <div className="mt-10 pt-6 border-t border-gray-100">
          <button 
            onClick={handleSalvar}
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-black text-lg py-4 px-10 rounded-xl shadow-xl shadow-green-200 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <Save size={24} />
            {loading ? 'Processando...' : 'Gravar Produção Mensal'}
          </button>
        </div>
        
      </div>
    </div>
  );
}