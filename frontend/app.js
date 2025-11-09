const { useState, useEffect, useMemo, useRef } = React;

// URL Global da API
const API_URL = "http://127.0.0.1:8000";

// ========== Utils ==========
const cls = (...xs) => xs.filter(Boolean).join(" ");
const money = (n) => new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Number(n || 0));
const fmtDateBR = (iso) => {
    if (!iso) return "";
    const d = new Date(iso);
    if (isNaN(d)) return iso;
    return d.toLocaleDateString("pt-BR");
};
const todayISO = () => new Date().toISOString().slice(0, 10);
const sameYM = (iso, ref = new Date()) => {
    if (!iso) return false;
    const d = new Date(iso);
    return (
        d.getFullYear() === ref.getFullYear() &&
        d.getMonth() === ref.getMonth()
    );
};

// ========== UI building blocks ==========
const Card = ({ children, className }) => (<div className={cls("rounded-2xl border border-black/5 bg-white shadow-sm", className)}>{children}</div>);
const StatCard = ({ title, value, subtitle }) => (<div className="bg-white/80 rounded-2xl shadow-sm p-5 border border-black/5"> <div className="text-sm text-neutral-500">{title}</div> <div className="text-3xl font-semibold mt-1">{value}</div> {subtitle && <div className="text-xs mt-2 text-neutral-400">{subtitle}</div>} </div>);
const Toolbar = ({ children }) => (<div className="flex flex-col sm:flex-row sm:items-center gap-3 justify-between mb-4">{children}</div>);
const Pill = ({ active, onClick, children }) => (<button onClick={onClick} className={cls("px-4 py-2 rounded-full border text-sm transition", active ? "bg-emerald-600 text-white border-emerald-700" : "bg-white text-neutral-700 border-neutral-200 hover:bg-neutral-50")} > {children} </button>);
const Table = ({ columns, data, emptyLabel = "Sem dados" }) => {const safeData = data || [] 
    return (<div className="overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-sm"> <div className="overflow-x-auto"> <table className="min-w-full text-sm"> <thead className="bg-neutral-50"> <tr> {columns.map(c => (<th key={c.key} className="text-left px-4 py-3 font-medium text-neutral-600">{c.header}</th>))} </tr> </thead> <tbody> {safeData.length === 0 ? (<tr><td colSpan={columns.length} className="px-4 py-10 text-center text-neutral-400">{emptyLabel}</td></tr>) : (data.map((row, i) => (<tr key={row.id ?? i} className={i % 2 ? "bg-white" : "bg-neutral-50/40"}> {columns.map(c => (<td key={c.key} className="px-4 py-3 text-neutral-800"> {c.render ? c.render(row[c.key], row) : row[c.key]} </td>))} </tr>)))} </tbody> </table> </div> </div>)};
const Drawer = ({ open, onClose, title, children }) => (<div className={cls("fixed inset-0 z-50 transition", open ? "pointer-events-auto" : "pointer-events-none")}> <div className={cls("absolute inset-0 bg-black/40 transition-opacity", open ? "opacity-100" : "opacity-0")} onClick={onClose} /> <div className={cls("absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-xl border-l border-neutral-200 p-6 transition-transform", open ? "translate-x-0" : "translate-x-full")} role="dialog" aria-modal="true"> <div className="flex items-start justify-between mb-4"> <h3 className="text-lg font-semibold">{title}</h3> <button onClick={onClose} className="rounded-full w-8 h-8 grid place-items-center border border-neutral-200 hover:bg-neutral-50" aria-label="Fechar">×</button> </div> {children} </div> </div>);
const TextInput = ({ label, value, onChange, placeholder, type = "text", required }) => { const id = useMemo(() => Math.random().toString(36).slice(2), []); return (<label className="block"> <span className="text-sm text-neutral-600">{label}</span> <input id={id} type={type} value={value} required={required} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} className="mt-1 w-full rounded-xl border border-neutral-200 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-emerald-500" /> </label>); };
const Select = ({ label, value, onChange, options, placeholder = "Selecione...", required }) => { const id = useMemo(() => Math.random().toString(36).slice(2), []); return (<label className="block"> <span className="text-sm text-neutral-600">{label}</span> <select id={id} value={value} required={required} onChange={(e) => onChange(e.target.value)} className="mt-1 w-full rounded-xl border border-neutral-200 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-emerald-500" > <option value="">{placeholder}</option> {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)} </select> </label>); };

// ========== Views ==========
function DashboardView({ store }) {
    const materiaisAtivos = store.materiais.filter(m => m.ativo).length;
    const associacoesAtivas = store.associacoes.filter(a => a.ativo).length;
    const compradoresAtivos = store.compradores.filter(c => c.ativo).length;

    return (
        <section>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <StatCard title="Materiais" value={materiaisAtivos} subtitle="Cadastros Ativos" />
                <StatCard title="Associações" value={associacoesAtivas} subtitle="Parceiras Ativas" />
                <StatCard title="Compradores" value={compradoresAtivos} subtitle="Cadastros Ativos" />
                <StatCard title="Relatórios" value="4" subtitle="Disponíveis" />
            </div>
            <Card className="p-6">
                <h3 className="text-lg font-semibold mb-2">Boas-vindas 👋</h3>
                <p className="text-neutral-600 text-sm leading-relaxed">
                    Sistema de Gestão v2.0 (Arquitetura Doador/Comprador).
                    Use o menu para navegar e gerenciar os dados.
                </p>
            </Card>
        </section>
    );
}

