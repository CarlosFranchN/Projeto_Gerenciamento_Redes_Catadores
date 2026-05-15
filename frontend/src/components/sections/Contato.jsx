import { useState } from 'react';

export default function Contato() {
  const [formData, setFormData] = useState({ nome: '', email: '', mensagem: '' });
  
  // 1. O Estado da LGPD: Controla se o visitante marcou a caixinha de consentimento
  const [aceitouTermos, setAceitouTermos] = useState(false);
  const [enviando, setEnviando] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!aceitouTermos) return; // Segurança extra

    setEnviando(true);
    try {
      // Aqui entraria a sua lógica de envio (Axios para o back ou serviço de e-mail)
      console.log("Enviando mensagem de contato:", formData);
      alert("Mensagem enviada com sucesso!");
      setFormData({ nome: '', email: '', mensagem: '' });
      setAceitouTermos(false);
    } catch (error) {
      console.error("Erro ao enviar contato:", error);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <section id="contato" className="bg-white py-16 px-6 max-w-4xl mx-auto">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold text-green-800">Fale Conosco</h2>
        <p className="text-gray-600 mt-2">Envie uma mensagem diretamente para a Associação de Catadores.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-1">Nome</label>
          <input 
            type="text" name="nome" required value={formData.nome} onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-1">E-mail</label>
          <input 
            type="email" name="email" required value={formData.email} onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-1">Mensagem</label>
          <textarea 
            name="mensagem" rows="4" required value={formData.mensagem} onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
          ></textarea>
        </div>

        {/* 2. O CHECKBOX DA LGPD NO FORMULÁRIO PÚBLICO */}
        <div className="flex items-start gap-3 bg-neutral-50 p-4 rounded-xl border border-neutral-200">
          <input 
            type="checkbox" 
            id="lgpd-contato"
            checked={aceitouTermos}
            onChange={(e) => setAceitouTermos(e.target.checked)}
            className="mt-1 w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500 cursor-pointer"
          />
          <label htmlFor="lgpd-contato" className="text-xs text-gray-600 cursor-pointer select-none">
            Autorizo a Associação de Catadores a utilizar os meus dados de contato preenchidos neste formulário exclusivamente para retornar a minha mensagem, em conformidade com a LGPD.
          </label>
        </div>

        {/* 3. O BOTÃO TRAVADO: Fica desativado se a caixinha não for marcada */}
        <button 
          type="submit"
          disabled={!aceitouTermos || enviando}
          className={`w-full py-3 rounded-lg font-bold transition-all duration-200 ${
            aceitouTermos && !enviando
              ? 'bg-green-700 hover:bg-green-800 text-white shadow-md cursor-pointer' 
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
        >
          {enviando ? 'Enviando...' : 'Enviar Mensagem'}
        </button>
      </form>
    </section>
  );
}