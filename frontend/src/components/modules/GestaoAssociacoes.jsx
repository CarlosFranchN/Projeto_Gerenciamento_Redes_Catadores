import { useState, useEffect } from 'react';
import { Building2, Plus, Search, Edit, Trash2, MapPin, CheckCircle, AlertCircle } from 'lucide-react';
import { getAssociacoes, createAssociacao, updateAssociacao, deleteAssociacao } from '../../services/api';

export default function GestaoAssociacoes() {
  const [associacoes, setAssociacoes] = useState([]);
  const [busca, setBusca] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });
  
  // NOVO: Estado para saber se estamos editando um registro existente
  const [editandoId, setEditandoId] = useState(null);

  const estadoInicial = {
    nome: '',
    cnpj: '',
    lider: '',
    telefone: '',
    cep: '', 
    endereco: '',
    bairro: '',
    cidade: '',
    uf: '',
    status: 'ativo',
    municipio_id: '',
    grupo_id: '',
    qtd_integrantes: 0,
    ativo: true
  };

  const [formData, setFormData] = useState(estadoInicial);

  const carregarDados = async () => {
    const dados = await getAssociacoes();
    if (busca) {
      setAssociacoes(dados.filter(a => 
        a.nome?.toLowerCase().includes(busca.toLowerCase()) || 
        a.cnpj?.includes(busca)
      ));
    } else {
      setAssociacoes(dados);
    }
  };

  useEffect(() => {
    carregarDados();
  }, [busca]);

  const handleBuscaCEP = async (cepDigitado) => {
    const cepLimpo = cepDigitado.replace(/\D/g, '');
    setFormData({ ...formData, cep: cepDigitado });

    if (cepLimpo.length === 8) {
      try {
        const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
        const data = await response.json();
        if (!data.erro) {
          setFormData(prev => ({
            ...prev,
            endereco: data.logradouro,
            bairro: data.bairro,
            cidade: data.localidade,
            uf: data.uf
          }));
        }
      } catch (err) {
        console.log("Erro ao buscar CEP", err);
      }
    }
  };

  // NOVO: Prepara o modal para Edição
  const handleEditar = (assoc) => {
    setFormData({
      nome: assoc.nome || '',
      cnpj: assoc.cnpj || '',
      lider: assoc.lider || '',
      telefone: assoc.telefone || '',
      cep: '', // Fica vazio pois não salvamos CEP no banco
      endereco: assoc.endereco || '',
      bairro: assoc.bairro || '',
      cidade: assoc.cidade || '',
      uf: assoc.uf || '',
      status: assoc.status || 'ativo',
      municipio_id: assoc.municipio_id || '',
      grupo_id: assoc.grupo_id || '',
      qtd_integrantes: assoc.qtd_integrantes || 0,
      ativo: assoc.ativo !== undefined ? assoc.ativo : true
    });
    setEditandoId(assoc.id);
    setShowModal(true);
  };

  // NOVO: Função de Exclusão com confirmação
  const handleExcluir = async (id, nome) => {
    if (window.confirm(`ATENÇÃO: Tem certeza que deseja excluir a associação "${nome}"?\n\nIsso apagará o registro do banco de dados.`)) {
      const res = await deleteAssociacao(id);
      if (res.success) {
        alert("Associação excluída com sucesso!");
        carregarDados(); // Atualiza a tabela
      } else {
        alert(`Erro ao excluir: ${res.error}`);
      }
    }
  };

  // ATUALIZADO: Agora sabe diferenciar Criar e Atualizar
  const handleSalvar = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMensagem({ texto: '', tipo: '' });

    const { cep, ...dadosParaEnviar } = formData;
    
    // Tratamento para evitar quebra de Foreign Key
    dadosParaEnviar.municipio_id = parseInt(dadosParaEnviar.municipio_id) || null;
    dadosParaEnviar.grupo_id = parseInt(dadosParaEnviar.grupo_id) || null;
    dadosParaEnviar.qtd_integrantes = parseInt(dadosParaEnviar.qtd_integrantes) || 0;

    let res;
    if (editandoId) {
      // Se tiver ID de edição, atualiza
      res = await updateAssociacao(editandoId, dadosParaEnviar);
    } else {
      // Se não, cria um novo
      res = await createAssociacao(dadosParaEnviar);
    }
    
    if (res.success) {
      setMensagem({ texto: `Associação ${editandoId ? 'atualizada' : 'cadastrada'} com sucesso!`, tipo: 'sucesso' });
      setTimeout(() => {
        fecharModal();
        carregarDados();
      }, 1500);
    } else {
      setMensagem({ texto: res.error || 'Erro ao processar a requisição.', tipo: 'erro' });
    }
    setLoading(false);
  };

  const fecharModal = () => {
    setShowModal(false);
    setFormData(estadoInicial);
    setEditandoId(null);
    setMensagem({ texto: '', tipo: '' });
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
            onClick={() => {
              setFormData(estadoInicial);
              setEditandoId(null);
              setShowModal(true);
            }}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-green-200 flex items-center gap-2 transition-all font-bold"
          >
            <Plus size={20} />
            <span className="hidden md:inline">Nova Entidade</span>
          </button>
        </div>
      </div>

      {/* TABELA DE ASSOCIAÇÕES */}
      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
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
              {associacoes.length > 0 ? (
                associacoes.map((assoc) => (
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
                      <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-lg font-bold text-sm">
                        {assoc.qtd_integrantes}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      {assoc.ativo ? (
                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-md text-xs font-black uppercase flex items-center justify-center gap-1 w-max mx-auto">
                          <CheckCircle size={12} /> Ativo
                        </span>
                      ) : (
                        <span className="bg-red-100 text-red-700 px-3 py-1 rounded-md text-xs font-black uppercase flex items-center justify-center gap-1 w-max mx-auto">
                          <AlertCircle size={12} /> Inativo
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      {/* BOTÕES DE AÇÃO AGORA FUNCIONAM */}
                      <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button 
                          onClick={() => handleEditar(assoc)}
                          className="p-2 hover:bg-blue-50 text-blue-600 rounded-lg transition-colors"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button 
                          onClick={() => handleExcluir(assoc.id, assoc.nome)}
                          className="p-2 hover:bg-red-50 text-red-600 rounded-lg transition-colors"
                          title="Excluir"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="px-6 py-16 text-center text-gray-400 italic font-medium">
                    Nenhuma associação encontrada.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
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
              <button onClick={fecharModal} className="text-white/80 hover:text-white hover:rotate-90 transition-all">✕</button>
            </div>
            
            <div className="overflow-y-auto p-8">
              {mensagem.texto && (
                <div className={`p-4 rounded-xl mb-6 flex items-center gap-3 ${mensagem.tipo === 'erro' ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
                  <AlertCircle size={20} />
                  <span className="font-bold">{mensagem.texto}</span>
                </div>
              )}

              <form id="formAssociacao" onSubmit={handleSalvar} className="space-y-8">
                
                {/* BLOCO 1: IDENTIFICAÇÃO */}
                <div>
                  <h4 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-4 border-b pb-2">Identificação Principal</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div className="space-y-1 md:col-span-2">
                      <label className="text-xs font-bold text-gray-600 uppercase">Nome da Associação *</label>
                      <input required className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" value={formData.nome} onChange={e => setFormData({...formData, nome: e.target.value})} />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">CNPJ *</label>
                      <input required className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" value={formData.cnpj} onChange={e => setFormData({...formData, cnpj: e.target.value})} />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">Nome do Líder/Presidente</label>
                      <input className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" value={formData.lider} onChange={e => setFormData({...formData, lider: e.target.value})} />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">Telefone de Contato</label>
                      <input className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" value={formData.telefone} onChange={e => setFormData({...formData, telefone: e.target.value})} />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">Qtd. de Integrantes</label>
                      <input type="number" min="0" className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" value={formData.qtd_integrantes} onChange={e => setFormData({...formData, qtd_integrantes: e.target.value})} />
                    </div>
                  </div>
                </div>

                {/* BLOCO 2: ENDEREÇO */}
                <div>
                  <h4 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-4 border-b pb-2 flex items-center justify-between">
                    Localização
                    {!editandoId && <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded normal-case font-bold">Busca automática por CEP disponível</span>}
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
                    <div className="space-y-1 md:col-span-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">CEP</label>
                      <input className="w-full border-2 border-green-200 bg-green-50 rounded-xl p-3 outline-none font-bold text-green-800" placeholder="Opcional" maxLength="9" value={formData.cep} onChange={e => handleBuscaCEP(e.target.value)} />
                    </div>
                    <div className="space-y-1 md:col-span-3">
                      <label className="text-xs font-bold text-gray-600 uppercase">Logradouro / Rua</label>
                      <input className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" value={formData.endereco} onChange={e => setFormData({...formData, endereco: e.target.value})} />
                    </div>
                    <div className="space-y-1 md:col-span-2">
                      <label className="text-xs font-bold text-gray-600 uppercase">Bairro</label>
                      <input className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" value={formData.bairro} onChange={e => setFormData({...formData, bairro: e.target.value})} />
                    </div>
                    <div className="space-y-1 md:col-span-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">Cidade</label>
                      <input className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-green-500" value={formData.cidade} onChange={e => setFormData({...formData, cidade: e.target.value})} />
                    </div>
                    <div className="space-y-1 md:col-span-1">
                      <label className="text-xs font-bold text-gray-600 uppercase">UF</label>
                      <input className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none uppercase focus:border-green-500" maxLength="2" value={formData.uf} onChange={e => setFormData({...formData, uf: e.target.value.toUpperCase()})} />
                    </div>
                  </div>
                </div>

                {/* BLOCO 3: ESTRUTURA SISTÊMICA & STATUS */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-5 bg-gray-50 p-5 rounded-2xl border border-gray-100">
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-gray-600 uppercase">ID Município</label>
                    <input type="number" min="0" className="w-full border-2 border-white rounded-xl p-3 outline-none" value={formData.municipio_id} onChange={e => setFormData({...formData, municipio_id: e.target.value})} />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-gray-600 uppercase">ID Grupo</label>
                    <input type="number" min="0" className="w-full border-2 border-white rounded-xl p-3 outline-none" value={formData.grupo_id} onChange={e => setFormData({...formData, grupo_id: e.target.value})} />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-gray-600 uppercase">Status</label>
                    <select className="w-full border-2 border-white rounded-xl p-3 outline-none font-bold" value={formData.ativo ? 'true' : 'false'} onChange={e => setFormData({...formData, ativo: e.target.value === 'true'})}>
                      <option value="true">🟢 ATIVO</option>
                      <option value="false">🔴 INATIVO</option>
                    </select>
                  </div>
                </div>

              </form>
            </div>

            {/* RODAPÉ */}
            <div className="p-6 border-t bg-gray-50 flex justify-end gap-3 shrink-0">
              <button type="button" onClick={fecharModal} className="px-6 py-3 font-bold text-gray-500 hover:bg-gray-200 rounded-xl transition-all">Cancelar</button>
              <button type="submit" form="formAssociacao" disabled={loading} className={`${editandoId ? 'bg-blue-600 hover:bg-blue-700 shadow-blue-200' : 'bg-green-600 hover:bg-green-700 shadow-green-200'} text-white px-8 py-3 rounded-xl font-black shadow-lg transition-all disabled:opacity-50 flex items-center gap-2`}>
                {loading ? 'Processando...' : editandoId ? 'Salvar Alterações' : 'Finalizar Cadastro'}
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}