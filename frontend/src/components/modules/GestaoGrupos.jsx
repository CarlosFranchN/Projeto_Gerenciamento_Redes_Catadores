import { useState, useEffect } from 'react';
import { Users, Plus, Search, Edit, Trash2, MapPin, CheckCircle, AlertCircle } from 'lucide-react';
import { getGrupos, createGrupo, updateGrupo, deleteGrupo } from '../../services/api';

export default function GestaoGrupos() {
  const [grupos, setGrupos] = useState([]);
  const [busca, setBusca] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });
  const [editandoId, setEditandoId] = useState(null);

  const estadoInicial = {
    nome: '',
    cidade: '',
    uf: '',
    qtd_integrantes: 0,
    ativo: true
  };

  const [formData, setFormData] = useState(estadoInicial);

  const carregarDados = async () => {
    const dados = await getGrupos();
    if (busca) {
      setGrupos(dados.filter(g => 
        g.nome?.toLowerCase().includes(busca.toLowerCase()) || 
        g.cidade?.toLowerCase().includes(busca.toLowerCase())
      ));
    } else {
      setGrupos(dados);
    }
  };

  useEffect(() => {
    carregarDados();
  }, [busca]);

  const handleEditar = (grupo) => {
    setFormData({
      nome: grupo.nome || '',
      cidade: grupo.cidade || '',
      uf: grupo.uf || '',
      qtd_integrantes: grupo.qtd_integrantes || 0,
      ativo: grupo.ativo !== undefined ? grupo.ativo : true
    });
    setEditandoId(grupo.id);
    setShowModal(true);
  };

  const handleExcluir = async (id, nome) => {
    if (window.confirm(`ATENÇÃO: Tem certeza que deseja excluir o grupo "${nome}"?`)) {
      const res = await deleteGrupo(id);
      if (res.success) {
        carregarDados();
      } else {
        alert(`Erro ao excluir: ${res.error}`);
      }
    }
  };

  const handleSalvar = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMensagem({ texto: '', tipo: '' });

    // Garante que a quantidade seja um número inteiro antes de enviar
    const dadosParaEnviar = {
      ...formData,
      qtd_integrantes: parseInt(formData.qtd_integrantes) || 0
    };

    let res;
    if (editandoId) {
      res = await updateGrupo(editandoId, dadosParaEnviar);
    } else {
      res = await createGrupo(dadosParaEnviar);
    }
    
    if (res.success) {
      setMensagem({ texto: `Grupo ${editandoId ? 'atualizado' : 'cadastrado'} com sucesso!`, tipo: 'sucesso' });
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
            onClick={() => {
              setFormData(estadoInicial);
              setEditandoId(null);
              setShowModal(true);
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-blue-200 flex items-center gap-2 transition-all font-bold"
          >
            <Plus size={20} />
            <span className="hidden md:inline">Novo Grupo</span>
          </button>
        </div>
      </div>

      {/* TABELA DE GRUPOS */}
      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
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
              {grupos.length > 0 ? (
                grupos.map((grupo) => (
                  <tr key={grupo.id} className="hover:bg-blue-50/30 transition-colors group">
                    <td className="px-6 py-4 font-bold text-gray-800 text-base">
                      {grupo.nome}
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-bold text-gray-700 flex items-center gap-1.5">
                        <MapPin size={14} className="text-blue-600" /> {grupo.cidade} - {grupo.uf}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-lg font-bold text-sm">
                        {grupo.qtd_integrantes}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      {grupo.ativo ? (
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
                      <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button 
                          onClick={() => handleEditar(grupo)}
                          className="p-2 hover:bg-blue-100 text-blue-600 rounded-lg transition-colors"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button 
                          onClick={() => handleExcluir(grupo.id, grupo.nome)}
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
                    Nenhum grupo encontrado.
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
          <div className="bg-white w-full max-w-2xl rounded-3xl shadow-2xl overflow-hidden flex flex-col">
            
            <div className={`${editandoId ? 'bg-indigo-700' : 'bg-blue-700'} p-6 flex justify-between items-center shrink-0 transition-colors`}>
              <div>
                <h3 className="text-xl font-black text-white flex items-center gap-2">
                  <Users /> {editandoId ? 'Editar Grupo' : 'Cadastrar Grupo'}
                </h3>
              </div>
              <button onClick={fecharModal} className="text-white/80 hover:text-white hover:rotate-90 transition-all">✕</button>
            </div>
            
            <div className="p-8">
              {mensagem.texto && (
                <div className={`p-4 rounded-xl mb-6 flex items-center gap-3 ${mensagem.tipo === 'erro' ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
                  <AlertCircle size={20} />
                  <span className="font-bold">{mensagem.texto}</span>
                </div>
              )}

              <form id="formGrupo" onSubmit={handleSalvar} className="space-y-6">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-gray-600 uppercase">Nome do Grupo *</label>
                  <input required className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-blue-500" value={formData.nome} onChange={e => setFormData({...formData, nome: e.target.value})} />
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
                  <div className="space-y-1 md:col-span-3">
                    <label className="text-xs font-bold text-gray-600 uppercase">Cidade *</label>
                    <input required className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none focus:border-blue-500" value={formData.cidade} onChange={e => setFormData({...formData, cidade: e.target.value})} />
                  </div>
                  <div className="space-y-1 md:col-span-1">
                    <label className="text-xs font-bold text-gray-600 uppercase">UF *</label>
                    <input required className="w-full border-2 border-gray-200 rounded-xl p-3 outline-none uppercase focus:border-blue-500" maxLength="2" value={formData.uf} onChange={e => setFormData({...formData, uf: e.target.value.toUpperCase()})} />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-5 bg-gray-50 p-5 rounded-2xl border border-gray-100">
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-gray-600 uppercase">Qtd. de Integrantes</label>
                    <input type="number" min="0" className="w-full border-2 border-white rounded-xl p-3 outline-none focus:border-blue-500" value={formData.qtd_integrantes} onChange={e => setFormData({...formData, qtd_integrantes: e.target.value})} />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-gray-600 uppercase">Status</label>
                    <select className="w-full border-2 border-white rounded-xl p-3 outline-none font-bold focus:border-blue-500" value={formData.ativo ? 'true' : 'false'} onChange={e => setFormData({...formData, ativo: e.target.value === 'true'})}>
                      <option value="true">🟢 ATIVO</option>
                      <option value="false">🔴 INATIVO</option>
                    </select>
                  </div>
                </div>
              </form>
            </div>

            <div className="p-6 border-t bg-gray-50 flex justify-end gap-3 shrink-0">
              <button type="button" onClick={fecharModal} className="px-6 py-3 font-bold text-gray-500 hover:bg-gray-200 rounded-xl transition-all">Cancelar</button>
              <button type="submit" form="formGrupo" disabled={loading} className={`${editandoId ? 'bg-indigo-600 hover:bg-indigo-700 shadow-indigo-200' : 'bg-blue-600 hover:bg-blue-700 shadow-blue-200'} text-white px-8 py-3 rounded-xl font-black shadow-lg transition-all disabled:opacity-50 flex items-center gap-2`}>
                {loading ? 'Processando...' : editandoId ? 'Salvar Alterações' : 'Finalizar Cadastro'}
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}