function MateriaisView({ data, onCreate, onUpdate, fetchAPI }) {
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    const [nome, setNome] = useState("");
    const [categoria, setCategoria] = useState("");
    const [unidade, setUnidade] = useState("Kg");
    const [editingId, setEditingId] = useState(null);

    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false); setNome(""); setCategoria("");
        setUnidade("Kg"); setEditingId(null);
    };

    const handleOpenCreate = () => {
        handleCloseDrawer();
        setOpen(true);
    };

    const submit = async (e) => {
        e.preventDefault(); setBusy(true);
        const payload = { nome, categoria, unidade_medida: unidade }; 
        let success = false;
        try {
            if (editingId) {
                success = await onUpdate(editingId, payload);
            } else {
                success = await onCreate(payload);
            }
            if (success) { handleCloseDrawer(); }
        } catch (error) { console.error("Falha submit material:", error); }
        finally { setBusy(false); }
    };

    const handleEdit = (material) => {
        setEditingId(material.id);
        setNome(material.nome || "");
        setCategoria(material.categoria || "");
        setUnidade(material.unidade_medida || "Kg");
        setOpen(true);
    };

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Materiais e Estoque</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={handleOpenCreate}>+ Novo material</button>
            </Toolbar>
            <Table
                columns={[
                    { key: "id", header: "ID" },
                    { key: "codigo", header: "Código" },
                    { key: "nome", header: "Nome" },
                    { key: "categoria", header: "Categoria" },
                    {
                        key: "estoque_atual",
                        header: "Estoque Atual",
                        render: (estoque, row) => `${estoque !== null && estoque !== undefined ? estoque.toFixed(1) : '-'} ${row.unidade_medida || 'un'}`
                    },
                    {
                        key: "actions", header: "Ações", render: (_, row) => (
                            <button className="px-2 py-1 rounded-lg border text-xs text-blue-600 border-blue-200 hover:bg-blue-50"
                                onClick={() => handleEdit(row)} title="Editar material">
                                ✏️ Editar
                            </button>
                        )
                    },
                ]}
                data={data}
                emptyLabel="Nenhum material cadastrado"
            />
            <Drawer open={open} onClose={handleCloseDrawer} title={editingId ? "Editar Material" : "Adicionar Material"}>
                <form onSubmit={submit} className="space-y-3">
                    <TextInput label="Nome" value={nome} onChange={setNome} placeholder="Ex: PET, Papelão" required />
                    <TextInput label="Categoria" value={categoria} onChange={setCategoria} placeholder="Ex: Plástico, Papel" />
                    <TextInput label="Unidade de Medida" value={unidade} onChange={setUnidade} placeholder="Ex: Kg, un" required />
                    <div className="flex justify-end gap-2 pt-2">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button disabled={busy} className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60">{busy ? "Salvando..." : "Salvar"}</button>
                    </div>
                </form>
            </Drawer>
        </section>
    );
}
function TipoParceiroView({ data, onCreate }) {
    console.log("TipoParceiroView recebeu dados:", data);
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    const [nome, setNome] = useState("");

    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false); setNome("");
    };

    const submit = async (e) => {
        e.preventDefault(); setBusy(true);
        try {
            const success = await onCreate({ nome });
            if (success) { handleCloseDrawer(); }
        } catch (error) { console.error("Falha submit tipo:", error); }
        finally { setBusy(false); }
    };

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Tipos de Parceiro</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={() => setOpen(true)}>+ Novo Tipo</button>
            </Toolbar>
            <Table
                columns={[
                    { key: "id", header: "ID" },
                    { key: "nome", header: "Nome" },
                ]}
                data={data || []}
                emptyLabel="Nenhum tipo cadastrado."
            />
            <Drawer open={open} onClose={handleCloseDrawer} title="Novo Tipo de Parceiro">
                <form onSubmit={submit} className="space-y-3">
                    <TextInput label="Nome do Tipo" value={nome} onChange={setNome} placeholder="Ex: ORGAO_PUBLICO" required />
                    <div className="flex justify-end gap-2 pt-2">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button disabled={busy} className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60">{busy ? "Salvando..." : "Salvar"}</button>
                    </div>
                </form>
            </Drawer>
        </section>
    );
}
// --- NOVA VIEW DE COMPRADORES ---
function CompradoresView({ data, onCreate, onUpdate, onDelete }) {
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    const [editingId, setEditingId] = useState(null);

    // Campos do formulário
    const [nome, setNome] = useState("");
    const [cnpj, setCnpj] = useState("");
    const [telefone, setTelefone] = useState("");
    const [email, setEmail] = useState("");
    const [ativo, setAtivo] = useState(true);

    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false); setEditingId(null);
        setNome(""); setCnpj(""); setTelefone(""); setEmail(""); setAtivo(true);
    };

    const handleOpenCreate = () => {
        handleCloseDrawer();
        setOpen(true);
    };

    const handleEdit = (comprador) => {
        setEditingId(comprador.id);
        setNome(comprador.nome || "");
        setCnpj(comprador.cnpj || "");
        setTelefone(comprador.telefone || "");
        setEmail(comprador.email || "");
        setAtivo(comprador.ativo === true);
        setOpen(true);
    };

    const submit = async (e) => {
        e.preventDefault(); setBusy(true);
        const payload = { nome, cnpj, telefone, email, ativo };
        let success = false;
        try {
            if (editingId) {
                success = await onUpdate(editingId, payload);
            } else {
                success = await onCreate(payload);
            }
            if (success) { handleCloseDrawer(); }
        } catch (error) { console.error("Falha submit comprador:", error); }
        finally { setBusy(false); }
    };

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Compradores</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={handleOpenCreate}>+ Novo Comprador</button>
            </Toolbar>
            <Table
                columns={[
                    { key: "id", header: "ID" },
                    { key: "nome", header: "Nome" },
                    { key: "cnpj", header: "CNPJ" },
                    { key: "telefone", header: "Telefone" },
                    { key: "email", header: "Email" },
                    {
                        key: "ativo", header: "Status", render: (isAtivo) => (
                            <span className={cls("px-2 py-0.5 rounded-full text-xs font-medium", isAtivo ? "bg-emerald-100 text-emerald-800" : "bg-red-100 text-red-800")}>
                                {isAtivo ? "Ativo" : "Inativo"}
                            </span>
                        )
                    },
                    {
                        key: "actions", header: "Ações", render: (_, row) => (
                            <div className="flex gap-2">
                                <button className="px-2 py-1 rounded-lg border text-xs text-blue-600 border-blue-200 hover:bg-blue-50"
                                    onClick={() => handleEdit(row)} title="Editar comprador">
                                    ✏️ Editar
                                </button>
                                {row.ativo && (
                                    <button className="px-2 py-1 rounded-lg border text-xs text-red-600 border-red-200 hover:bg-red-50"
                                        onClick={() => onDelete(row.id)} title="Inativar comprador">
                                        🗑️ Inativar
                                    </button>
                                )}
                            </div>
                        )
                    },
                ]}
                data={data}
                emptyLabel="Nenhum comprador cadastrado"
            />
            <Drawer open={open} onClose={handleCloseDrawer} title={editingId ? "Editar Comprador" : "Adicionar Comprador"}>
                <form onSubmit={submit} className="space-y-3">
                    <TextInput label="Nome" value={nome} onChange={setNome} placeholder="Ex: Recicla Brasil Ltda" required />
                    <TextInput label="CNPJ" value={cnpj} onChange={setCnpj} placeholder="00.000.000/0000-00" />
                    <TextInput label="Telefone" value={telefone} onChange={setTelefone} placeholder="(85) 9...." />
                    <TextInput label="Email" type="email" value={email} onChange={setEmail} placeholder="contato@empresa.com" />
                    <Select
                        label="Status"
                        value={String(ativo)}
                        onChange={(value) => setAtivo(value === 'true')}
                        options={[{ value: 'true', label: "Ativo" }, { value: 'false', label: "Inativo" }]}
                        required
                    />
                    <div className="flex justify-end gap-2 pt-2">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button disabled={busy} className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60">{busy ? "Salvando..." : "Salvar"}</button>
                    </div>
                </form>
            </Drawer>
        </section>
    );
}

function AssociacoesView({ store, onCreate, onUpdate, onDelete , fetchAPI}) {
    // --- Estados Locais (Dados, Loading, Paginação, Filtros) ---
    const [associacoes, setAssociacoes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const [paginaAtual, setPaginaAtual] = useState(0);
    const [totalAssociacoes, setTotalAssociacoes] = useState(0);
    const ITENS_POR_PAGINA = 20;

    const [filtroNome, setFiltroNome] = useState("");

    // --- Estados do Formulário (Drawer) ---
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [nome, setNome] = useState("");
    const [lider, setLider] = useState("");
    const [telefone, setTelefone] = useState("");
    const [cnpj, setCnpj] = useState("");
    const [ativo, setAtivo] = useState(true);

    // Busca o ID do tipo "ASSOCIACAO" no store global (necessário para criar)
    const tipoParceiroAssociacaoId = useMemo(() => {
        if (!store.tiposParceiro) return null;
        const tipoAssoc = store.tiposParceiro.find(t => t.nome === "ASSOCIACAO");
        return tipoAssoc ? tipoAssoc.id : null;
    }, [store.tiposParceiro]);

    // --- useEffect para BUSCAR DADOS ---
    useEffect(() => {
        const fetchAssociacoes = async () => {
            setLoading(true);
            const params = new URLSearchParams();
            if (filtroNome) params.append('nome', filtroNome);
            params.append('skip', paginaAtual * ITENS_POR_PAGINA);
            params.append('limit', ITENS_POR_PAGINA);

            try {
                const data = await fetchAPI(`/associacoes/?${params.toString()}`);
                
                // fetchAPI já joga erro se falhar e já faz o .json()!
                setAssociacoes(data.items);
                setTotalAssociacoes(data.total_count);
            } catch (error) {
                console.error("Erro ao buscar associações:", error);
                alert(error.message);
                setAssociacoes([]);
                setTotalAssociacoes(0);
            } finally {
                setLoading(false);
            }
        };
        fetchAssociacoes();
    }, [filtroNome, paginaAtual, refreshTrigger]);

    // --- Funções do Drawer e Ações ---
    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false); setEditingId(null);
        setNome(""); setLider(""); setTelefone(""); setCnpj(""); setAtivo(true);
    };

    const handleOpenCreate = () => {
        if (!tipoParceiroAssociacaoId) {
            alert("Erro: Tipo 'ASSOCIACAO' não encontrado. Verifique os cadastros.");
            return;
        }
        handleCloseDrawer();
        setOpen(true);
    };

    const handleEdit = (assoc) => {
        setEditingId(assoc.id);
        // CORREÇÃO: O nome agora vem do objeto aninhado 'doador_info'
        setNome(assoc.parceiro_info?.nome || "");
        setLider(assoc.lider || "");
        setTelefone(assoc.telefone || "");
        setCnpj(assoc.cnpj || "");
        setAtivo(assoc.ativo === true);
        setOpen(true);
    };

    const submit = async (e) => {
        e.preventDefault(); setBusy(true);
        let success = false;
        try {
            if (editingId) {
                const payload = { nome, lider, telefone, cnpj, ativo };
                success = await onUpdate(editingId, payload);
            } else {
                const payload = {
                    nome,
                    id_tipo_parceiro: tipoParceiroAssociacaoId,
                    lider, telefone, cnpj, ativo
                };
                success = await onCreate(payload);
            }
            if (success) {
                handleCloseDrawer();
                setRefreshTrigger(t => t + 1); // Força recarregamento da tabela
            }
        } catch (error) { console.error("Falha no submit:", error); }
        finally { setBusy(false); }
    };

    const handleDelete = async (id) => {
        const success = await onDelete(id);
        if (success) setRefreshTrigger(t => t + 1);
    };

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Associações</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={handleOpenCreate}>+ Nova Associação</button>
            </Toolbar>

            {/* Filtros */}
            <Card className="p-4 mb-4">
                <div className="flex gap-3 items-end">
                    <div className="flex-1">
                        <TextInput label="Filtrar por Nome" value={filtroNome} onChange={setFiltroNome} placeholder="Digite o nome..." />
                    </div>
                    <button className="px-3 py-2 rounded-xl border bg-white h-10" onClick={() => setFiltroNome("")}>Limpar</button>
                </div>
            </Card>

            {/* Tabela */}
            {loading && <div className="text-center p-4 text-emerald-600">Carregando associações...</div>}
            {!loading && (
                <>
                    <Table
                        columns={[
                            { key: "doador_info", header: "Nome", render: (doador) => doador?.nome || "-" },
                            { key: "lider", header: "Líder" },
                            { key: "telefone", header: "Telefone" },
                            { key: "cnpj", header: "CNPJ" },
                            {
                                key: "ativo", header: "Status", render: (isAtivo) => (
                                    <span className={cls("px-2 py-0.5 rounded-full text-xs font-medium", isAtivo ? "bg-emerald-100 text-emerald-800" : "bg-red-100 text-red-800")}>
                                        {isAtivo ? "Ativa" : "Inativa"}
                                    </span>
                                )
                            },
                            {
                                key: "actions", header: "Ações", render: (_, row) => (
                                    <div className="flex gap-2">
                                        <button className="px-2 py-1 rounded-lg border text-xs text-blue-600 border-blue-200 hover:bg-blue-50"
                                            onClick={() => handleEdit(row)} title="Editar">
                                            ✏️ Editar
                                        </button>
                                        {row.ativo && (
                                            <button className="px-2 py-1 rounded-lg border text-xs text-red-600 border-red-200 hover:bg-red-50"
                                                onClick={() => handleDelete(row.id)} title="Inativar">
                                                🗑️ Inativar
                                            </button>
                                        )}
                                    </div>
                                )
                            },
                        ]}
                        data={associacoes}
                        emptyLabel="Nenhuma associação encontrada."
                    />
                    {/* Paginação */}
                    {totalAssociacoes > ITENS_POR_PAGINA && (
                        <div className="flex justify-between items-center mt-4">
                            <span className="text-sm text-neutral-600">
                                Mostrando {paginaAtual * ITENS_POR_PAGINA + 1} - {Math.min((paginaAtual + 1) * ITENS_POR_PAGINA, totalAssociacoes)} de {totalAssociacoes}
                            </span>
                            <div className="flex gap-2">
                                <button onClick={() => setPaginaAtual(p => p - 1)} disabled={paginaAtual === 0} className="px-3 py-1 rounded border bg-white disabled:opacity-50">&larr; Anterior</button>
                                <button onClick={() => setPaginaAtual(p => p + 1)} disabled={(paginaAtual + 1) * ITENS_POR_PAGINA >= totalAssociacoes} className="px-3 py-1 rounded border bg-white disabled:opacity-50">Próxima &rarr;</button>
                            </div>
                        </div>
                    )}
                </>
            )}

            <Drawer open={open} onClose={handleCloseDrawer} title={editingId ? "Editar Associação" : "Adicionar Associação"}>
                <form onSubmit={submit} className="space-y-3">
                    <TextInput label="Nome da Associação" value={nome} onChange={setNome} placeholder="Ex: Associação Central" required />
                    <TextInput label="Nome do Líder" value={lider} onChange={setLider} placeholder="Ex: João Silva" />
                    <TextInput label="CNPJ" value={cnpj} onChange={setCnpj} placeholder="00.000.000/0000-00" />
                    <TextInput label="Telefone" value={telefone} onChange={setTelefone} placeholder="(85) 9...." />
                    <Select label="Status" value={String(ativo)} onChange={(value) => setAtivo(value === 'true')} options={[{ value: 'true', label: "Ativa" }, { value: 'false', label: "Inativa" }]} required />
                    <div className="flex justify-end gap-2 pt-2">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button disabled={busy} className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60">{busy ? "Salvando..." : "Salvar"}</button>
                    </div>
                </form>
            </Drawer>
        </section>
    );
}

