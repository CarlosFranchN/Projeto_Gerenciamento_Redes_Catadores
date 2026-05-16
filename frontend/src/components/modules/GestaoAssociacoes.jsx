import { useState } from 'react';
import { Building2, Plus, Search, Edit, Trash2, MapPin, CheckCircle, AlertCircle } from 'lucide-react';
import { getAssociacoes, createAssociacao, updateAssociacao, deleteAssociacao } from '../../services/api';

// IMPORTAÇÕES DA STACK DE DADOS e VALIDAÇÃO
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 🔥 UTILITÁRIOS DO SEU PROJETO
import { showWarning } from '../../utils/toast'; 
import { sanitizeCNPJ, sanitizePhone } from '../../utils/sanitizers'; // Limpeza para o banco
import { formatarCNPJ, formatarTelefone, formatarCEP } from '../../utils/masks'; // Formatação visual

// 1. SCHEMA DE VALIDAÇÃO (ZOD)
const associacaoSchema = z.object({
  nome: z.string().min(3, 'O nome deve ter pelo menos 3 caracteres'),
  cnpj: z.string().min(18, 'O CNPJ deve estar completo'), // Conta os pontos e traços da máscara visual
  lider: z.string().optional(),
  telefone: z.string().optional(),
  cep: z.string().optional(),
  endereco: z.string().optional(),
  bairro: z.string().optional(),
  cidade: z.string().optional(),
  uf: z.string().max(2, 'Apenas 2 letras').toUpperCase().optional(),
  status: z.string().default('ativo'),
  
  municipio_id: z.preprocess((val) => (val === "" || Number(val) === 0 ? null : Number(val)), z.number().nullable()),
  grupo_id: z.preprocess((val) => (val === "" || Number(val) === 0 ? null : Number(val)), z.number().nullable()),
  
  qtd_integrantes: z.coerce.number().min(0, 'Não pode ser negativo'),
  ativo: z.boolean()
});

