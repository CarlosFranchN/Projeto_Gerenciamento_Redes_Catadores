import { useState, useEffect } from 'react';
import { MapPin, Plus, Search, Edit, Trash2, CheckCircle, AlertCircle } from 'lucide-react';
import { getMunicipios, createMunicipio, updateMunicipio, deleteMunicipio } from '../../services/api';

export default function GestaoMunicipios() {
  const [municipios, setMunicipios] = useState([]);
  const [busca, setBusca] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });
  const [editandoId, setEditandoId] = useState(null);

  const estadoInicial = {
    nome: '',
    uf: 'CE', // Padrão para facilitar o uso no Ceará
    qtd_integrantes: 0,
    ativo: true
  };

  const [formData, setFormData] = useState(estadoInicial);

  const carregarDados = async () => {
    const dados = await getMunicipios();
    if (busca) {
      setMunicipios(dados.filter(m => 
        m.nome?.toLowerCase().includes(busca.toLowerCase())
      ));
    } else {
      setMunicipios(dados);
    }
  };

  useEffect(() => {
    carregarDados();
  }, [busca]);

  const handleEditar = (municipio) => {
    setFormData({
      nome: municipio.nome || '',
      uf: municipio.uf || 'CE',
      qtd_integrantes: municipio.qtd_integrantes || 0,
      ativo: municipio.ativo !== undefined ? municipio.ativo : true
    });
    setEditandoId(municipio.id);
    setShowModal(true);
  };

  const handleExcluir = async (id, nome) => {
    if (window.confirm(`Tem certeza que deseja excluir o município de ${nome}?`)) {
      const res = await deleteMunicipio(id);
      if (res.success) {
        carregarDados();
      } else {
        alert(`Erro: ${res.error}`);
      }
    }
  };

  const handleSalvar = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMensagem({ texto: '', tipo: '' });

    const dadosParaEnviar = {
      ...formData,
      qtd_integrantes: parseInt(formData.qtd_integrantes) || 0
    };

    let res;
    if (editandoId) {
      res = await updateMunicipio(editandoId, dadosParaEnviar);
    } else {
      res = await createMunicipio(dadosParaEnviar);
    }
    
    if (res.success) {
      setMensagem({ texto: `Município ${editandoId ? 'atualizado' : 'cadastrado'} com sucesso!`, tipo: 'sucesso' });
      setTimeout(() => {
        fecharModal();
        carregarDados();
      }, 1500);
    } else {
      setMensagem({ texto: res.error, tipo: 'erro' });
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
              className="w-full pl-11 pr-4 py-2.5 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-emerald-500 outline-none transition-all"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-emerald-200 flex items-center gap-2 transition-all font-bold"
          >
            <Plus size={20} />
            <span className="hidden md:inline">Novo Município</span>
          </button>
        </div>
      </div>

      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50/80 text-gray-400 text-xs uppercase font-black tracking-widest border-b border-gray-100">
              <tr>
                <th className="px-6 py-5">Nome do Município</th>
                <th className="px-6 py-5">Estado</th>
                <th className="px-6 py-5 text-center">Total Integrantes</th>
                <th className="px-6 py-5 text-center">Status</th>
                <th className="px-6 py-5 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {municipios.map((m) => (
                <tr key={m.id} className="hover:bg-emerald-50/30 transition-colors group">
                  <td className="px-6 py-4 font-bold text-gray-800 text-base">{m.nome}</td>
                  <td className="px-6 py-4">
                    <span className="bg-emerald-100 text-emerald-800 px-3 py-1 rounded-lg font-black text-xs">
                      {m.uf}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className="font-bold text-gray-700">{m.qtd_integrantes}</span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    {m.ativo ? (
                      <span className="text-emerald-600 flex items-center justify-center gap-1 font-black text-xs uppercase">
                        <CheckCircle size={14} /> Ativo
                      </span>
                    ) : (
                      <span className="text-red-400 flex items-center justify-center gap-1 font-black text-xs uppercase">
                        <AlertCircle size={14} /> Inativo
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button onClick={() => handleEditar(m)} className="p-2 hover:bg-emerald-50 text-emerald-600 rounded-lg transition-colors"><Edit size={18} /></button>
                      <button onClick={() => handleExcluir(m.id, m.nome)} className="p-2 hover:bg-red-50 text-red-600 rounded-lg transition-colors"><Trash2 size={18} /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-gray-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-lg rounded-3xl shadow-2xl overflow-hidden">
            <div className={`${editandoId ? 'bg-emerald-700' : 'bg-emerald-600'} p-6 flex justify-between items-center text-white`}>
              <h3 className="text-xl font-black flex items-center gap-2"><MapPin /> {editandoId ? 'Editar Município' : 'Novo Município'}</h3>
              <button onClick={fecharModal} className="hover:rotate-90 transition-all text-2xl">✕</button>
            </div>
            <form onSubmit={handleSalvar} className="p-8 space-y-6">
              {mensagem.texto && (
                <div className={`p-4 rounded-xl flex items-center gap-3 ${mensagem.tipo === 'erro' ? 'bg-red-50 text-red-700' : 'bg-emerald-50 text-emerald-700'}`}>
                  <AlertCircle size={20} /> <span className="font-bold text-sm">{mensagem.texto}</span>
                </div>
              )}
              <div className="space-y-4">
                <div>
                  <label className="text-xs font-bold text-gray-400 uppercase">Nome do Município</label>
                  <input required className="w-full border-2 border-gray-100 rounded-xl p-3 focus:border-emerald-500 outline-none font-medium" value={formData.nome} onChange={e => setFormData({...formData, nome: e.target.value})} />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs font-bold text-gray-400 uppercase">UF (Estado)</label>
                    <input required maxLength="2" className="w-full border-2 border-gray-100 rounded-xl p-3 focus:border-emerald-500 outline-none uppercase font-bold" value={formData.uf} onChange={e => setFormData({...formData, uf: e.target.value.toUpperCase()})} />
                  </div>
                  <div>
                    <label className="text-xs font-bold text-gray-400 uppercase">Qtd. Integrantes</label>
                    <input type="number" min="0" className="w-full border-2 border-gray-100 rounded-xl p-3 focus:border-emerald-500 outline-none" value={formData.qtd_integrantes} onChange={e => setFormData({...formData, qtd_integrantes: e.target.value})} />
                  </div>
                </div>
                <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-2xl border border-gray-100">
                  <input type="checkbox" id="ativo" className="w-5 h-5 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500" checked={formData.ativo} onChange={e => setFormData({...formData, ativo: e.target.checked})} />
                  <label htmlFor="ativo" className="text-sm font-bold text-gray-700">Município está ativo no sistema?</label>
                </div>
              </div>
              <div className="flex justify-end gap-3 pt-4">
                <button type="button" onClick={fecharModal} className="px-6 py-3 font-bold text-gray-400 hover:text-gray-600">Cancelar</button>
                <button type="submit" disabled={loading} className="bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-3 rounded-xl font-black shadow-lg shadow-emerald-100 transition-all disabled:opacity-50">
                  {loading ? 'Salvando...' : 'Confirmar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}