// --- RECEBIMENTOSVIEW REFATORADA ---
function RecebimentosView({ store, setActive, onCreate, onCancel,fetchAPI }) {
    // --- Estados Locais ---
    const [recebimentos, setRecebimentos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const [paginaAtual, setPaginaAtual] = useState(0);
    const [totalRecebimentos, setTotalRecebimentos] = useState(0);
    const ITENS_POR_PAGINA = 20;

    // --- Filtros ---
    const [dataInicio, setDataInicio] = useState("");
    const [dataFim, setDataFim] = useState("");
    const [filtroParceiroId, setFiltroParceiroId] = useState(""); // Renomeado para Parceiro
    const [filtroMaterialId, setFiltroMaterialId] = useState("");

    // --- Estados do Formulário (Drawer) ---
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    // const [data, setData] = useState(todayISO()); // REMOVIDO: Data é automática no back
    const [tipoParceiroMode, setTipoParceiroMode] = useState("cadastrado"); // 'cadastrado' ou 'outro'
    const [parceiroId, setParceiroId] = useState(""); // Para o Select (ID)
    const [nomeParceiroExterno, setNomeParceiroExterno] = useState(""); // Para o TextInput (Nome)
    const [materialId, setMaterialId] = useState("");
    const [quantidade, setQuantidade] = useState("");

    // --- Opções para Selects ---
    const materiaisOpts = store.materiais.map(m => ({ value: String(m.id), label: m.nome }));
    // 👇 USA A LISTA DE PARCEIROS (que inclui Associações e outros)
    const parceirosOpts = store.parceiros.map(p => ({ value: String(p.id), label: p.nome }));

    // --- Busca de Dados (useEffect) ---
    useEffect(() => {
        const fetchRecebimentos = async () => {
            setLoading(true);
            const params = new URLSearchParams();
            if (dataInicio) params.append('data_inicio', dataInicio);
            if (dataFim) params.append('end_date', dataFim);
            // 👇 Usa o nome correto do filtro da API
            if (filtroParceiroId) params.append('id_parceiro', filtroParceiroId);
            if (filtroMaterialId) params.append('id_material', filtroMaterialId);

            params.append('skip', paginaAtual * ITENS_POR_PAGINA);
            params.append('limit', ITENS_POR_PAGINA);

            try {
                const data = await fetchAPI(`/entradas/?${params.toString()}`);
                
                // fetchAPI já joga erro se falhar e já faz o .json()!
                setRecebimentos(data.items);
                setTotalRecebimentos(data.total_count);
            } catch (error) {
                console.error("Erro buscr recebimentos:", error);
                setRecebimentos([]); setTotalRecebimentos(0);
            } finally { setLoading(false); }
        };
        fetchRecebimentos();
    }, [dataInicio, dataFim, filtroParceiroId, filtroMaterialId, paginaAtual, refreshTrigger]);

    // --- Actions ---
    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false);
        setMaterialId(""); setQuantidade("");
        setParceiroId(""); setNomeParceiroExterno(""); setTipoParceiroMode("cadastrado");
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        setBusy(true);

        // Lógica para decidir qual ID de parceiro usar
        let idParceiroFinal = null;
        if (tipoParceiroMode === 'cadastrado') {
            if (!parceiroId) { alert("Selecione um parceiro."); setBusy(false); return; }
            idParceiroFinal = Number(parceiroId);
        } else {
            alert("Criação rápida de parceiro externo ainda não implementada. Por favor, cadastre-o primeiro na aba 'Cadastros'.");
            setBusy(false);
            return;
        }

        const payload = {
            id_parceiro: idParceiroFinal, // 👈 Envia o campo correto para a API
            id_material: Number(materialId),
            quantidade: parseFloat(quantidade || "0"),
        };

        try {
            const success = await onCreate(payload);
            if (success) {
                handleCloseDrawer();
                setRefreshTrigger(t => t + 1);
            }
        } catch (error) { } finally { setBusy(false); }
    };

    const handleCancel = async (id) => {
        const success = await onCancel(id);
        if (success) setRefreshTrigger(t => t + 1);
    };

    const totalPagina = recebimentos.reduce((s, x) => s + Number(x.quantidade || 0), 0);

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Recebimentos (Doações)</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={() => setOpen(true)}>+ Novo</button>
            </Toolbar>

            <Card className="p-4 mb-4">
                <div className="grid grid-cols-1 md:grid-cols-5 gap-3 items-end">
                    <TextInput label="Data Início" type="date" value={dataInicio} onChange={setDataInicio} />
                    <TextInput label="Data Fim" type="date" value={dataFim} onChange={setDataFim} />
                    <Select label="Material" value={filtroMaterialId} onChange={setFiltroMaterialId} options={materiaisOpts} placeholder="Todos" />
                    <Select label="Parceiro (Doador)" value={filtroParceiroId} onChange={setFiltroParceiroId} options={parceirosOpts} placeholder="Todos" />
                    <button className="px-3 py-2 rounded-xl border bg-white h-10" onClick={() => { setDataInicio(""); setDataFim(""); setFiltroMaterialId(""); setFiltroParceiroId(""); }}>Limpar</button>
                </div>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <StatCard title="Total Registros" value={totalRecebimentos} subtitle="Filtrados" />
                <StatCard title="Qtd. Recebida" value={`${totalPagina.toFixed(1)} Kg`} subtitle="Nesta página" />
            </div>

            {loading && <div className="text-center p-4 text-emerald-600">Carregando...</div>}
            {!loading && (
                <>
                    <Table
                        columns={[
                            { key: "data_entrada", header: "Data", render: v => fmtDateBR(v) },
                            { key: "codigo_lote", header: "Cód. Lote" },
                            // 👇 Lê o nome do objeto parceiro aninhado
                            { key: "parceiro", header: "Parceiro (Doador)", render: (p) => p?.nome || "-" },
                            { key: "material", header: "Material", render: (m) => m?.nome || "-" },
                            { key: "quantidade", header: "Qtd.", render: (v, row) => `${v.toFixed(1)} ${row.material?.unidade_medida || ""}` },
                            {
                                key: "actions", header: "Ações", render: (_, row) => (
                                    <button className="px-2 py-1 rounded-lg border text-xs text-orange-600 border-orange-200 hover:bg-orange-50"
                                        onClick={() => handleCancel(row.id)} title="Cancelar recebimento">
                                        🚫 Cancelar
                                    </button>
                                )
                            },
                        ]}
                        data={recebimentos}
                        emptyLabel="Nenhum recebimento encontrado."
                    />
                    {/* Paginação Simplificada */}
                    {totalRecebimentos > ITENS_POR_PAGINA && (
                        <div className="flex justify-end gap-2 mt-4">
                            <button onClick={() => setPaginaAtual(p => p - 1)} disabled={paginaAtual === 0} className="px-3 py-1 rounded border bg-white disabled:opacity-50">&larr; Anterior</button>
                            <span className="px-3 py-1 text-sm text-neutral-600">Pág. {paginaAtual + 1}</span>
                            <button onClick={() => setPaginaAtual(p => p + 1)} disabled={(paginaAtual + 1) * ITENS_POR_PAGINA >= totalRecebimentos} className="px-3 py-1 rounded border bg-white disabled:opacity-50">Próxima &rarr;</button>
                        </div>
                    )}
                </>
            )}

            <Drawer open={open} onClose={handleCloseDrawer} title="Novo Recebimento (Doação)">
                <form onSubmit={onSubmit} className="space-y-4">
                    <div className="text-sm font-medium text-neutral-700">Fonte da Doação</div>
                    {/* Seletor de Modo (Cadastrado vs Outro) */}
                    <div className="flex gap-2 mb-2">
                        <Pill active={tipoParceiroMode === 'cadastrado'} onClick={() => setTipoParceiroMode('cadastrado')}>Parceiro Cadastrado</Pill>
                        <Pill active={tipoParceiroMode === 'outro'} onClick={() => setTipoParceiroMode('outro')}>Outro (Rápido)</Pill>
                    </div>

                    {tipoParceiroMode === 'cadastrado' ? (
                        <Select label="Selecione o Parceiro" value={parceiroId} onChange={setParceiroId} options={parceirosOpts} required />
                    ) : (
                        <div className="p-3 bg-amber-50 border border-amber-100 rounded-lg text-sm text-amber-800">
                            Para manter a integridade dos dados, por favor cadastre novos parceiros na aba <strong>Cadastros - Parceiros</strong> primeiro.
                        </div>

                    )}

                    <hr className="my-4" />
                    <Select label="Material Recebido" value={materialId} onChange={setMaterialId} options={materiaisOpts} required />
                    <TextInput label="Quantidade" type="number" value={quantidade} onChange={setQuantidade} placeholder="Ex: 150.5" required />

                    <div className="flex justify-end gap-2 pt-4">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button disabled={busy} className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60">{busy ? "Salvar" : "Salvar"}</button>
                    </div>
                </form>
            </Drawer>
        </section>
    );
}

