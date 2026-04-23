export default function Footer() {
  return (
    <footer className="bg-green-700 text-white py-8">
      <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-6 text-sm">
        <div>
          <div className="font-semibold text-lg">Rede de Catadores</div>
          <div className="mt-1 opacity-80">CNPJ: 09.000.185/0001-09</div>
        </div>
        <div>
          <div className="font-semibold text-lg">Endereço</div>
          <div className="mt-1 opacity-80">Rua Valdemar Holanda, 474 — João XXIII, Fortaleza/CE</div>
        </div>
        <div>
          <div className="font-semibold text-lg">Contato</div>
          <div className="mt-1 opacity-80">redeestadual.catadores@gmail.com</div>
        </div>
        <div>
          <div className="font-semibold text-lg">Redes Sociais</div>
          <div className="mt-2 flex items-center gap-3">
            <a href="https://www.instagram.com/redecatadoresce" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-full border border-white/30 flex items-center justify-center hover:bg-white/10 transition">
              <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor"><path d="M7 2h10a5 5 0 015 5v10a5 5 0 01-5 5H7a5 5 0 01-5-5V7a5 5 0 015-5zm10 2H7a3 3 0 00-3 3v10a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3zm-5 3a5 5 0 110 10 5 5 0 010-10zm0 2.2a2.8 2.8 0 100 5.6 2.8 2.8 0 000-5.6zM17.5 6.8a1.25 1.25 0 110 2.5 1.25 1.25 0 010-2.5z" /></svg>
            </a>
          </div>
        </div>
      </div>
      <p className="text-center mt-8 text-xs opacity-70">© 2025 Rede de Catadores. Feito com ♻ e respeito ao meio ambiente.</p>
    </footer>
  );
}