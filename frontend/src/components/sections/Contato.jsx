export default function Contato() {
  return (
    <section id="contato" className="max-w-4xl mx-auto py-16 px-6 text-center">
      <h3 className="text-3xl font-bold text-green-800 mb-3">Entre em Contato</h3>
      <p className="text-lg mb-6">Parcerias, doações e projetos: fale com a gente.</p>
      <form className="space-y-4 max-w-md mx-auto" onSubmit={(e) => e.preventDefault()}>
        <input type="text" placeholder="Seu nome" className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-green-600 outline-none" required />
        <input type="email" placeholder="Seu e-mail" className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-green-600 outline-none" required />
        <textarea placeholder="Sua mensagem" rows="4" className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-green-600 outline-none" required></textarea>
        <button type="submit" className="bg-green-700 text-white font-semibold px-6 py-3 rounded-lg hover:bg-green-800 transition w-full">
          Enviar Mensagem
        </button>
      </form>
    </section>
  );
}