function VendasView({ store, setActive, onCreate, onCancel,fetchAPI }) {
    // Estados locais de dados, filtros e paginação
    const [vendas, setVendas] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const [paginaAtual, setPaginaAtual] = useState(0);
    const [totalVendas, setTotalVendas] = useState(0);
    const ITENS_POR_PAGINA = 20;

    const [dataInicio, setDataInicio] = useState("");
    const [dataFim, setDataFim] = useState("");
    const [filtroComprador, setFiltroComprador] = useState("");
    const [filtroMaterialId, setFiltroMaterialId] = useState("");

    // Estados do formulário (Drawer)
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    const [dataVenda, setDataVenda] = useState(todayISO());
    const [compradorId, setCompradorId] = useState(""); // MUDANÇA: de string 'comprador' para 'compradorId'
    const [itemAtualMaterialId, setItemAtualMaterialId] = useState("");
    const [itemAtualQuantidade, setItemAtualQuantidade] = useState("");
    const [itemAtualPrecoUnit, setItemAtualPrecoUnit] = useState("");
    const [estoqueDisponivel, setEstoqueDisponivel] = useState(null);
    const [itens, setItens] = useState([]);

    // Opções dos Selects (do store global)
    const materiaisOpts = store.materiais.map(m => ({ value: String(m.id), label: m.nome }));
    const compradoresOpts = store.compradores.map(c => ({ value: String(c.id), label: c.nome })); // Para o novo Select
    const getMat = (id) => store.materiais.find(m => m.id === Number(id));

    // useEffect para buscar dados filtrados e paginados
    useEffect(() => {
        const fetchVendasData = async () => {
            setLoading(true);
            const params = new URLSearchParams();
            if (dataInicio) params.append('data_inicio', dataInicio);
            if (dataFim) params.append('end_date', dataFim);
            if (filtroComprador) params.append('comprador', filtroComprador);
            if (filtroMaterialId) params.append('id_material', filtroMaterialId);

            const skip = paginaAtual * ITENS_POR_PAGINA;
            params.append('skip', skip);
            params.append('limit', ITENS_POR_PAGINA);

            try {
                const data = await fetchAPI(`/vendas/?${params.toString()}`);
                setVendas(data.items);
                setTotalVendas(data.total_count);
            } catch (error) {
                console.error("Erro ao buscar vendas:", error);
                alert(error.message);
                setVendas([]);
                setTotalVendas(0);
            } finally {
                setLoading(false);
            }
        };
        fetchVendasData();
    }, [dataInicio, dataFim, filtroComprador, filtroMaterialId, paginaAtual, refreshTrigger]);

    // useEffect para buscar estoque (do Drawer)
    useEffect(() => {
        const fetchEstoque = async () => {
            if (itemAtualMaterialId && !isNaN(Number(itemAtualMaterialId))) {
                try {
                    setEstoqueDisponivel(null);
                    const response = await fetch(`${API_URL}/estoque/${itemAtualMaterialId}`);
                    if (!response.ok) { const errorData = await response.json(); throw new Error(errorData.detail || 'Falha ao buscar estoque'); }
                    const data = await response.json();
                    setEstoqueDisponivel(data);
                } catch (error) {
                    console.error("Erro ao buscar estoque:", error.message);
                    setEstoqueDisponivel(null);
                }
            } else {
                setEstoqueDisponivel(null);
            }
        };
        fetchEstoque();
    }, [itemAtualMaterialId]);

    // Funções do Drawer (handleAddItem, handleRemoveItem)
    const handleAddItem = () => {
        if (!itemAtualMaterialId || !itemAtualQuantidade || !itemAtualPrecoUnit) {
            alert("Preencha Material, Quantidade e Preço Unitário para adicionar.");
            return;
        }
        const qtdNum = parseFloat(itemAtualQuantidade || "0");
        const precoNum = parseFloat(itemAtualPrecoUnit || "0");
        if (isNaN(qtdNum) || qtdNum <= 0 || isNaN(precoNum) || precoNum <= 0) {
            alert("Quantidade e Preço Unitário devem ser números positivos.");
            return;
        }
        if (estoqueDisponivel && qtdNum > estoqueDisponivel.estoque_atual) {
            alert(`Estoque insuficiente. Disponível: ${estoqueDisponivel.estoque_atual} ${estoqueDisponivel.unidade_medida}`);
            return;
        }
        const novoItem = { id_material: Number(itemAtualMaterialId), quantidade_vendida: qtdNum, valor_unitario: precoNum };
        setItens(listaAnterior => [...listaAnterior, novoItem]);
        setItemAtualMaterialId("");
        setItemAtualQuantidade("");
        setItemAtualPrecoUnit("");
        setEstoqueDisponivel(null);
    };

    const handleRemoveItem = (indexParaRemover) => {
        setItens(listaAnterior => listaAnterior.filter((_, index) => index !== indexParaRemover));
    };

    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false); setDataVenda(todayISO());
        setCompradorId(""); setItens([]); setItemAtualMaterialId(""); // MUDANÇA AQUI
        setItemAtualQuantidade(""); setItemAtualPrecoUnit(""); setEstoqueDisponivel(null);
    };

    const handleOpenCreate = () => {
        handleCloseDrawer();
        setOpen(true);
    };

    // Funções de Ação
    const handleSubmitVenda = async () => {
        if (!compradorId) { alert("Selecione um comprador."); return; } // MUDANÇA AQUI
        if (itens.length === 0) { alert("Adicione pelo menos um item à venda."); return; }

        setBusy(true);
        try {
            // MUDANÇA AQUI: Passa 'id_comprador'
            const success = await onCreate({ id_comprador: Number(compradorId), itens: itens });
            if (success) {
                handleCloseDrawer();
                setRefreshTrigger(t => t + 1);
            }
        } catch (error) { /* erro já tratado em onCreate */ }
        finally { setBusy(false); }
    };

    const handleCancel = async (id) => {
        const success = await onCancel(id);
        if (success) {
            setRefreshTrigger(t => t + 1);
        }
    };

    // Cálculos de StatCard (baseados nos dados da página)
    const totalQtdVendida = vendas.reduce((totalVendas, venda) =>
        totalVendas + venda.itens.reduce((totalItens, item) =>
            totalItens + Number(item.quantidade_vendida || 0), 0),
        0);
    const receitaTotal = vendas.reduce((totalVendas, venda) =>
        totalVendas + venda.itens.reduce((totalItens, item) =>
            totalItens + (Number(item.quantidade_vendida || 0) * Number(item.valor_unitario || 0)), 0),
        0);

    // Preparação dos dados para a Tabela
    const itensVendidosData = useMemo(() => {
        return vendas.flatMap(venda =>
            venda.itens.map(item => ({
                ...item,
                venda_id: venda.id,
                data_venda: venda.data_venda,
                codigo: venda.codigo,
                // MUDANÇA AQUI: Pega o objeto 'comprador' aninhado
                comprador: venda.comprador,
            }))
        ).sort((a, b) => new Date(b.data_venda) - new Date(a.data_venda));
    }, [vendas]);

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Vendas</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={handleOpenCreate}>+ Nova venda</button>
            </Toolbar>

            <Card className="p-4 mb-4">
                <div className="grid grid-cols-1 md:grid-cols-5 gap-3 items-end">
                    <TextInput label="Data Início" type="date" value={dataInicio} onChange={setDataInicio} />
                    <TextInput label="Data Fim" type="date" value={dataFim} onChange={setDataFim} />
                    <TextInput label="Filtrar por Comprador" value={filtroComprador} onChange={setFiltroComprador} placeholder="Nome do comprador..." />
                    <Select label="Filtrar por Material" value={filtroMaterialId} onChange={setFiltroMaterialId} options={materiaisOpts} placeholder="Todos os Materiais" />
                    <button className="px-3 py-2 rounded-xl border bg-white h-10" onClick={() => { setDataInicio(""); setDataFim(""); setFiltroComprador(""); setFiltroMaterialId(""); }}>Limpar Filtros</button>
                </div>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <StatCard title="Vendas (Filtradas)" value={totalVendas} />
                <StatCard title="Qtd Vendida (Página)" value={`${totalQtdVendida.toFixed(2)} Kg`} />
                <StatCard title="Receita (Página)" value={money(receitaTotal)} />
            </div>

            {loading && <div className="text-center p-4 text-emerald-600">Carregando vendas...</div>}
            {!loading && (
                <Table
                    columns={[
                        { key: "data_venda", header: "Data", render: v => fmtDateBR(v) },
                        { key: "codigo", header: "Cód. Venda" },
                        // MUDANÇA AQUI: Lê o nome do objeto comprador
                        { key: "comprador", header: "Comprador", render: (comprador) => comprador?.nome || "-" },
                        { key: "material", header: "Material", render: (mat) => mat?.nome || "-" },
                        { key: "quantidade_vendida", header: "Quantidade", render: (v, row) => `${v.toFixed(1)} ${row.material?.unidade_medida || "un"}` },
                        { key: "valor_unitario", header: "Preço Unit.", render: v => money(v) },
                        { key: "total", header: "Total Item", render: (_, row) => money(Number(row.quantidade_vendida || 0) * Number(row.valor_unitario || 0)) },
                        {
                            key: "actions", header: "Ações", render: (_, row) => (
                                <button className="px-2 py-1 rounded-lg border text-xs text-orange-600 border-orange-200 hover:bg-orange-50"
                                    onClick={() => handleCancel(row.venda_id)}
                                    title="Cancelar venda completa">
                                    🚫 Cancelar Venda
                                </button>
                            )
                        },
                    ]}
                    data={itensVendidosData}
                    emptyLabel="Nenhuma venda encontrada para os filtros selecionados."
                />
            )}

            {!loading && totalVendas > ITENS_POR_PAGINA && (
                <div className="flex justify-between items-center mt-4">
                    <span className="text-sm text-neutral-600">
                        Mostrando {paginaAtual * ITENS_POR_PAGINA + 1} - {Math.min((paginaAtual + 1) * ITENS_POR_PAGINA, totalVendas)} de {totalVendas} vendas
                    </span>
                    <div className="flex gap-2">
                        <button onClick={() => setPaginaAtual(p => p - 1)} disabled={paginaAtual === 0} className="px-4 py-2 rounded-xl border bg-white text-sm disabled:opacity-50 disabled:cursor-not-allowed">
                            &larr; Anterior
                        </button>
                        <button onClick={() => setPaginaAtual(p => p + 1)} disabled={(paginaAtual + 1) * ITENS_POR_PAGINA >= totalVendas} className="px-4 py-2 rounded-xl border bg-white text-sm disabled:opacity-50 disabled:cursor-not-allowed">
                            Próxima &rarr;
                        </button>
                    </div>
                </div>
            )}

            <Drawer open={open} onClose={handleCloseDrawer} title="Registrar Nova Venda">
                <div className="space-y-4">
                    <TextInput label="Data" type="date" value={dataVenda} onChange={setDataVenda} required />
                    {/* MUDANÇA AQUI: de TextInput para Select */}
                    <Select
                        label="Comprador"
                        value={compradorId}
                        onChange={setCompradorId}
                        options={compradoresOpts}
                        required
                    />
                    <hr className="my-4" />
                    {/* ... (Resto do formulário de adicionar itens, que está correto) ... */}
                    <h4 className="font-medium text-neutral-700">Adicionar Item</h4>
                    <div className="grid grid-cols-3 gap-2 p-3 border rounded-lg bg-neutral-50">
                        <div className="col-span-3">
                            <Select
                                label="Material"
                                value={itemAtualMaterialId}
                                onChange={setItemAtualMaterialId}
                                options={materiaisOpts}
                                required={itens.length === 0}
                            />
                            {estoqueDisponivel && (<p className="text-xs text-emerald-700 mt-1"> Disponível: {estoqueDisponivel.estoque_atual} {estoqueDisponivel.unidade_medida} </p>)}
                            {!itemAtualMaterialId && <p className="text-xs text-neutral-400 mt-1">Selecione um material para ver o estoque.</p>}
                        </div>
                        <TextInput
                            label="Qtd" type="number" value={itemAtualQuantidade}
                            onChange={(value) => setItemAtualQuantidade(value)}
                            placeholder="Kg" required={itens.length === 0}
                        />
                        <TextInput label="Preço Unit (R$)" type="number" value={itemAtualPrecoUnit} onChange={setItemAtualPrecoUnit} placeholder="Ex: 2.5" required={itens.length === 0} />
                        <div className="flex items-end">
                            <button
                                type="button"
                                onClick={handleAddItem}
                                disabled={!itemAtualMaterialId || !itemAtualQuantidade || !itemAtualPrecoUnit || parseFloat(itemAtualQuantidade || '0') <= 0 || parseFloat(itemAtualPrecoUnit || '0') <= 0 || (estoqueDisponivel === null && itemAtualMaterialId !== "") || (estoqueDisponivel && parseFloat(itemAtualQuantidade || '0') > estoqueDisponivel.estoque_atual)}
                                className="w-full px-3 py-2 rounded-lg bg-blue-500 hover:bg-blue-600 text-white text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                + Adicionar
                            </button>
                        </div>
                        {estoqueDisponivel && parseFloat(itemAtualQuantidade || '0') > estoqueDisponivel.estoque_atual && (
                            <p className="text-xs text-red-600 col-span-3 mt-1">
                                Quantidade maior que o estoque disponível!
                            </p>
                        )}
                    </div>
                    <hr className="my-4" />
                    <h4 className="font-medium text-neutral-700">Itens da Venda ({itens.length})</h4>
                    {itens.length === 0 ? (
                        <p className="text-sm text-neutral-500 text-center py-4">Nenhum item adicionado ainda.</p>
                    ) : (
                        <ul className="space-y-2 max-h-40 overflow-y-auto border rounded-lg p-2 bg-neutral-50">
                            {itens.map((item, index) => {
                                const materialInfo = getMat(item.id_material);
                                return (
                                    <li key={index} className="flex justify-between items-center text-sm p-2 bg-white rounded shadow-sm">
                                        <span>
                                            {item.quantidade_vendida} {materialInfo?.unidade_medida || 'un'} de {materialInfo?.nome || '?'}
                                            @ {money(item.valor_unitario)}
                                        </span>
                                        <button
                                            onClick={() => handleRemoveItem(index)}
                                            className="text-red-500 hover:text-red-700 font-bold"
                                            title="Remover Item"
                                        >
                                            &times;
                                        </button>
                                    </li>
                                );
                            })}
                        </ul>
                    )}
                    <div className="flex justify-end gap-2 pt-4">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button
                            type="button"
                            onClick={handleSubmitVenda}
                            disabled={busy || itens.length === 0 || !compradorId} // MUDANÇA AQUI
                            className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60"
                        >
                            {busy ? "Salvando..." : "Finalizar Venda"}
                        </button>
                    </div>
                </div>
            </Drawer>
        </section>
    );
}

