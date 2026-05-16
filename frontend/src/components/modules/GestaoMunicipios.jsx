import { useState } from 'react';
import { MapPin, Plus, Search, Edit, Trash2, CheckCircle, AlertCircle } from 'lucide-react';
import { getMunicipios, createMunicipio, updateMunicipio, deleteMunicipio } from '../../services/api';

// IMPORTAÇÕES NOVAS (React Query + Hook Form + Zod)
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 🔥 UTILITÁRIOS DO SEU PROJETO
import { showWarning } from '../../utils/toast';
import { normalizeString } from '../../utils/sanitizers';

// 1. CRIAR O SCHEMA DE VALIDAÇÃO
const municipioSchema = z.object({
  nome: z.string().min(3, 'O nome deve ter pelo menos 3 caracteres'),
  uf: z.string().length(2, 'A UF deve ter exatamente 2 letras').toUpperCase(),
  qtd_integrantes: z.coerce.number().min(0, 'A quantidade não pode ser negativa'),
  ativo: z.boolean()
});

export default function GestaoMunicipios() {
  const [busca, setBusca] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editandoId, setEditandoId] = useState(null);
  
  const queryClient = useQueryClient();

  // 2. BUSCA DE DADOS COM REACT QUERY
  const { data: municipios = [], isLoading } = useQuery({
    queryKey: ['municipios'],
    queryFn: getMunicipios
  });

  const municipiosFiltrados = busca 
    ? municipios.filter(m => m.nome.toLowerCase().includes(busca.toLowerCase())) 
    : municipios;

  // 3. CONFIGURAR O FORMULÁRIO
  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm({
    resolver: zodResolver(municipioSchema),
    defaultValues: {
      nome: '',
      uf: 'CE',
      qtd_integrantes: 0,
      ativo: true
    }
  });

  // 4. MUTAÇÕES DO REACT QUERY
  const mutationSalvar = useMutation({
    mutationFn: (dados) => {
      // 🔥 NORMALIZAÇÃO DOS DADOS: Padroniza o texto antes de enviar para a API
      const dadosNormalizados = {
        ...dados,
        nome: normalizeString(dados.nome),
        uf: dados.uf.trim().toUpperCase()
      };
      
      return editandoId ? updateMunicipio(editandoId, dadosNormalizados) : createMunicipio(dadosNormalizados);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['municipios']); 
      fecharModal();
      // 🔥 Feedback via Toast elegante
      showWarning(`Município ${editandoId ? 'atualizado' : 'cadastrado'} com sucesso!`);
    },
    onError: (error) => showWarning(error.message || 'Erro ao salvar município.')
  });

  const mutationExcluir = useMutation({
    mutationFn: deleteMunicipio,
    onSuccess: () => {
      queryClient.invalidateQueries(['municipios']);
      showWarning('Município removido da abrangência da rede.');
    },
    onError: (error) => showWarning(error.message || 'Erro ao excluir município.')
  });

  // Funções de interface
  const handleEditar = (municipio) => {
    setEditandoId(municipio.id);
    setValue('nome', municipio.nome);
    setValue('uf', municipio.uf);
    setValue('qtd_integrantes', municipio.qtd_integrantes);
    setValue('ativo', municipio.ativo);
    setShowModal(true);
  };

  const handleExcluir = (id, nome) => {
    if (window.confirm(`Tem certeza que deseja excluir o município de ${nome}?\nIsso pode afetar as associações vinculadas a esta região.`)) {
      mutationExcluir.mutate(id);
    }
  };

  const onSubmit = (dados) => {
    mutationSalvar.mutate(dados);
  };

  const fecharModal = () => {
    setShowModal(false);
    setEditandoId(null);
    reset();
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* CABEÇALHO */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
        <div>
          <h2 className="text-2xl font-black text-gray-800 flex items-center gap-2">
            <MapPin className="text-emerald-600" /> Municípios da Rede
          </h2>
          <p className="text-gray-500 text-sm font-medium mt-1">Gestão da abrangência geográfica da rede.</p>
        </div>

        <div className="flex w-full md:w-auto gap-3">
          <div className="relative flex-1 md:w-72">
            <Search className="absolute left-4 top-3 text-gray-400" size={18} />
            <input 
              type="text"
              placeholder="Buscar município..."
              className="w-full pl-11 pr-4 py-2.5 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-emerald-500 outline-none transition-all font-medium"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-emerald-200 flex items-center gap-2 transition-all font-bold"
          >
            <Plus size={20} /> Nova Cidade
          </button>
        </div>
      </div>

      {/* TABELA */}
      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
        {isLoading ? (
          <div className="p-10 text-center text-emerald-600 font-bold animate-pulse">Carregando dados do servidor...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-gray-50/80 text-gray-400 text-xs uppercase font-black tracking-widest border-b border-gray-100">
                <tr>
                  <th className="px-6 py-5">Nome do Município</th>
                  <th className="px-6 py-5">Estado</th>
                  <th className="px-6 py-5 text-center">Integrantes</th>
                  <th className="px-6 py-5 text-center">Status</th>
                  <th className="px-6 py-5 text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {municipiosFiltrados.length > 0 ? municipiosFiltrados.map((m) => (
                  <tr key={m.id} className="hover:bg-emerald-50/30 transition-colors group">
                    <td className="px-6 py-4 font-bold text-gray-800 text-base">{m.nome}</td>
                    <td className="px-6 py-4">
                      <span className="bg-emerald-100 text-emerald-800 px-3 py-1 rounded-lg font-black text-xs">{m.uf}</span>
                    </td>
                    <td className="px-6 py-4 text-center font-bold text-gray-700 text-sm">{m.qtd_integrantes}</td>
                    <td className="px-6 py-4 text-center">
                      {m.ativo ? (
                        <span className="text-emerald-600 flex items-center justify-center gap-1 font-black text-xs uppercase"><CheckCircle size={14}/> ATIVO</span>
                      ) : (
                        <span className="text-red-400 flex items-center justify-center gap-1 font-black text-xs uppercase"><AlertCircle size={14}/> INATIVO</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onClick={() => handleEditar(m)} className="p-2 hover:bg-emerald-50 text-emerald-600 rounded-lg transition-colors"><Edit size={18} /></button>
                        <button onClick={() => handleExcluir(m.id, m.nome)} className="p-2 hover:bg-red-50 text-red-600 rounded-lg transition-colors"><Trash2 size={18} /></button>
                      </div>
                    </td>
                  </tr>
                )) : (
                  <tr><td colSpan="5" className="px-6 py-16 text-center text-gray-400 italic font-medium">Nenhum município encontrado.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* MODAL */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-lg rounded-3xl shadow-2xl overflow-hidden">
            <div className="bg-emerald-600 p-6 flex justify-between items-center text-white">
              <h3 className="text-xl font-black flex items-center gap-2"><MapPin /> {editandoId ? 'Editar Município' : 'Novo Município'}</h3>
              <button onClick={fecharModal} className="hover:rotate-90 transition-all text-2xl">✕</button>
            </div>
            
            <form onSubmit={handleSubmit(onSubmit)} className="p-8 space-y-6">
              
              <div>
                <label className="text-xs font-bold text-gray-400 uppercase">Nome do Município</label>
                <input 
                  {...register('nome')} 
                  className={`w-full border-2 rounded-xl p-3 outline-none font-medium ${errors.nome ? 'border-red-400 focus:border-red-500 bg-red-50' : 'border-gray-100 focus:border-emerald-500'}`} 
                />
                {errors.nome && <p className="text-red-500 text-xs font-bold mt-1">{errors.nome.message}</p>}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold text-gray-400 uppercase">UF (Estado)</label>
                  <input 
                    {...register('uf')} 
                    maxLength="2" 
                    className={`w-full border-2 rounded-xl p-3 outline-none uppercase font-bold ${errors.uf ? 'border-red-400 focus:border-red-500' : 'border-gray-100 focus:border-emerald-500'}`} 
                  />
                  {errors.uf && <p className="text-red-500 text-xs font-bold mt-1">{errors.uf.message}</p>}
                </div>
                <div>
                  <label className="text-xs font-bold text-gray-400 uppercase">Qtd. Integrantes</label>
                  <input 
                    type="number" 
                    {...register('qtd_integrantes')} 
                    className="w-full border-2 border-gray-100 rounded-xl p-3 outline-none focus:border-emerald-500" 
                  />
                  {errors.qtd_integrantes && <p className="text-red-500 text-xs font-bold mt-1">{errors.qtd_integrantes.message}</p>}
                </div>
              </div>

              <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-2xl border border-gray-100">
                <input type="checkbox" id="ativo" {...register('ativo')} className="w-5 h-5 rounded text-emerald-600 focus:ring-emerald-500" />
                <label htmlFor="ativo" className="text-sm font-bold text-gray-700">Município ativo?</label>
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t">
                <button type="button" onClick={fecharModal} className="px-6 py-3 font-bold text-gray-400 hover:text-gray-600">Cancelar</button>
                <button 
                  type="submit" 
                  disabled={mutationSalvar.isPending} 
                  className="bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-3 rounded-xl font-black transition-all disabled:opacity-50"
                >
                  {mutationSalvar.isPending ? 'Salvando...' : 'Confirmar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}