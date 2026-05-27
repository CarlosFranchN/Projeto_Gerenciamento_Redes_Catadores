import { useState } from 'react';

export default function Contato() {
  const [formData, setFormData] = useState({ nome: '', email: '', mensagem: '' });
  
  const [aceitouTermos, setAceitouTermos] = useState(false);
  const [enviando, setEnviando] = useState(false);
  
  // 🔥 NOVO: Estado para controlar o balão de sucesso
  const [mostrarBalao, setMostrarBalao] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!aceitouTermos) return; 

    setEnviando(true);
    try {
      const response = await fetch("https://formspree.io/f/xredrywo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          nome: formData.nome,
          email: formData.email,
          mensagem: formData.mensagem
        })
      });

      if (response.ok) {
        // 🔥 Sai o alert feio, entra o balão bonito!
        setMostrarBalao(true);
        
        // Limpa o formulário
        setFormData({ nome: '', email: '', mensagem: '' });
        setAceitouTermos(false);

        // Faz o balão sumir sozinho depois de 5 segundos
        setTimeout(() => {
          setMostrarBalao(false);
        }, 5000);
      } else {
        alert("Ops! Ocorreu um erro ao enviar sua mensagem.");
      }
      
    } catch (error) {
      console.error("Erro ao enviar contato:", error);
      alert("Erro de conexão. Tente novamente mais tarde.");
    } finally {
      setEnviando(false);
    }
  };

  return (
    <section id="contato" className="bg-white py-16 px-6 max-w-4xl mx-auto relative">
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

      {/* 🔥 O BALÃO ESPECIAL FLUTUANTE 🔥 */}
      {mostrarBalao && (
        <div className="fixed bottom-10 right-10 z-50 bg-white border-l-4 border-green-600 shadow-2xl rounded-r-lg p-5 flex items-start gap-4 transition-all duration-500 animate-[bounce_1s_infinite]">
          {/* Ícone verde bonitinho */}
          <div className="bg-green-100 p-2 rounded-full">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <div>
            <h4 className="text-green-800 font-bold text-lg">Mensagem Recebida! ♻️</h4>
            <p className="text-sm text-gray-600">Agradecemos o contato. Retornaremos em breve!</p>
          </div>
          {/* Botão de fechar (X) caso ele queira fechar antes dos 5 segundos */}
          <button 
            onClick={() => setMostrarBalao(false)}
            className="text-gray-400 hover:text-gray-600 ml-4 font-bold"
          >
            ✕
          </button>
        </div>
      )}
    </section>
  );
}