function RelatoriosView({ store,fetchAPI }) {
    const [start, setStart] = useState("");
    const [end, setEnd] = useState("");
    
    // Estados para dados (inicializados com valores seguros)
    const [summaryData, setSummaryData] = useState({ 
        total_recebido: 0, 
        total_comprado_qtd: 0, 
        total_vendido: 0, 
        receita_periodo: 0, 
        total_gasto_compras: 0, 
        lucro_bruto: 0 
    });
    const [porMaterialData, setPorMaterialData] = useState([]);
    const [porParceiroData, setPorParceiroData] = useState([]); // Renomeado para Parceiro
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchDataForReports = async () => {
            setLoading(true);
            try {
                const params = new URLSearchParams();
                if (start) params.append('start_date', start);
                if (end) params.append('end_date', end);
                const queryString = params.toString();

            const [summary, porMaterial, porParceiro] = await Promise.all([
                        fetchAPI(`/relatorio/summary?${queryString}`),
                        fetchAPI(`/relatorio/por-material?${queryString}`),
                        fetchAPI(`/relatorio/por-doador?${queryString}`)
                    ]);
            setSummaryData(summary);
            setPorMaterialData(porMaterial);
            setPorParceiroData(porParceiro);

            } catch (error) {
                console.error("Erro ao buscar relatórios:", error);
                // Zerar dados em caso de erro para não mostrar informações antigas
                setSummaryData({ total_recebido: 0, total_comprado_qtd: 0, total_vendido: 0, receita_periodo: 0, total_gasto_compras: 0, lucro_bruto: 0 });
                setPorMaterialData([]);
                setPorParceiroData([]);
            } finally {
                setLoading(false);
            }
        };
        fetchDataForReports();
    }, [start, end,fetchAPI]);

    // --- Gráficos (Chart.js) ---
    const recChartRef = useRef(null), recChartInstance = useRef(null);
    const revChartRef = useRef(null), revChartInstance = useRef(null);

    useEffect(() => {
        if (!window.Chart || !porMaterialData) return;

        // Preparar dados para os gráficos
        const labels = porMaterialData.map(m => m.nome);
        const dataRecebido = porMaterialData.map(m => m.recebido);
        const dataComprado = porMaterialData.map(m => m.comprado || 0); // Novo dado V3
        const dataReceita = porMaterialData.map(m => m.receita);

        // Limpeza dos gráficos anteriores
        if (recChartInstance.current) recChartInstance.current.destroy();
        if (revChartInstance.current) revChartInstance.current.destroy();

        // Gráfico 1: Entradas (Doação vs Compra) - Stacked Bar seria legal aqui, mas vamos de simples por enquanto
        if (recChartRef.current && porMaterialData.length > 0) {
            recChartInstance.current = new Chart(recChartRef.current, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Doado (Kg)',
                            data: dataRecebido,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        },
                        {
                            label: 'Comprado (Kg)',
                            data: dataComprado,
                            backgroundColor: 'rgba(255, 159, 64, 0.6)',
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { stacked: true }, // Barras empilhadas para ver o total de entrada
                        y: { beginAtZero: true, stacked: true }
                    }
                }
            });
        }

        // Gráfico 2: Receita
        if (revChartRef.current && porMaterialData.length > 0) {
            revChartInstance.current = new Chart(revChartRef.current, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Receita de Vendas (R$)',
                        data: dataReceita,
                        backgroundColor: 'rgba(54, 162, 235, 0.6)'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, ticks: { callback: (v) => money(v) } } }
                }
            });
        }

        return () => {
            if (recChartInstance.current) recChartInstance.current.destroy();
            if (revChartInstance.current) revChartInstance.current.destroy();
        };
    }, [porMaterialData]);

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Relatórios Gerenciais</h2>
                <div className="flex flex-wrap gap-2 items-end">
                    <TextInput label="Início" type="date" value={start} onChange={setStart} />
                    <TextInput label="Fim" type="date" value={end} onChange={setEnd} />
                    <button className="px-3 py-2 rounded-xl border bg-white" onClick={() => { setStart(""); setEnd(""); }}>Limpar</button>
                </div>
            </Toolbar>

            {loading && <div className="text-center p-4 text-emerald-600">Calculando indicadores...</div>}

            {!loading && (
                <>
                    {/* --- CARDS V3 (Expandidos) --- */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                        <StatCard 
                            title="Entradas (Doação)" 
                            value={`${Number(summaryData.total_recebido || 0).toFixed(1)} Kg`} 
                            subtitle="Custo Zero"
                        />
                        <StatCard 
                            title="Entradas (Compra)" 
                            value={`${Number(summaryData.total_comprado_qtd || 0).toFixed(1)} Kg`} 
                            subtitle={`Custo: ${money(summaryData.total_gasto_compras || 0)}`}
                        />
                        <StatCard 
                            title="Saídas (Vendas)" 
                            value={`${Number(summaryData.total_vendido || 0).toFixed(1)} Kg`} 
                            subtitle={`Receita: ${money(summaryData.receita_periodo || 0)}`}
                        />
                        <StatCard 
                            title="Lucro Bruto" 
                            value={money(summaryData.lucro_bruto || 0)} 
                            subtitle="Receita - Custo de Compras"
                        />
                    </div>

                    {/* --- GRÁFICOS --- */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                        <Card className="p-6">
                            <div className="text-sm text-neutral-500 mb-2">Entradas por Material (Kg)</div>
                            <canvas ref={recChartRef} height="140"></canvas>
                        </Card>
                        <Card className="p-6">
                            <div className="text-sm text-neutral-500 mb-2">Receita de Vendas por Material (R$)</div>
                            <canvas ref={revChartRef} height="140"></canvas>
                        </Card>
                    </div>

                    {/* --- TABELAS --- */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Tabela 1: Por Material (V3) */}
                        <Card className="p-6">
                            <div className="text-sm text-neutral-500 mb-3">Balanço por Material</div>
                            <Table
                                columns={[
                                    { key: "nome", header: "Material" },
                                    { key: "recebido", header: "Doado", render: (v, r) => `${Number(v || 0).toFixed(1)}` },
                                    { key: "comprado", header: "Comprado", render: (v, r) => `${Number(v || 0).toFixed(1)}` },
                                    { key: "vendido", header: "Vendido", render: (v, r) => `${Number(v || 0).toFixed(1)}` },
                                    { key: "saldo", header: "Saldo (+/-)", render: (v, r) => `${Number(v || 0).toFixed(1)} ${r.unidade_medida || ''}` },
                                ]}
                                data={porMaterialData}
                                emptyLabel="Sem movimentação no período."
                            />
                        </Card>

                        {/* Tabela 2: Por Parceiro (V3) */}
                        <Card className="p-6">
                            <div className="text-sm text-neutral-500 mb-3">Movimentação por Parceiro</div>
                            <Table
                                columns={[
                                    { key: "nome", header: "Parceiro" },
                                    { key: "tipo_parceiro", header: "Tipo", render: (v) => <span className="text-xs bg-slate-100 px-2 py-1 rounded">{v || '-'}</span> },
                                    { key: "quantidade_recebida", header: "Doou (Kg)", render: (v) => Number(v || 0).toFixed(1) },
                                    { key: "quantidade_comprada", header: "Vendeu (Kg)", render: (v) => Number(v || 0).toFixed(1) },
                                ]}
                                data={porParceiroData}
                                emptyLabel="Nenhum parceiro ativo no período."
                            />
                        </Card>
                    </div>
                </>
            )}
        </section>
    );
}

