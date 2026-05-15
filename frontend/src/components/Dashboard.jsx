import { useState } from "react";
import {
  LayoutDashboard,
  Scale,
  FilePieChart,
  Building2,
  Users,
  MapPin,
  LogOut,
} from "lucide-react";

// Importação dos módulos que já estão prontos
import RegistroProducao from "./modules/RegistroProducao";
import HistoricoProducao from "./modules/HistoricoProducao";

// Módulos que vamos criar em seguida
import GestaoAssociacoes from "./modules/GestaoAssociacoes";
import GestaoGrupos from "./modules/GestaoGrupos";
import GestaoMunicipios from "./modules/GestaoMunicipios";

export default function Dashboard({ onLogout }) {
  const [activeTab, setActiveTab] = useState("resumo");

  // O Menu agora reflete a hierarquia real da Rede de Catadores
  const menuItems = [
    { id: "resumo", label: "Início / Resumo", icon: LayoutDashboard },
    { id: "registro", label: "Lançar Produção", icon: Scale },
    { id: "historico", label: "Relatórios e Gráficos", icon: FilePieChart },
    { id: "associacoes", label: "Associações", icon: Building2 },
    { id: "grupos", label: "Grupos Locais", icon: Users },
    { id: "municipios", label: "Municípios", icon: MapPin },
  ];

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-900">
      {/* SIDEBAR FIXA */}
      <aside className="w-72 bg-green-900 text-white flex flex-col shadow-2xl z-20">
        <div className="p-8 border-b border-green-800">
          <h2 className="text-xl font-black tracking-tighter uppercase leading-none">
            Rede <span className="text-green-400">Gestão</span>
          </h2>
          <p className="text-[10px] text-green-400 font-bold uppercase mt-2 tracking-widest">
            Painel Administrativo
          </p>
        </div>

        <nav className="flex-1 p-4 mt-4 space-y-1">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-200 ${
                activeTab === item.id
                  ? "bg-green-600 text-white shadow-lg translate-x-1"
                  : "text-green-100/70 hover:bg-green-800 hover:text-white"
              }`}
            >
              <item.icon
                size={20}
                className={
                  activeTab === item.id ? "text-white" : "text-green-400"
                }
              />
              <span className="font-semibold text-sm">{item.label}</span>
            </button>
          ))}
        </nav>

        {/* BOTÃO DE LOGOUT */}
        <div className="p-4 border-t border-green-800">
          <button
            onClick={onLogout}
            className="w-full flex items-center gap-3 px-4 py-3.5 text-red-300 hover:bg-red-900/40 rounded-xl transition-all"
          >
            <LogOut size={20} />
            <span className="font-bold text-sm">Sair do Sistema</span>
          </button>
        </div>
      </aside>

      {/* ÁREA DE CONTEÚDO PRINCIPAL */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* HEADER SUPERIOR */}
        <header className="h-20 bg-white border-b border-gray-200 flex items-center justify-between px-10">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-6 bg-green-500 rounded-full"></div>
            <h1 className="text-lg font-black text-gray-700 capitalize tracking-tight">
              {menuItems.find((i) => i.id === activeTab)?.label}
            </h1>
          </div>

          <div className="flex items-center gap-4 bg-gray-50 px-4 py-2 rounded-2xl border border-gray-100">
            <div className="text-right">
              <p className="text-xs font-bold text-gray-800">Admin Rede</p>
              <p className="text-[10px] text-green-600 font-black uppercase tracking-tighter">
                Assoc. Sede
              </p>
            </div>
            <div className="w-10 h-10 bg-green-600 rounded-xl flex items-center justify-center text-white font-black shadow-lg shadow-green-100">
              AS
            </div>
          </div>
        </header>

        {/* CONTEÚDO DINÂMICO (O MIOLO) */}
        <main className="flex-1 overflow-y-auto p-10 bg-[#f8fafc]">
          <div className="max-w-5xl mx-auto">
            {/* 1. ABA DE RESUMO (WELCOME SCREEN) */}
            {activeTab === "resumo" && (
              <div className="space-y-6">
                <div className="bg-white p-10 rounded-3xl shadow-sm border border-gray-100">
                  <h2 className="text-3xl font-black text-gray-800">
                    Bem-vindo de volta! 👋
                  </h2>
                  <p className="text-gray-500 mt-2 font-medium">
                    O que vamos gerenciar hoje na Rede de Catadores?
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <button
                    onClick={() => setActiveTab("registro")}
                    className="bg-green-50 hover:bg-green-100 p-8 rounded-3xl border-2 border-green-100 transition-all text-left group"
                  >
                    <Scale
                      className="text-green-600 mb-4 group-hover:scale-110 transition-transform"
                      size={40}
                    />
                    <h3 className="font-black text-green-900 text-xl">
                      Lançar Nova Produção
                    </h3>
                    <p className="text-green-700/70 text-sm mt-1">
                      Registrar os KGs coletados este mês.
                    </p>
                  </button>

                  <button
                    onClick={() => setActiveTab("historico")}
                    className="bg-white hover:border-green-200 p-8 rounded-3xl border-2 border-gray-50 transition-all text-left group shadow-sm"
                  >
                    <FilePieChart
                      className="text-blue-600 mb-4 group-hover:scale-110 transition-transform"
                      size={40}
                    />
                    <h3 className="font-black text-gray-800 text-xl">
                      Ver Relatórios
                    </h3>
                    <p className="text-gray-500 text-sm mt-1">
                      Analisar gráficos e histórico anual.
                    </p>
                  </button>

                  {/* Associações ocupando 1 coluna */}
                  <button
                    onClick={() => setActiveTab("associacoes")}
                    className="bg-white hover:border-orange-200 p-8 rounded-3xl border-2 border-gray-50 transition-all text-left group shadow-sm"
                  >
                    <Building2
                      className="text-orange-500 mb-4 group-hover:scale-110 transition-transform"
                      size={40}
                    />
                    <h3 className="font-black text-gray-800 text-xl">
                      Gestão de Associações
                    </h3>
                    <p className="text-gray-500 text-sm mt-1">
                      Cadastrar as entidades e polos da nossa rede.
                    </p>
                  </button>

                  {/* Grupos ocupando a outra coluna */}
                  <button
                    onClick={() => setActiveTab("grupos")}
                    className="bg-white hover:border-blue-200 p-8 rounded-3xl border-2 border-gray-50 transition-all text-left group shadow-sm"
                  >
                    <Users
                      className="text-blue-500 mb-4 group-hover:scale-110 transition-transform"
                      size={40}
                    />
                    <h3 className="font-black text-gray-800 text-xl">
                      Gestão de Grupos
                    </h3>
                    <p className="text-gray-500 text-sm mt-1">
                      Gerenciar equipes e coletivos de base locais.
                    </p>
                  </button>

                  {/* Municípios ocupando a linha inteira para equilibrar o grid ímpar */}
                  <button
                    onClick={() => setActiveTab("municipios")}
                    className="bg-white hover:border-emerald-200 p-8 rounded-3xl border-2 border-gray-50 transition-all text-left group shadow-sm md:col-span-2"
                  >
                    <MapPin
                      className="text-emerald-500 mb-4 group-hover:scale-110 transition-transform"
                      size={40}
                    />
                    <h3 className="font-black text-gray-800 text-xl">
                      Gestão de Municípios
                    </h3>
                    <p className="text-gray-500 text-sm mt-1">
                      Mapear e gerenciar a abrangência geográfica da rede no
                      estado.
                    </p>
                  </button>
                </div>
              </div>
            )}

            {/* ABAS FUNCIONAIS */}
            {activeTab === "registro" && <RegistroProducao />}
            {activeTab === "historico" && <HistoricoProducao />}

            {activeTab === "associacoes" && <GestaoAssociacoes />}
            {activeTab === "grupos" && <GestaoGrupos />}
            {activeTab === "municipios" && <GestaoMunicipios />}
          </div>
        </main>
      </div>
    </div>
  );
}