export default function GestaoAssociacoes() {
  const [busca, setBusca] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editandoId, setEditandoId] = useState(null);
  
  const queryClient = useQueryClient();

  // 2. BUSCA DE DADOS (REACT QUERY)
  const { data: associacoes = [], isLoading } = useQuery({
    queryKey: ['associacoes'],
    queryFn: getAssociacoes
  });

  const associacoesFiltradas = busca 
    ? associacoes.filter(a => a.nome.toLowerCase().includes(busca.toLowerCase()) || a.cnpj.includes(busca)) 
    : associacoes;

  // 3. FORMULÁRIO (REACT HOOK FORM)
  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm({
    resolver: zodResolver(associacaoSchema),
    defaultValues: {
      nome: '', cnpj: '', lider: '', telefone: '', cep: '', endereco: '', bairro: '', 
      cidade: '', uf: '', status: 'ativo', municipio_id: 0, grupo_id: 0, qtd_integrantes: 0, ativo: true
    }
  });

  // Função para tratar a busca do CEP aplicando a máscara importada
  const handleBuscaCEP = async (e) => {
    const valorDigitado = e.target.value;
    const cepFormatado = formatarCEP(valorDigitado);
    setValue('cep', cepFormatado); // Atualiza visualmente no input
    
    const cepLimpo = cepFormatado.replace(/\D/g, '');
    if (cepLimpo.length === 8) {
      try {
        const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
        const data = await response.json();
        if (!data.erro) {
          setValue('endereco', data.logradouro);
          setValue('bairro', data.bairro);
          setValue('cidade', data.localidade);
          setValue('uf', data.uf);
        }
      } catch (err) {
        console.error("Erro ao buscar CEP", err);
      }
    }
  };

  // 4. MUTAÇÕES (SALVAR E EXCLUIR)
  const mutationSalvar = useMutation({
    mutationFn: (dados) => {
      const { cep, ...dadosLimpos } = dados;
      
      // 🔥 USANDO SEU ARQUIVO SANITIZERS.JS PARA SANEAR ANTES DE IR PRO BACKEND
      dadosLimpos.cnpj = sanitizeCNPJ(dadosLimpos.cnpj);
      if (dadosLimpos.telefone) {
        dadosLimpos.telefone = sanitizePhone(dadosLimpos.telefone);
      }

      return editandoId ? updateAssociacao(editandoId, dadosLimpos) : createAssociacao(dadosLimpos);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['associacoes']); 
      fecharModal();
      showWarning(`Associação ${editandoId ? 'atualizada' : 'cadastrada'} com sucesso!`);
    },
    onError: (error) => showWarning(error.message || 'Erro ao salvar associação.')
  });

  const mutationExcluir = useMutation({
    mutationFn: deleteAssociacao,
    onSuccess: () => {
      queryClient.invalidateQueries(['associacoes']);
      showWarning('Associação removida da rede.');
    },
    onError: (error) => showWarning(error.message || 'Erro ao excluir associação.')
  });

  // AÇÕES DA INTERFACE
  const handleEditar = (assoc) => {
    setEditandoId(assoc.id);
    
    // 🔥 Ao abrir para edição, já aplicamos as máscaras nos dados vindos puros do banco
    setValue('nome', assoc.nome || '');
    setValue('cnpj', formatarCNPJ(assoc.cnpj || ''));
    setValue('lider', assoc.lider || '');
    setValue('telefone', formatarTelefone(assoc.telefone || ''));
    setValue('endereco', assoc.endereco || '');
    setValue('bairro', assoc.bairro || '');
    setValue('cidade', assoc.cidade || '');
    setValue('uf', assoc.uf || '');
    setValue('status', assoc.status || 'ativo');
    setValue('municipio_id', assoc.municipio_id || 0);
    setValue('grupo_id', assoc.grupo_id || 0);
    setValue('qtd_integrantes', assoc.qtd_integrantes || 0);
    setValue('ativo', assoc.ativo !== undefined ? assoc.ativo : true);
    setShowModal(true);
  };

  const handleExcluir = (id, nome) => {
    if (window.confirm(`ATENÇÃO: Tem certeza que deseja excluir a associação "${nome}"?\nIsto apagará o registro do banco de dados.`)) {
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
            <Building2 className="text-green-600" /> Rede de Associações
          </h2>
          <p className="text-gray-500 text-sm font-medium mt-1">Gerencie os polos, sedes e entidades parceiras.</p>
        </div>

        <div className="flex w-full md:w-auto gap-3">
          <div className="relative flex-1 md:w-72">
            <Search className="absolute left-4 top-3 text-gray-400" size={18} />
            <input 
              type="text"
              placeholder="Buscar por nome ou CNPJ..."
              className="w-full pl-11 pr-4 py-2.5 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-green-500 outline-none transition-all font-medium"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-green-200 flex items-center gap-2 transition-all font-bold"
          >
            <Plus size={20} /> Nova Entidade
          </button>
        </div>
      </div>

      {/* TABELA */}
      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
        {isLoading ? (
          <div className="p-10 text-center text-green-600 font-bold animate-pulse">Carregando entidades...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-gray-50/80 text-gray-400 text-xs uppercase font-black tracking-widest border-b border-gray-100">
                <tr>
                  <th className="px-6 py-5">Entidade</th>
                  <th className="px-6 py-5">Localização</th>
                  <th className="px-6 py-5 text-center">Integrantes</th>
                  <th className="px-6 py-5 text-center">Status</th>
                  <th className="px-6 py-5 text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {associacoesFiltradas.length > 0 ? associacoesFiltradas.map((assoc) => (
                  <tr key={assoc.id} className="hover:bg-green-50/30 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="font-bold text-gray-800 text-base">{assoc.nome}</div>
                      <div className="text-xs text-gray-500 mt-0.5 font-medium">CNPJ: {assoc.cnpj} • Líder: {assoc.lider}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-bold text-gray-700 flex items-center gap-1.5">
                        <MapPin size={14} className="text-green-600" /> {assoc.cidade} - {assoc.uf}
                      </div>
                      <div className="text-xs text-gray-400 mt-0.5 truncate max-w-[200px]">{assoc.bairro}</div>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-lg font-bold text-sm">{assoc.qtd_integrantes}</span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      {assoc.ativo ? (
                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-md text-xs font-black uppercase flex items-center justify-center gap-1 w-max mx-auto"><CheckCircle size={12} /> Ativo</span>
                      ) : (
                        <span className="bg-red-100 text-red-700 px-3 py-1 rounded-md text-xs font-black uppercase flex items-center justify-center gap-1 w-max mx-auto"><AlertCircle size={12} /> Inativo</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onClick={() => handleEditar(assoc)} className="p-2 hover:bg-blue-50 text-blue-600 rounded-lg transition-colors"><Edit size={18} /></button>
                        <button onClick={() => handleExcluir(assoc.id, assoc.nome)} className="p-2 hover:bg-red-50 text-red-600 rounded-lg transition-colors"><Trash2 size={18} /></button>
                      </div>
                    </td>
                  </tr>
                )) : (
                  <tr><td colSpan="5" className="px-6 py-16 text-center text-gray-400 italic font-medium">Nenhuma associação encontrada.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* MODAL MISTO (CADASTRO/EDIÇÃO) */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-4xl rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
            
            <div className={`${editandoId ? 'bg-blue-700' : 'bg-green-700'} p-6 flex justify-between items-center shrink-0 transition-colors`}>
              <div>
                <h3 className="text-xl font-black text-white flex items-center gap-2">
                  <Building2 /> {editandoId ? 'Editar Entidade' : 'Cadastrar Entidade'}
                </h3>
                <p className={`${editandoId ? 'text-blue-200' : 'text-green-200'} text-sm mt-1`}>
                  {editandoId ? 'Altere os dados institucionais abaixo.' : 'Preencha os dados institucionais e de localização.'}
                </p>
              </div>
              <button onClick={fecharModal} className="text-white/80 hover:text-white hover:rotate-90 transition-all text-xl">✕</button>
            </div>
            
            <div className="overflow-y-auto p-8">
              <form id="formAssociacao" onSubmit={handleSubmit(onSubmit)} className="space-y-8">
                
                {/* IDENTIFICAÇÃO */}
                <div>
                  <h4 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-4 border-b pb-2">Identificação Principal</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div className="space-y-1 md:col-span-2">
                      <label className="text-xs font-bold text-gray-600 uppercase">Nome da Associação *</label>
                      <input {...register('nome')} className={`w-full border-2 rounded-xl p-3 outline-none ${errors.nome ? 'border-red-400 bg-red-50' : 'border-gray-200 focus:border-green-500'}`} />
                      {errors.nome && <p className="text-red-500 text-xs font-bold">{errors.nome.message}</p>}
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">CNPJ *</label>
                      <input 
                        {...register('cnpj')} 
                        onChange={(e) => setValue('cnpj', formatarCNPJ(e.target.value))} // 🔥 Aplica a máscara importada
                        placeholder="00.000.000/0001-00"
                        className={`w-full border-2 rounded-xl p-3 outline-none ${errors.cnpj ? 'border-red-400 bg-red-50' : 'border-gray-200 focus:border-green-500'}`} 
                      />
                      {errors.cnpj && <p className="text-red-500 text-xs font-bold">{errors.cnpj.message}</p>}
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">Nome do Líder/Presidente</label>
                      <input {...register('lider')} className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">Telefone de Contato</label>
                      <input 
                        {...register('telefone')} 
                        onChange={(e) => setValue('telefone', formatarTelefone(e.target.value))} // 🔥 Aplica a máscara importada
                        placeholder="(00) 00000-0000"
                        className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" 
                      />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">Qtd. de Integrantes</label>
                      <input type="number" {...register('qtd_integrantes')} className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" />
                      {errors.qtd_integrantes && <p className="text-red-500 text-xs font-bold">{errors.qtd_integrantes.message}</p>}
                    </div>
                  </div>
                </div>

                {/* ENDEREÇO COM BUSCA DE CEP */}
                <div>
                  <h4 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-4 border-b pb-2 flex items-center justify-between">
                    Localização
                    {!editandoId && <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded normal-case font-bold">Busca automática por CEP disponível</span>}
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
                    <div className="space-y-1 md:col-span-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">CEP</label>
                      <input 
                        {...register('cep')} 
                        onChange={handleBuscaCEP} 
                        placeholder="00000-000"
                        className="w-full border-2 border-green-200 bg-green-50 rounded-xl p-3 outline-none font-bold text-green-800 focus:border-green-500" 
                        maxLength="9" 
                      />
                    </div>
                    <div className="space-y-1 md:col-span-3">
                      <label className="text-xs font-bold text-gray-600 uppercase">Logradouro / Rua</label>
                      <input {...register('endereco')} className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" />
                    </div>
                    <div className="space-y-1 md:col-span-2">
                      <label className="text-xs font-bold text-gray-600 uppercase">Bairro</label>
                      <input {...register('bairro')} className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" />
                    </div>
                    <div className="space-y-1 md:col-span-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">Cidade</label>
                      <input {...register('cidade')} className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" />
                    </div>
                    <div className="space-y-1 md:col-span-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">UF</label>
                      <input {...register('uf')} maxLength="2" className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none uppercase focus:border-green-500" />
                    </div>
                  </div>
                </div>

                {/* ESTRUTURA SISTÊMICA & STATUS */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-5 bg-gray-50 p-5 rounded-2xl border border-gray-100">
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-gray-600 uppercase">ID Município</label>
                    <input type="number" {...register('municipio_id')} className="w-full border-2 border-white rounded-xl p-3 outline-none" />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-gray-600 uppercase">ID Grupo</label>
                    <input type="number" {...register('grupo_id')} className="w-full border-2 border-white rounded-xl p-3 outline-none" />
                  </div>
                  <div className="space-y-1 pt-6 flex items-center gap-3">
                    <input type="checkbox" id="ativo" {...register('ativo')} className="w-5 h-5 rounded text-green-600 focus:ring-green-500" />
                    <label htmlFor="ativo" className="text-sm font-bold text-gray-700">A entidade está ativa?</label>
                  </div>
                </div>

              </form>
            </div>

            {/* RODAPÉ */}
            <div className="p-6 border-t bg-gray-50 flex justify-end gap-3 shrink-0">
              <button type="button" onClick={fecharModal} className="px-6 py-3 font-bold text-gray-500 hover:bg-gray-200 rounded-xl transition-all">Cancelar</button>
              <button type="submit" form="formAssociacao" disabled={mutationSalvar.isPending} className={`${editandoId ? 'bg-blue-600 hover:bg-blue-700 shadow-blue-200' : 'bg-green-600 hover:bg-green-700 shadow-green-200'} text-white px-8 py-3 rounded-xl font-black shadow-lg transition-all disabled:opacity-50 flex items-center gap-2`}>
                {mutationSalvar.isPending ? 'Processando...' : editandoId ? 'Salvar Alterações' : 'Finalizar Cadastro'}
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}