function ComprasView({ store, setActive, onCreate, onCancel , fetchAPI }) {
    // --- Estados Locais ---
    const [compras, setCompras] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const [paginaAtual, setPaginaAtual] = useState(0);
    const [totalCompras, setTotalCompras] = useState(0);
    const ITENS_POR_PAGINA = 20;

    // --- Filtros ---
    const [dataInicio, setDataInicio] = useState("");
    const [dataFim, setDataFim] = useState("");
    const [filtroParceiroId, setFiltroParceiroId] = useState("");
    const [filtroMaterialId, setFiltroMaterialId] = useState("");

    // --- Estados do Formulário ---
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    const [dataCompra, setDataCompra] = useState(todayISO()); 
    const [parceiroId, setParceiroId] = useState("");
    const [materialId, setMaterialId] = useState("");
    const [quantidade, setQuantidade] = useState("");
    const [valorUnitario, setValorUnitario] = useState(""); 




    const materiaisOpts = store.materiais.map(m => ({ value: String(m.id), label: m.nome }));
    const parceirosOpts = store.parceiros.map(p => ({ value: String(p.id), label: `${p.nome} (${p.tipo_info?.nome})` }));

    // --- Busca de Dados ---
    useEffect(() => {
        const fetchCompras = async () => {
            setLoading(true);
            const params = new URLSearchParams();
            if (dataInicio) params.append('data_inicio', dataInicio);
            if (dataFim) params.append('end_date', dataFim);
            if (filtroParceiroId) params.append('id_parceiro', filtroParceiroId);
            if (filtroMaterialId) params.append('id_material', filtroMaterialId);
            params.append('skip', paginaAtual * ITENS_POR_PAGINA);
            params.append('limit', ITENS_POR_PAGINA);

            try {
                const data = await fetchAPI(`/compras/?${params.toString()}`);
                    
                // fetchAPI já joga erro se falhar e já faz o .json()!
                setCompras(data.items);
                setTotalCompras(data.total_count);
            } catch (error) {
                console.error("Erro buscar compras:", error);
                setCompras([]); setTotalCompras(0);
            } finally { setLoading(false); }
        };
        fetchCompras();
    }, [dataInicio, dataFim, filtroParceiroId, filtroMaterialId, paginaAtual, refreshTrigger]);

    // --- Actions ---
    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false);
        setDataCompra(todayISO());
        setMaterialId(""); setQuantidade(""); setValorUnitario(""); setParceiroId("");
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        setBusy(true);
        const payload = {
            id_parceiro: Number(parceiroId),
            id_material: Number(materialId),
            quantidade: parseFloat(quantidade || "0"),
            valor_pago_unitario: parseFloat(valorUnitario || "0") // NOVO!
        };
        try {
            const success = await onCreate(payload);
            if (success) { handleCloseDrawer(); setRefreshTrigger(t => t + 1); }
        } catch (error) { } finally { setBusy(false); }
    };

    const handleCancel = async (id) => {
        if (await onCancel(id)) setRefreshTrigger(t => t + 1);
    };

    const totalQtd = compras.reduce((s, x) => s + Number(x.quantidade || 0), 0);
    const totalPago = compras.reduce((s, x) => s + (Number(x.quantidade || 0) * Number(x.valor_pago_unitario || 0)), 0);

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Compras (Entradas com Custo)</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={() => setOpen(true)}>+ Nova Compra</button>
            </Toolbar>

            <Card className="p-4 mb-4">
                <div className="grid grid-cols-1 md:grid-cols-5 gap-3 items-end">
                    <TextInput label="Início" type="date" value={dataInicio} onChange={setDataInicio} />
                    <TextInput label="Fim" type="date" value={dataFim} onChange={setDataFim} />
                    <Select label="Material" value={filtroMaterialId} onChange={setFiltroMaterialId} options={materiaisOpts} placeholder="Todos" />
                    <Select label="Fornecedor (Parceiro)" value={filtroParceiroId} onChange={setFiltroParceiroId} options={parceirosOpts} placeholder="Todos" />
                    <button className="px-3 py-2 rounded-xl border bg-white h-10" onClick={() => { setDataInicio(""); setDataFim(""); setFiltroMaterialId(""); setFiltroParceiroId(""); }}>Limpar</button>
                </div>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <StatCard title="Registros (Filtrados)" value={totalCompras} />
                <StatCard title="Qtd. Comprada" value={`${totalQtd.toFixed(1)} Kg`} subtitle="Nesta página" />
                <StatCard title="Total Pago" value={money(totalPago)} subtitle="Nesta página" />
            </div>

            {loading && <div className="text-center p-4 text-emerald-600">Carregando...</div>}
            {!loading && (
                <>
                    <Table
                        columns={[
                            { key: "data_compra", header: "Data", render: v => fmtDateBR(v) },
                            { key: "codigo_compra", header: "Cód." },
                            { key: "parceiro", header: "Fornecedor", render: (p) => p?.nome || "-" },
                            { key: "material", header: "Material", render: (m) => m?.nome || "-" },
                            { key: "quantidade", header: "Qtd.", render: (v, row) => `${v.toFixed(1)} ${row.material?.unidade_medida || ""}` },
                            // NOVAS COLUNAS DE VALOR
                            { key: "valor_pago_unitario", header: "Valor Unit.", render: v => money(v) },
                            { key: "valor_pago_total", header: "Total Pago", render: v => money(v) },
                            {
                                key: "actions", header: "Ações", render: (_, row) => (
                                    <button className="px-2 py-1 rounded-lg border text-xs text-red-600 border-red-200 hover:bg-red-50"
                                        onClick={() => handleCancel(row.id)} title="Cancelar compra">
                                        🚫 Cancelar
                                    </button>
                                )
                            },
                        ]}
                        data={compras}
                        emptyLabel="Nenhuma compra encontrada."
                    />
                    {/* (Bloco de Paginação igual aos outros - copie se quiser) */}
                </>
            )}

            <Drawer open={open} onClose={handleCloseDrawer} title="Registrar Nova Compra">
                <form onSubmit={onSubmit} className="space-y-4">
                    <TextInput label="Data" type="date" value={dataCompra} onChange={setDataCompra} required />
                    <Select label="Fornecedor (Parceiro)" value={parceiroId} onChange={setParceiroId} options={parceirosOpts} required />
                    <Select label="Material" value={materialId} onChange={setMaterialId} options={materiaisOpts} required />
                    <div className="grid grid-cols-2 gap-4">
                        <TextInput label="Quantidade" type="number" value={quantidade} onChange={setQuantidade} placeholder="Ex: 500" required />
                        {/* NOVO INPUT DE VALOR */}
                        <TextInput label="Valor Unit. Pago (R$)" type="number" value={valorUnitario} onChange={setValorUnitario} placeholder="Ex: 0.50" required />
                    </div>
                    <div className="p-3 bg-slate-100 rounded-lg text-right font-medium">
                        Total a Pagar: {money((parseFloat(quantidade || 0) * parseFloat(valorUnitario || 0)))}
                    </div>

                    <div className="flex justify-end gap-2 pt-4">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button disabled={busy} className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60">{busy ? "Salvar Compra" : "Salvar"}</button>
                    </div>
                </form>
            </Drawer>
        </section>
    );
}



