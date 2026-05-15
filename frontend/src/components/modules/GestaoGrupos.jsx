import { useState } from 'react';
import { Users, Plus, Search, Edit, Trash2, MapPin, CheckCircle, AlertCircle } from 'lucide-react';
import { getGrupos, createGrupo, updateGrupo, deleteGrupo } from '../../services/api';

// IMPORTAÇÕES DA NOVA STACK
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 1. SCHEMA DE VALIDAÇÃO (ZOD)
const grupoSchema = z.object({
  nome: z.string().min(3, 'O nome deve ter pelo menos 3 caracteres'),
  cidade: z.string().min(3, 'A cidade deve ter pelo menos 3 caracteres'),
  uf: z.string().length(2, 'A UF deve ter exatamente 2 letras').toUpperCase(),
  qtd_integrantes: z.coerce.number().min(0, 'A quantidade não pode ser negativa'),
  ativo: z.boolean()
});

export default function GestaoGrupos() {
  const [busca, setBusca] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editandoId, setEditandoId] = useState(null);
  
  const queryClient = useQueryClient();

  // 2. BUSCA DE DADOS (REACT QUERY)
  const { data: grupos = [], isLoading } = useQuery({
    queryKey: ['grupos'],
    queryFn: getGrupos
  });

  const gruposFiltrados = busca 
    ? grupos.filter(g => g.nome.toLowerCase().includes(busca.toLowerCase()) || g.cidade.toLowerCase().includes(busca.toLowerCase())) 
    : grupos;

  // 3. FORMULÁRIO (REACT HOOK FORM)
  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm({
    resolver: zodResolver(grupoSchema),
    defaultValues: {
      nome: '',
      cidade: '',
      uf: 'CE',
      qtd_integrantes: 0,
      ativo: true
    }
  });

  // 4. MUTAÇÕES (SALVAR E EXCLUIR)
  const mutationSalvar = useMutation({
    mutationFn: (dados) => editandoId ? updateGrupo(editandoId, dados) : createGrupo(dados),
    onSuccess: () => {
      queryClient.invalidateQueries(['grupos']); 
      fecharModal();
      alert(`Grupo ${editandoId ? 'atualizado' : 'cadastrado'} com sucesso!`);
    },
    onError: (error) => alert(error.message || 'Erro ao salvar grupo.')
  });

  const mutationExcluir = useMutation({
    mutationFn: deleteGrupo,
    onSuccess: () => queryClient.invalidateQueries(['grupos'])
  });

  // AÇÕES DA INTERFACE
  const handleEditar = (grupo) => {
    setEditandoId(grupo.id);
    setValue('nome', grupo.nome);
    setValue('cidade', grupo.cidade);
    setValue('uf', grupo.uf);
    setValue('qtd_integrantes', grupo.qtd_integrantes);
    setValue('ativo', grupo.ativo);
    setShowModal(true);
  };

  const handleExcluir = (id, nome) => {
    if (window.confirm(`ATENÇÃO: Tem certeza que deseja excluir o grupo "${nome}"?`)) {
      mutationExcluir.mutate(id);
    }
  };

  const onSubmit = (dados) => mutationSalvar.mutate(dados);

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
            <Users className="text-blue-600" /> Grupos Locais
          </h2>
          <p className="text-gray-500 text-sm font-medium mt-1">Gerencie as equipes e coletivos de base.</p>
        </div>

        <div className="flex w-full md:w-auto gap-3">
          <div className="relative flex-1 md:w-72">
            <Search className="absolute left-4 top-3 text-gray-400" size={18} />
            <input 
              type="text"
              placeholder="Buscar por nome ou cidade..."
              className="w-full pl-11 pr-4 py-2.5 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-blue-500 outline-none transition-all font-medium"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-blue-200 flex items-center gap-2 transition-all font-bold"
          >
            <Plus size={20} /> Novo Grupo
          </button>
        </div>
      </div>

      {/* TABELA DE GRUPOS */}
      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
        {isLoading ? (
          <div className="p-10 text-center text-blue-600 font-bold animate-pulse">Carregando grupos...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-gray-50/80 text-gray-400 text-xs uppercase font-black tracking-widest border-b border-gray-100">
                <tr>
                  <th className="px-6 py-5">Nome do Grupo</th>
                  <th className="px-6 py-5">Localização</th>
                  <th className="px-6 py-5 text-center">Integrantes</th>
                  <th className="px-6 py-5 text-center">Status</th>
                  <th className="px-6 py-5 text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {gruposFiltrados.length > 0 ? gruposFiltrados.map((grupo) => (
                  <tr key={grupo.id} className="hover:bg-blue-50/30 transition-colors group">
                    <td className="px-6 py-4 font-bold text-gray-800 text-base">{grupo.nome}</td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-bold text-gray-700 flex items-center gap-1.5">
                        <MapPin size={14} className="text-blue-600" /> {grupo.cidade} - {grupo.uf}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-lg font-bold text-sm">{grupo.qtd_integrantes}</span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      {grupo.ativo ? (
                        <span className="text-emerald-600 flex items-center justify-center gap-1 font-black text-xs uppercase"><CheckCircle size={14} /> Ativo</span>
                      ) : (
                        <span className="text-red-400 flex items-center justify-center gap-1 font-black text-xs uppercase"><AlertCircle size={14} /> Inativo</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onClick={() => handleEditar(grupo)} className="p-2 hover:bg-blue-100 text-blue-600 rounded-lg"><Edit size={18} /></button>
                        <button onClick={() => handleExcluir(grupo.id, grupo.nome)} className="p-2 hover:bg-red-50 text-red-600 rounded-lg"><Trash2 size={18} /></button>
                      </div>
                    </td>
                  </tr>
                )) : (
                  <tr><td colSpan="5" className="px-6 py-16 text-center text-gray-400 italic font-medium">Nenhum grupo encontrado.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* MODAL MISTO (CADASTRO/EDIÇÃO) */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-2xl rounded-3xl shadow-2xl overflow-hidden flex flex-col">
            
            <div className={`${editandoId ? 'bg-indigo-700' : 'bg-blue-700'} p-6 flex justify-between items-center shrink-0 transition-colors`}>
              <h3 className="text-xl font-black text-white flex items-center gap-2">
                <Users /> {editandoId ? 'Editar Grupo' : 'Cadastrar Grupo'}
              </h3>
              <button onClick={fecharModal} className="text-white/80 hover:text-white hover:rotate-90 transition-all text-xl">✕</button>
            </div>
            
            <div className="p-8">
              <form id="formGrupo" onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                
                <div className="space-y-1">
                  <label className="text-xs font-bold text-gray-400 uppercase">Nome do Grupo *</label>
                  <input {...register('nome')} className={`w-full border-2 rounded-xl p-3 outline-none ${errors.nome ? 'border-red-400 focus:border-red-500 bg-red-50' : 'border-gray-100 focus:border-blue-500'}`} />
                  {errors.nome && <p className="text-red-500 text-xs font-bold">{errors.nome.message}</p>}
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
                  <div className="space-y-1 md:col-span-3">
                    <label className="text-xs font-bold text-gray-400 uppercase">Cidade *</label>
                    <input {...register('cidade')} className={`w-full border-2 rounded-xl p-3 outline-none ${errors.cidade ? 'border-red-400 focus:border-red-500 bg-red-50' : 'border-gray-100 focus:border-blue-500'}`} />
                    {errors.cidade && <p className="text-red-500 text-xs font-bold">{errors.cidade.message}</p>}
                  </div>
                  <div className="space-y-1 md:col-span-1">
                    <label className="text-xs font-bold text-gray-400 uppercase">UF *</label>
                    <input {...register('uf')} maxLength="2" className={`w-full border-2 rounded-xl p-3 outline-none uppercase ${errors.uf ? 'border-red-400 focus:border-red-500 bg-red-50' : 'border-gray-100 focus:border-blue-500'}`} />
                    {errors.uf && <p className="text-red-500 text-xs font-bold">{errors.uf.message}</p>}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-5 bg-gray-50 p-5 rounded-2xl border border-gray-100">
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-gray-400 uppercase">Qtd. de Integrantes</label>
                    <input type="number" {...register('qtd_integrantes')} className="w-full border-2 border-white rounded-xl p-3 outline-none focus:border-blue-500" />
                    {errors.qtd_integrantes && <p className="text-red-500 text-xs font-bold">{errors.qtd_integrantes.message}</p>}
                  </div>
                  <div className="flex items-center gap-3 pt-6">
                    <input type="checkbox" id="ativo" {...register('ativo')} className="w-5 h-5 rounded text-blue-600 focus:ring-blue-500" />
                    <label htmlFor="ativo" className="text-sm font-bold text-gray-700">Grupo ativo?</label>
                  </div>
                </div>
              </form>
            </div>

            <div className="p-6 border-t bg-gray-50 flex justify-end gap-3 shrink-0">
              <button type="button" onClick={fecharModal} className="px-6 py-3 font-bold text-gray-400 hover:text-gray-600">Cancelar</button>
              <button type="submit" form="formGrupo" disabled={mutationSalvar.isPending} className={`${editandoId ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-blue-600 hover:bg-blue-700'} text-white px-8 py-3 rounded-xl font-black shadow-lg transition-all disabled:opacity-50`}>
                {mutationSalvar.isPending ? 'Processando...' : 'Confirmar'}
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}