// ========== App ==========
function App() {
    const API_URL = "http://127.0.0.1:8000";

    const [token,setToken] = useState(() => localStorage.getItem("rc_token") )

    useEffect(() => {
        console.log(token);
        
        if (!token) {
            window.location.href = "landpage.html";
        }
    }, [token]);
    
    const [active, setActive] = useState("dashboard");



    const [store, setStore] = useState({
        materiais: [],
        associacoes: [],
        compradores: [],
        tiposParceiro: [], 
        parceiros: [],     
        recebimentos: [],
        vendas: [],
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!token) {
            window.localStorage.href = "landpage.html"
        }
    }, [token])

    const fetchAPI = async (endpoint, options = {}) => {
            if (!token) return; 
            const headers = { 
                'Content-Type': 'application/json', 
                'Authorization': `Bearer ${token}`, 
                ...options.headers 
            };
            console.log(`[FETCH] Enviando para ${endpoint}`, headers.Authorization);
            const res = await window.fetch(`${API_URL}${endpoint}`, { ...options, headers });
            if (res.status === 401) { 
                alert("Sessão expirada. Faça login novamente.");
                localStorage.removeItem("rc_token");
                window.location.href = "landPage.html";
                throw new Error("Sessão expirada");
            }
            if (!res.ok) {
                const errorData = await res.json().catch(() => ({}));
                throw new Error(errorData.detail || `${res.status} ${res.statusText}`);
            }
            if (res.status === 204) return null;
            return res.json();
        };

    // --- Busca Inicial de Dados ---
    useEffect(() => {
        if (!token) return; 

        const loadInitialData = async () => {
            setLoading(true);
            console.log("Token verificado. Buscando dados ...");
            try {
                const [mats, assocs, comps, tipos, parcs] = await Promise.all([
                    fetchAPI('/estoque/'),
                    fetchAPI('/associacoes/'),
                    fetchAPI('/compradores/'),
                    fetchAPI('/tipos_parceiro/'),
                    fetchAPI('/parceiros/')
                ]);
                setStore({
                    materiais: mats.items || mats,
                    associacoes: assocs.items || assocs,
                    parceiros: parcs.items || parcs,
                    tipoParceiro: tipos.items || tipos,
                    compradores: comps.items || comps,
                    recebimentos: [], vendas: []
                });
            } catch (err) {
                
                if (err.message !== "Sessão expirada") {
                    console.error("Erro no carregamento:", err);
                }
            } finally {
                setLoading(false);
            }
        };
        loadInitialData();
    }, [token]);

    // --- Helpers de Refresh ---
    const refreshEstoque = async () => {
        try {
            const data = await fetchAPI('/estoque/');
            setStore(s => ({ ...s, materiais: data.items || data }));
        } catch (e) { console.error("Erro refresh estoque:", e); }
    };
    const refreshAssociacoes = async () => {
        try {
            const data = await fetchAPI('/associacoes/');
            setStore(s => ({ ...s, associacoes: data.items || data }));
        } catch (e) { console.error("Erro refresh associacoes:", e); }
    };
    const refreshCompradores = async () => {
        try {
            const data = await fetchAPI('/compradores/');
            setStore(s => ({ ...s, compradores: data.items || data }));
        } catch (e) { console.error("Erro refresh compradores:", e); }
    };
    const refreshTiposParceiro = async () => {
        try {
            const data = await fetchAPI('/tipos_parceiro/');
            console.log(data);
            
            setStore(s => ({ ...s, tiposParceiro: data }));
        } catch (e) { console.error("Erro refresh tipos parceiro:", e); }
    };
    const refreshParceiros = async () => {
        try {
            const data = await fetchAPI('/parceiros/');
            setStore(s => ({ ...s, parceiros: data.items || data }));
        } catch (e) { console.error("Erro refresh parceiros:", e); }
    };

    // --- Funções de Ação (CREATE/UPDATE/DELETE) ---

    // MATERIAIS
    const createMaterial = async (payload) => {
        const payloadAPI = { ...payload, unidade_medida: payload.unidade };
        try {
            const res = await window.fetch(`${API_URL}/materiais/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payloadAPI) });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshEstoque(); return true;
        } catch (e) { alert(e.message); return false; }
    };
    const updateMaterial = async (id, payload) => {
        const payloadAPI = { ...payload, unidade_medida: payload.unidade };
        try {
            const res = await window.fetch(`${API_URL}/materiais/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payloadAPI) });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshEstoque(); return true;
        } catch (e) { alert(e.message); return false; }
    };

    // TIPOS DE PARCEIRO (Novo)
    const createTipoParceiro = async (payload) => {
        try {
            const res = await window.fetch(`${API_URL}/tipos_parceiro/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshTiposParceiro(); return true;
        } catch (e) { alert(e.message); return false; }
    };

    // COMPRADORES
    const createComprador = async (payload) => {
        try {
            const res = await window.fetch(`${API_URL}/compradores/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshCompradores(); return true;
        } catch (e) { alert(e.message); return false; }
    };
    const updateComprador = async (id, payload) => {
        try {
            const res = await window.fetch(`${API_URL}/compradores/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshCompradores(); return true;
        } catch (e) { alert(e.message); return false; }
    };
    const deleteComprador = async (id) => {
        if (!confirm("Inativar comprador?")) return false;
        try {
            const res = await window.fetch(`${API_URL}/compradores/${id}`, { method: 'DELETE' });
            if (res.status !== 204) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshCompradores(); return true;
        } catch (e) { alert(e.message); return false; }
    };

    // ASSOCIAÇÕES (Agora cria Parceiro + Associacao)
    const createAssociacao = async (payload) => {
        try {
            const res = await window.fetch(`${API_URL}/associacoes/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshAssociacoes(); await refreshParceiros(); return true;
        } catch (e) { alert(e.message); return false; }
    };
    const updateAssociacao = async (id, payload) => {
        try {
            const res = await window.fetch(`${API_URL}/associacoes/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshAssociacoes(); await refreshParceiros(); return true;
        } catch (e) { alert(e.message); return false; }
    };
    const deleteAssociacao = async (id) => {
        if (!confirm("Inativar associação?")) return false;
        try {
            const res = await window.fetch(`${API_URL}/associacoes/${id}`, { method: 'DELETE' });
            if (res.status !== 204) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshAssociacoes(); await refreshParceiros(); return true;
        } catch (e) { alert(e.message); return false; }
    };

    // RECEBIMENTOS (Agora usa /recebimentos/ e id_parceiro)
    const createRecebimento = async (payload) => {
        // Payload esperado: { id_parceiro, id_material, quantidade }
        try {
            const res = await window.fetch(`${API_URL}/recebimentos/`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
            });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro ao criar recebimento"); }
            await refreshEstoque(); return true;
        } catch (e) { alert(e.message); return false; }
    };
    const cancelRecebimento = async (id) => {
        if (!confirm("Cancelar recebimento?")) return false;
        try {
            const res = await window.fetch(`${API_URL}/recebimentos/${id}`, { method: 'DELETE' });
            if (res.status !== 204) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshEstoque(); return true;
        } catch (e) { alert(e.message); return false; }
    };

    // VENDAS (Usa id_comprador)
    const createVenda = async (payload) => {
        try {
            const res = await window.fetch(`${API_URL}/vendas/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Erro ao criar venda"); }
            await refreshEstoque(); return true;
        } catch (e) { alert(e.message); return false; }
    };
    const cancelVenda = async (id) => {
        if (!confirm("Cancelar venda?")) return false;
        try {
            const res = await window.fetch(`${API_URL}/vendas/${id}`, { method: 'DELETE' });
            if (res.status !== 204) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshEstoque(); return true;
        } catch (e) { alert(e.message); return false; }
    };
    const createCompra = async (payload) => {

        try {
            const res = await window.fetch(`${API_URL}/compras/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Erro ao registrar compra");
            }
            await refreshMateriaisComEstoque();
            return true;
        } catch (e) { alert(e.message); return false; }
    };


    const cancelCompra = async (id) => {
        if (!confirm("Cancelar esta compra? O estoque será reduzido e o valor estornado nos relatórios.")) return false;
        try {
            const res = await window.fetch(`${API_URL}/compras/${id}`, { method: 'DELETE' });
            if (res.status !== 204) { const d = await res.json(); throw new Error(d.detail || "Erro"); }
            await refreshMateriaisComEstoque(); // Atualiza estoque!
            return true;
        } catch (e) { alert(e.message); return false; }
    };
    const handleLogout = () => {
        localStorage.removeItem("rc_token");
        window.location.href = "landpage.html";
    };

    if (!token) return null;

    return (
        <div className="min-h-screen bg-slate-50">
             <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-lg bg-emerald-600 grid place-items-center text-white font-bold shadow-sm">RC</div>
                        <div className="flex-1">
                            <div className="font-semibold leading-tight text-slate-900">Rede de Catadores</div>
                            <div className="text-xs text-slate-500">Sistema de Gestão v3.0</div>
                        </div>
                    </div>
                    <button onClick={handleLogout} className="text-sm text-slate-500 hover:text-red-600 flex items-center gap-1 font-medium">
                        Sair 🚪
                    </button>
                </div>
            </header>

            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-[240px,1fr] gap-6 px-4 py-6">
                <aside className="md:sticky md:top-20 h-max">
                    <nav className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-6">
                        <div>
                            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 px-2">Principal</div>
                            <div className="flex flex-col gap-1">
                                <Pill active={active==="dashboard"} onClick={()=>setActive("dashboard")}>📊 Dashboard</Pill>
                            </div>
                        </div>
                        <div>
                            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 px-2">Operação</div>
                            <div className="flex flex-col gap-1">
                                <Pill active={active==="recebimentos"} onClick={()=>setActive("recebimentos")}>📥 Recebimentos (Doações)</Pill>
                                <Pill active={active==="compras"} onClick={()=>setActive("compras")}>💸 Compras</Pill>
                                <Pill active={active==="vendas"} onClick={()=>setActive("vendas")}>📤 Vendas</Pill>
                            </div>
                        </div>
                        <div>
                             <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 px-2">Cadastros</div>
                             <div className="flex flex-col gap-1">
                                <Pill active={active==="materiais"} onClick={()=>setActive("materiais")}>📦 Materiais</Pill>
                                <Pill active={active==="associacoes"} onClick={()=>setActive("associacoes")}>🤝 Associações</Pill>
                                <Pill active={active==="compradores"} onClick={()=>setActive("compradores")}>💰 Compradores</Pill>
                                <Pill active={active==="tipoParceiros"} onClick={()=>setActive("tipoParceiros")}>🏷️ Tipos de Parceiro</Pill>
                             </div>
                        </div>
                        <div>
                            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 px-2">Análise</div>
                            <div className="flex flex-col gap-1">
                                <Pill active={active==="relatorios"} onClick={()=>setActive("relatorios")}>📈 Relatórios</Pill>
                            </div>
                        </div>
                    </nav>
                </aside>
                
                <main>
                    {loading ? (
                        <div className="flex items-center justify-center h-64 text-slate-500">
                            <svg className="animate-spin h-8 w-8 text-emerald-600 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            Carregando dados...
                        </div>
                    ) : (
                        <>
                            {active === "dashboard" && <DashboardView store={store} />}
                            {active === "materiais" && <MateriaisView data={store.materiais} onCreate={createMaterial} onUpdate={updateMaterial} />}
                            {active === "associacoes" && <AssociacoesView store={store} data={store.associacoes} onCreate={createAssociacao} onUpdate={updateAssociacao} onDelete={deleteAssociacao} fetchAPI={fetchAPI}  />}
                            {active === "compradores" && <CompradoresView data={store.compradores} onCreate={createComprador} onUpdate={updateComprador} onDelete={deleteComprador} />}
                            {active === "tipoParceiros" && <TipoParceiroView data={store.tiposParceiro} onCreate={createTipoParceiro} />}
                            {active === "recebimentos" && <RecebimentosView store={store} setActive={setActive} onCreate={createRecebimento} onCancel={cancelRecebimento} fetchAPI={fetchAPI} />}
                            {active === "compras" && <ComprasView store={store} setActive={setActive} onCreate={createCompra} onCancel={cancelCompra} fetchAPI={fetchAPI}/>}
                            {active === "vendas" && <VendasView store={store} setActive={setActive} onCreate={createVenda} onCancel={cancelVenda} fetchAPI={fetchAPI}/>}
                            {active === "relatorios" && <RelatoriosView store={store} fetchAPI={fetchAPI}/>}
                        </>
                    )}
                </main>
            </div>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);