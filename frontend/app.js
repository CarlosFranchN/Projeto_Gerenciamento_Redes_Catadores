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
const inRange = (iso, startISO, endISO) => {
    if (!iso) return false;
    const t = new Date(iso).getTime();
    if (isNaN(t)) return false;
    const a = startISO ? new Date(startISO).getTime() : -Infinity;
    const b = endISO
        ? new Date(endISO).getTime() + 24 * 60 * 60 * 1000 - 1
        : Infinity;
    return t >= a && t <= b;
};

// ========== UI building blocks ==========
const Card = ({ children, className }) => (<div className={cls("rounded-2xl border border-black/5 bg-white shadow-sm", className)}>{children}</div>);
const StatCard = ({ title, value, subtitle }) => (<div className="bg-white/80 rounded-2xl shadow-sm p-5 border border-black/5"> <div className="text-sm text-neutral-500">{title}</div> <div className="text-3xl font-semibold mt-1">{value}</div> {subtitle && <div className="text-xs mt-2 text-neutral-400">{subtitle}</div>} </div>);
const Toolbar = ({ children }) => (<div className="flex flex-col sm:flex-row sm:items-center gap-3 justify-between mb-4">{children}</div>);
const Pill = ({ active, onClick, children }) => (<button onClick={onClick} className={cls("px-4 py-2 rounded-full border text-sm transition", active ? "bg-emerald-600 text-white border-emerald-700" : "bg-white text-neutral-700 border-neutral-200 hover:bg-neutral-50")} > {children} </button>);
const Table = ({ columns, data, emptyLabel = "Sem dados" }) => (<div className="overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-sm"> <div className="overflow-x-auto"> <table className="min-w-full text-sm"> <thead className="bg-neutral-50"> <tr> {columns.map(c => (<th key={c.key} className="text-left px-4 py-3 font-medium text-neutral-600">{c.header}</th>))} </tr> </thead> <tbody> {data.length === 0 ? (<tr><td colSpan={columns.length} className="px-4 py-10 text-center text-neutral-400">{emptyLabel}</td></tr>) : (data.map((row, i) => (<tr key={row.id ?? i} className={i % 2 ? "bg-white" : "bg-neutral-50/40"}> {columns.map(c => (<td key={c.key} className="px-4 py-3 text-neutral-800"> {c.render ? c.render(row[c.key], row) : row[c.key]} </td>))} </tr>)))} </tbody> </table> </div> </div>);
const Drawer = ({ open, onClose, title, children }) => (<div className={cls("fixed inset-0 z-50 transition", open ? "pointer-events-auto" : "pointer-events-none")}> <div className={cls("absolute inset-0 bg-black/40 transition-opacity", open ? "opacity-100" : "opacity-0")} onClick={onClose} /> <div className={cls("absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-xl border-l border-neutral-200 p-6 transition-transform", open ? "translate-x-0" : "translate-x-full")} role="dialog" aria-modal="true"> <div className="flex items-start justify-between mb-4"> <h3 className="text-lg font-semibold">{title}</h3> <button onClick={onClose} className="rounded-full w-8 h-8 grid place-items-center border border-neutral-200 hover:bg-neutral-50" aria-label="Fechar">×</button> </div> {children} </div> </div>);
const TextInput = ({ label, value, onChange, placeholder, type = "text", required }) => { const id = useMemo(() => Math.random().toString(36).slice(2), []); return (<label className="block"> <span className="text-sm text-neutral-600">{label}</span> <input id={id} type={type} value={value} required={required} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} className="mt-1 w-full rounded-xl border border-neutral-200 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-emerald-500" /> </label>); };
const Select = ({ label, value, onChange, options, placeholder = "Selecione...", required }) => { const id = useMemo(() => Math.random().toString(36).slice(2), []); return (<label className="block"> <span className="text-sm text-neutral-600">{label}</span> <select id={id} value={value} required={required} onChange={(e) => onChange(e.target.value)} className="mt-1 w-full rounded-xl border border-neutral-200 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-emerald-500" > <option value="">{placeholder}</option> {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)} </select> </label>); };

// ========== Views ==========
function DashboardView({ store }) {
    const recMes = store.recebimentos.filter(r => sameYM(r.data_entrada));
    const venMes = store.vendas.filter(v => sameYM(v.data_venda));
    const totalRecMes = recMes.reduce((s, x) => s + Number(x.quantidade || 0), 0);
    const receitaMes = venMes.reduce((totalVendas, venda) =>
        totalVendas + venda.itens.reduce((totalItens, item) =>
            totalItens + (Number(item.quantidade_vendida || 0) * Number(item.valor_unitario || 0)), 0),
        0);

    return (
        <section>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <StatCard title="Materiais" value={store.materiais.length} subtitle="Cadastrados (com estoque)" />
                <StatCard title="Associações" value={store.associacoes.length} subtitle="Ativas" />
                <StatCard title="Recebimentos (mês)" value={`${totalRecMes.toFixed(1)} Kg`} subtitle="Somatório" />
                <StatCard title="Receita (mês)" value={money(receitaMes)} subtitle="Vendas" />
            </div>
            <Card className="p-6">
                <h3 className="text-lg font-semibold mb-2">Boas-vindas 👋</h3>
                <p className="text-neutral-600 text-sm leading-relaxed">
                    Sistema de Gestão da Rede de Catadores. Use o menu ao lado para navegar.
                </p>
            </Card>
        </section>
    );
}

function MateriaisView({ data, onCreate, onUpdate }) {
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
        const payload = { nome, categoria, unidade };
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
                <h2 className="text-xl font-semibold">Materiais</h2>
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
                    <TextInput label="Unidade" value={unidade} onChange={setUnidade} placeholder="Ex: Kg, un" required />
                    <div className="flex justify-end gap-2 pt-2">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button disabled={busy} className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60">{busy ? "Salvando..." : "Salvar"}</button>
                    </div>
                </form>
            </Drawer>
        </section>
    );
}

function AssociacoesView({ data, onCreate, onUpdate, onDelete }) {
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    const [nome, setNome] = useState("");
    const [cnpj, setCnpj] = useState("");
    const [lider, setLider] = useState("");
    const [telefone, setTelefone] = useState("");
    const [ativo, setAtivo] = useState(true);
    const [editingId, setEditingId] = useState(null);

    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false); setNome(""); setLider(""); setTelefone("");
        setCnpj(""); setAtivo(true); setEditingId(null);
    };

    const handleOpenCreate = () => {
        handleCloseDrawer();
        setOpen(true);
    };

    const submit = async (e) => {
        e.preventDefault(); setBusy(true);
        const payload = { nome, cnpj, lider, telefone, ativo };
        let success = false;
        try {
            if (editingId) {
                success = await onUpdate(editingId, payload);
            } else {
                success = await onCreate(payload);
            }
            if (success) { handleCloseDrawer(); }
        } catch (error) { console.error("Falha no submit associação:", error); }
        finally { setBusy(false); }
    };

    const handleEdit = (assoc) => {
        setEditingId(assoc.id);
        setNome(assoc.nome || "");
        setLider(assoc.lider || "");
        setTelefone(assoc.telefone || "");
        setCnpj(assoc.cnpj || "");
        setAtivo(assoc.ativo === true);
        setOpen(true);
    };

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Associações</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={handleOpenCreate}>+ Nova associação</button>
            </Toolbar>
            <Table
                columns={[
                    { key: "id", header: "ID" },
                    { key: "nome", header: "Nome" },
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
                                    onClick={() => handleEdit(row)} title="Editar associação">
                                    ✏️ Editar
                                </button>
                                {row.ativo && (
                                    <button className="px-2 py-1 rounded-lg border text-xs text-red-600 border-red-200 hover:bg-red-50"
                                        onClick={() => onDelete(row.id)} title="Inativar associação">
                                        🗑️ Inativar
                                    </button>
                                )}
                            </div>
                        )
                    },
                ]}
                data={data}
                emptyLabel="Nenhuma associação cadastrada"
            />
            <Drawer open={open} onClose={handleCloseDrawer} title={editingId ? "Editar Associação" : "Adicionar Associação"}>
                <form onSubmit={submit} className="space-y-3">
                    <TextInput label="Nome" value={nome} onChange={setNome} placeholder="Ex: Associação Central" required />
                    <TextInput label="CNPJ" value={cnpj} onChange={setCnpj} placeholder="00.000.000/0000-00" />
                    <TextInput label="Nome do Líder/Responsável" value={lider} onChange={setLider} placeholder="Ex: João Silva" />
                    <TextInput label="Telefone" value={telefone} onChange={setTelefone} placeholder="(85) 9...." />
                    <Select
                        label="Status"
                        value={String(ativo)}
                        onChange={(value) => setAtivo(value === 'true')}
                        options={[{ value: 'true', label: "Ativa" }, { value: 'false', label: "Inativa" }]}
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

function RecebimentosView({ store, setActive, onCreate, onCancel }) {
    const [open, setOpen] = useState(false);
    const [data, setData] = useState(todayISO());
    const [materialId, setMaterialId] = useState("");
    const [associacaoId, setAssociacaoId] = useState("");
    const [quantidade, setQuantidade] = useState("");
    const [busy, setBusy] = useState(false);

    const materiaisOpts = store.materiais.map(m => ({ value: String(m.id), label: m.nome }));
    const assocOpts = store.associacoes.map(a => ({ value: String(a.id), label: a.nome }));

    const handleCloseDrawer = () => {
        setOpen(false); setBusy(false); setData(todayISO());
        setMaterialId(""); setAssociacaoId(""); setQuantidade("");
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        if (!store.materiais.length) { alert("Cadastre materiais primeiro."); setActive("materiais"); return; }
        if (!store.associacoes.length) { alert("Cadastre associações primeiro."); setActive("associacoes"); return; }
        setBusy(true);

        const payload = {
            materialId: Number(materialId),
            associacaoId: Number(associacaoId),
            quantidade: parseFloat(quantidade || "0"),
        };

        try {
            const success = await onCreate(payload);
            if (success) { handleCloseDrawer(); }
        } catch (error) { /* erro já tratado em onCreate */ }
        finally { setBusy(false); }
    };

    const total = store.recebimentos.reduce((s, x) => s + Number(x.quantidade || 0), 0);

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Recebimentos</h2>
                <div className="flex gap-2">
                    <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={() => setOpen(true)}>+ Novo recebimento</button>
                </div>
            </Toolbar>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <StatCard title="Entradas registradas" value={store.recebimentos.length} />
                <StatCard title="Total recebido" value={`${total.toFixed(1)} Kg`} />
                <Card className="p-5">
                    <div className="text-sm text-neutral-500">Ações rápidas</div>
                    <div className="mt-2 flex gap-2">
                        <button className="px-3 py-1.5 rounded-lg border text-sm" onClick={() => setActive("materiais")}>+ Material</button>
                        <button className="px-3 py-1.5 rounded-lg border text-sm" onClick={() => setActive("associacoes")}>+ Associação</button>
                    </div>
                </Card>
            </div>
            <Table
                columns={[
                    { key: "data_entrada", header: "Data", render: v => fmtDateBR(v) },
                    { key: "codigo_lote", header: "Cód. Lote" },
                    { key: "material", header: "Material", render: (_, row) => row.material?.nome || "-" },
                    { key: "associacao", header: "Associação", render: (_, row) => row.associacao?.nome || "-" },
                    { key: "quantidade", header: "Quantidade", render: (v, row) => `${v.toFixed(1)} ${row.material?.unidade_medida || ""}` },
                    {
                        key: "actions", header: "Ações", render: (_, row) => (
                            <button className="px-2 py-1 rounded-lg border text-xs text-orange-600 border-orange-200 hover:bg-orange-50"
                                onClick={() => onCancel(row.id)} title="Cancelar recebimento">
                                🚫 Cancelar
                            </button>
                        )
                    },
                ]}
                data={store.recebimentos}
                emptyLabel="Nenhum recebimento cadastrado"
            />
            <Drawer open={open} onClose={handleCloseDrawer} title="Adicionar Recebimento">
                <form onSubmit={onSubmit} className="space-y-3">
                    <TextInput label="Data" type="date" value={data} onChange={setData} required />
                    <Select label="Material" value={materialId} onChange={setMaterialId} options={materiaisOpts} required />
                    <Select label="Associação" value={associacaoId} onChange={setAssociacaoId} options={assocOpts} required />
                    <TextInput label="Quantidade" type="number" value={quantidade} onChange={setQuantidade} placeholder="Ex: 120" required />
                    <div className="flex justify-end gap-2 pt-2">
                        <button type="button" className="px-4 py-2 rounded-xl border" onClick={handleCloseDrawer}>Cancelar</button>
                        <button disabled={busy} className="px-4 py-2 rounded-xl bg-emerald-600 text-white disabled:opacity-60">{busy ? "Salvando..." : "Salvar"}</button>
                    </div>
                </form>
            </Drawer>
        </section>
    );
}

function VendasView({ store, setActive, onCreate, onCancel }) {
    const [open, setOpen] = useState(false);
    const [busy, setBusy] = useState(false);
    const [dataVenda, setDataVenda] = useState(todayISO());
    const [comprador, setComprador] = useState("");
    const [itemAtualMaterialId, setItemAtualMaterialId] = useState("");
    const [itemAtualQuantidade, setItemAtualQuantidade] = useState("");
    const [itemAtualPrecoUnit, setItemAtualPrecoUnit] = useState("");
    const [estoqueDisponivel, setEstoqueDisponivel] = useState(null);
    const [itens, setItens] = useState([]);

    const materiaisOpts = store.materiais.map(m => ({ value: String(m.id), label: m.nome }));

    const getMat = (id) => store.materiais.find(m => m.id === Number(id));

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
        setComprador(""); setItens([]); setItemAtualMaterialId("");
        setItemAtualQuantidade(""); setItemAtualPrecoUnit(""); setEstoqueDisponivel(null);
    };

    const handleOpenCreate = () => {
        handleCloseDrawer();
        setOpen(true);
    };

    const handleSubmitVenda = async () => {
        if (!comprador) { alert("Informe o nome do comprador."); return; }
        if (itens.length === 0) { alert("Adicione pelo menos um item à venda."); return; }

        setBusy(true);
        try {
            const success = await onCreate({ nomeComprador: comprador, itens: itens });
            if (success) { handleCloseDrawer(); }
        } catch (error) { /* erro já tratado em onCreate */ }
        finally { setBusy(false); }
    };

    const totalQtdVendida = store.vendas.reduce((totalVendas, venda) =>
        totalVendas + venda.itens.reduce((totalItens, item) =>
            totalItens + Number(item.quantidade_vendida || 0), 0),
        0);

    const receitaTotal = store.vendas.reduce((totalVendas, venda) =>
        totalVendas + venda.itens.reduce((totalItens, item) =>
            totalItens + (Number(item.quantidade_vendida || 0) * Number(item.valor_unitario || 0)), 0),
        0);

    const itensVendidosData = useMemo(() => {
        return store.vendas.flatMap(venda =>
            venda.itens.map(item => ({
                ...item,
                venda_id: venda.id,
                data_venda: venda.data_venda,
                codigo: venda.codigo,
                comprador: venda.comprador,
            }))
        ).sort((a, b) => new Date(b.data_venda) - new Date(a.data_venda));
    }, [store.vendas]);

    return (
        <section>
            <Toolbar>
                <h2 className="text-xl font-semibold">Vendas</h2>
                <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white" onClick={handleOpenCreate}>+ Nova venda</button>
            </Toolbar>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <StatCard title="Vendas registradas" value={store.vendas.length} />
                <StatCard title="Quantidade vendida (Total)" value={`${totalQtdVendida.toFixed(2)} Kg`} />
                <StatCard title="Receita total" value={money(receitaTotal)} />
            </div>
            <Table
                columns={[
                    { key: "data_venda", header: "Data", render: v => fmtDateBR(v) },
                    { key: "codigo", header: "Cód. Venda" },
                    { key: "comprador", header: "Comprador" },
                    { key: "material", header: "Material", render: (mat) => mat?.nome || "-" },
                    { key: "quantidade_vendida", header: "Quantidade", render: (v, row) => `${v} ${row.material?.unidade_medida || "un"}` },
                    { key: "valor_unitario", header: "Preço Unit.", render: v => money(v) },
                    { key: "total", header: "Total Item", render: (_, row) => money(Number(row.quantidade_vendida || 0) * Number(row.valor_unitario || 0)) },
                    {
                        key: "actions", header: "Ações", render: (_, row) => (
                            <button className="px-2 py-1 rounded-lg border text-xs text-orange-600 border-orange-200 hover:bg-orange-50"
                                onClick={() => onCancel(row.venda_id)}
                                title="Cancelar venda completa">
                                🚫 Cancelar Venda
                            </button>
                        )
                    },
                ]}
                data={itensVendidosData}
                emptyLabel="Nenhuma venda registrada"
            />
            <Drawer open={open} onClose={handleCloseDrawer} title="Registrar Nova Venda">
                <div className="space-y-4">
                    <TextInput label="Data" type="date" value={dataVenda} onChange={setDataVenda} required />
                    <TextInput label="Nome do Comprador" value={comprador} onChange={setComprador} placeholder="Ex: Recicla Brasil Ltda" required />
                    <hr className="my-4" />
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
                            disabled={busy || itens.length === 0 || !comprador}
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

function RelatoriosView({ store }) {
    const [start, setStart] = useState("");
    const [end, setEnd] = useState("");
    const [summaryData, setSummaryData] = useState({ total_recebido: 0, total_vendido: 0, receita_periodo: 0 });
    const [porMaterialData, setPorMaterialData] = useState([]);
    const [porAssociacaoData, setPorAssociacaoData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchDataForReports = async () => {
            setLoading(true);
            try {
                const params = new URLSearchParams();
                if (start) params.append('start_date', start);
                if (end) params.append('end_date', end);
                const queryString = params.toString();

                const [summaryRes, porMaterialRes, porAssocRes] = await Promise.all([
                    fetch(`${API_URL}/relatorio/relatorio?${queryString}`),
                    fetch(`${API_URL}/relatorio/por-material?${queryString}`),
                    fetch(`${API_URL}/relatorio/por-associacao?${queryString}`)
                ]);

                if (!summaryRes.ok) { throw new Error(`Erro Sumário: ${summaryRes.statusText}`); }
                if (!porMaterialRes.ok) { throw new Error(`Erro Por Material: ${porMaterialRes.statusText}`); }
                if (!porAssocRes.ok) { throw new Error(`Erro Por Associação: ${porAssocRes.statusText}`); }

                const summaryJson = await summaryRes.json();
                const porMaterialJson = await porMaterialRes.json();
                const porAssocJson = await porAssocRes.json();

                setSummaryData(summaryJson);
                setPorMaterialData(porMaterialJson);
                setPorAssociacaoData(porAssocJson);

            } catch (error) {
                console.error("Erro ao buscar dados dos relatórios:", error);
                alert(`Erro ao carregar relatórios: ${error.message}. Verifique o console e o backend.`);
                setSummaryData({ total_recebido: 0, total_vendido: 0, receita_periodo: 0 });
                setPorMaterialData([]);
                setPorAssociacaoData([]);
            } finally {
                setLoading(false);
            }
        };
        fetchDataForReports();
    }, [start, end]);

    const recChartRef = useRef(null), recChartInstance = useRef(null);
    const revChartRef = useRef(null), revChartInstance = useRef(null);

    useEffect(() => {
        if (!window.Chart || !porMaterialData) { // Simplificado
            if (recChartInstance.current) recChartInstance.current.destroy();
            if (revChartInstance.current) revChartInstance.current.destroy();
            recChartInstance.current = null;
            revChartInstance.current = null;
            return;
        }

        const recLabels = porMaterialData.map(m => m.nome);
        const recData = porMaterialData.map(m => m.recebido);
        const revLabels = porMaterialData.map(m => m.nome);
        const revData = porMaterialData.map(m => m.receita);

        if (recChartInstance.current) recChartInstance.current.destroy();
        if (revChartInstance.current) revChartInstance.current.destroy();

        if (recChartRef.current && recData.length > 0) { // Adicionado verificação de dados
            recChartInstance.current = new Chart(recChartRef.current, {
                type: "bar",
                data: { labels: recLabels, datasets: [{ label: "Recebido (Kg)", data: recData, backgroundColor: 'rgba(75, 192, 192, 0.6)' }] },
                options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
            });
        }
        if (revChartRef.current && revData.length > 0) { // Adicionado verificação de dados
            revChartInstance.current = new Chart(revChartRef.current, {
                type: "bar",
                data: { labels: revLabels, datasets: [{ label: "Receita (R$)", data: revData, backgroundColor: 'rgba(54, 162, 235, 0.6)' }] },
                options: {
                    responsive: true, plugins: { legend: { display: false } },
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
                <h2 className="text-xl font-semibold">Relatórios</h2>
                <div className="flex flex-wrap gap-2 items-end">
                    <TextInput label="Início" type="date" value={start} onChange={setStart} />
                    <TextInput label="Fim" type="date" value={end} onChange={setEnd} />
                    <button className="px-3 py-2 rounded-xl border bg-white" onClick={() => { setStart(""); setEnd(""); }}>Limpar Datas</button>
                </div>
            </Toolbar>
            {loading && <div className="text-center p-4 text-emerald-600">Carregando relatórios...</div>}
            {!loading && (
                <>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <StatCard title="Total recebido" value={`${summaryData.total_recebido.toFixed(1)} Kg`} subtitle="No período selecionado" />
                        <StatCard title="Total vendido" value={`${summaryData.total_vendido.toFixed(1)} Kg`} subtitle="No período selecionado" />
                        <StatCard title="Receita no período" value={money(summaryData.receita_periodo)} />
                    </div>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                        <Card className="p-6">
                            <div className="text-sm text-neutral-500 mb-2">Recebidos por Material (Kg)</div>
                            <canvas ref={recChartRef} height="140"></canvas>
                            {porMaterialData.length === 0 && !loading && <div className="text-neutral-400 text-sm mt-4 text-center">Sem dados de recebimento no período.</div>}
                        </Card>
                        <Card className="p-6">
                            <div className="text-sm text-neutral-500 mb-2">Receita por Material (R$)</div>
                            <canvas ref={revChartRef} height="140"></canvas>
                            {porMaterialData.length === 0 && !loading && <div className="text-neutral-400 text-sm mt-4 text-center">Sem dados de receita no período.</div>}
                        </Card>
                    </div>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <Card className="p-6">
                            <div className="text-sm text-neutral-500 mb-3">Resumo por Material</div>
                            <Table
                                columns={[
                                    { key: "nome", header: "Material" },
                                    { key: "recebido", header: "Recebido", render: (v, row) => `${v.toFixed(1)} ${row.unidade_medida}` },
                                    { key: "vendido", header: "Vendido", render: (v, row) => `${v.toFixed(1)} ${row.unidade_medida}` },
                                    { key: "saldo", header: "Saldo", render: (v, row) => `${v.toFixed(1)} ${row.unidade_medida}` },
                                    { key: "receita", header: "Receita", render: v => money(v) },
                                ]}
                                data={porMaterialData}
                                emptyLabel="Sem dados no período"
                            />
                        </Card>
                        <Card className="p-6">
                            <div className="text-sm text-neutral-500 mb-3">Recebido por Associação (Kg)</div>
                            <Table
                                columns={[
                                    { key: "nome", header: "Associação" },
                                    { key: "quantidade", header: "Quantidade Total", render: (v) => v.toFixed(1) + ' Kg' },
                                ]}
                                data={porAssociacaoData}
                                emptyLabel="Sem recebimentos no período"
                            />
                        </Card>
                    </div>
                </>
            )}
        </section>
    );
}
// ========== App ==========

function App() {
    const [active, setActive] = useState("dashboard");
    const [store, setStore] = useState({
        materiais: [],
        associacoes: [],
        recebimentos: [],
        vendas: [],
    });
    const [loading, setLoading] = useState(true);

    // --- Funções de Busca Reutilizáveis ---
    const fetchMaterialsWithStock = async () => {
        try {
            const response = await fetch(`${API_URL}/estoque/`);
            if (!response.ok)
                throw new Error(`Fetch Estoque: ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error("Erro fetchMaterialsWithStock:", error);
            throw error;
        }
    };
    const fetchAssociacoes = async () => {
        try {
            const response = await fetch(`${API_URL}/associacoes/`);
            if (!response.ok)
                throw new Error(`Fetch Associações: ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error("Erro fetchAssociacoes:", error);
            throw error;
        }
    };
    const fetchEntradas = async () => {
        try {
            const response = await fetch(`${API_URL}/entradas_material/`);
            if (!response.ok)
                throw new Error(`Fetch Entradas: ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error("Erro fetchEntradas:", error);
            throw error;
        }
    };
    const fetchVendas = async () => {
        try {
            const response = await fetch(`${API_URL}/vendas/`);
            if (!response.ok)
                throw new Error(`Fetch Vendas: ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error("Erro fetchVendas:", error);
            throw error;
        }
    };

    // --- Busca de Dados Iniciais ---
    useEffect(() => {
        const loadInitialData = async () => {
            setLoading(true);
            console.log("Buscando dados iniciais da API...");
            try {
                const [materiaisData, associacoesData, entradasData, vendasData] =
                    await Promise.all([
                        fetchMaterialsWithStock(),
                        fetchAssociacoes(),
                        fetchEntradas(),
                        fetchVendas(),
                    ]);
                setStore({
                    materiais: materiaisData,
                    associacoes: associacoesData,
                    recebimentos: entradasData,
                    vendas: vendasData,
                });
                console.log("Dados carregados com sucesso!");
            } catch (error) {
                console.error("Falha GERAL ao carregar dados da API:", error);
                alert(
                    `Não foi possível carregar os dados iniciais.\nErro: ${error.message}`
                );
                setStore({
                    materiais: [],
                    associacoes: [],
                    recebimentos: [],
                    vendas: [],
                });
            } finally {
                setLoading(false);
            }
        };
        loadInitialData();
    }, []);

    // --- Função Helper para Atualizar Estoque ---
    const refreshMateriaisComEstoque = async () => {
        try {
            const updatedMaterials = await fetchMaterialsWithStock();
            setStore((s) => ({ ...s, materiais: updatedMaterials }));
        } catch (error) {
            console.error("Falha ao re-buscar estoque após ação:", error);
        }
    };

    // --- Funções CREATE ---
    const createMaterial = async (payload) => {
        const payloadParaAPI = {
            nome: payload.nome,
            categoria: payload.categoria,
            unidade_medida: payload.unidade,
        };
        try {
            const response = await fetch(`${API_URL}/materiais/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payloadParaAPI),
            });
            if (!response.ok) {
                const d = await response.json();
                throw new Error(d.detail || "Erro");
            }
            await refreshMateriaisComEstoque();
            return true;
        } catch (error) {
            console.error("Erro criar material:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    const createAssociacao = async (payload) => {
        const payloadParaAPI = { ...payload };
        try {
            const response = await fetch(`${API_URL}/associacoes/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payloadParaAPI),
            });
            if (!response.ok) {
                const d = await response.json();
                throw new Error(d.detail || "Erro");
            }
            const newData = await response.json();
            setStore((s) => ({
                ...s,
                associacoes: [...s.associacoes, newData].sort((a, b) =>
                    a.nome.localeCompare(b.nome)
                ),
            }));
            return true;
        } catch (error) {
            console.error("Erro criar associação:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    const createRecebimento = async (payload) => {
        const payloadParaAPI = {
            quantidade: payload.quantidade,
            id_material: payload.materialId,
            id_associacao: payload.associacaoId,
        };
        try {
            const response = await fetch(`${API_URL}/entradas/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payloadParaAPI),
            });
            if (!response.ok) {
                const errorData = await response.json();
                let errorMsg = "Falha ao registrar recebimento.";
                if (errorData.detail && Array.isArray(errorData.detail)) {
                    errorMsg = errorData.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join('; ');
                } else if (errorData.detail) { errorMsg = errorData.detail; }
                throw new Error(errorMsg);
            }
            const newData = await response.json();
            setStore((s) => ({
                ...s,
                recebimentos: [...s.recebimentos, newData],
            }));
            await refreshMateriaisComEstoque();
            return true;
        } catch (error) {
            console.error("Erro criar recebimento:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    const createVenda = async (payload) => {
        const payloadParaAPI = {
            comprador: payload.comprador,
            concluida: true,
            itens: payload.itens,
        };
        console.log("Enviando para API (Venda):", JSON.stringify(payloadParaAPI, null, 2));
        try {
            const response = await fetch(`${API_URL}/vendas/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payloadParaAPI),
            });
            if (!response.ok) {
                const errorData = await response.json();
                let errorMsg = `Falha ao registrar venda (Status: ${response.status})`;
                if (errorData.detail && Array.isArray(errorData.detail)) {
                    errorMsg += `: ${errorData.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join('; ')}`;
                } else if (errorData.detail) { errorMsg += `: ${errorData.detail}`; }
                throw new Error(errorMsg);
            }
            const newData = await response.json();
            setStore((s) => ({ ...s, vendas: [...s.vendas, newData] }));
            await refreshMateriaisComEstoque();
            return true;
        } catch (error) {
            console.error("Erro criar venda:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    // --- Funções UPDATE ---
    const updateMaterial = async (id, payload) => {
        const payloadParaAPI = {
            nome: payload.nome,
            categoria: payload.categoria,
            unidade_medida: payload.unidade,
        };
        try {
            const response = await fetch(`${API_URL}/materiais/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payloadParaAPI),
            });
            if (!response.ok) {
                const d = await response.json();
                throw new Error(d.detail || "Erro");
            }
            await refreshMateriaisComEstoque();
            return true;
        } catch (error) {
            console.error("Erro atualizar material:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    const updateAssociacao = async (id, payload) => {
        const payloadParaAPI = { ...payload };
        try {
            const response = await fetch(`${API_URL}/associacoes/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payloadParaAPI),
            });
            if (!response.ok) {
                const d = await response.json();
                throw new Error(d.detail || "Erro");
            }
            const updatedData = await response.json();
            setStore((s) => ({
                ...s,
                associacoes: s.associacoes.map((a) =>
                    a.id === id ? updatedData : a
                ),
            }));
            return true;
        } catch (error) {
            console.error("Erro atualizar associação:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    // --- Funções DELETE / CANCEL ---
    const deleteAssociacao = async (id) => {
        if (!confirm("Tem certeza que deseja INATIVAR esta associação?"))
            return false;
        try {
            const response = await fetch(`${API_URL}/associacoes/${id}`, {
                method: "DELETE",
            });
            if (response.status === 204) {
                setStore((s) => ({
                    ...s,
                    associacoes: s.associacoes.filter((a) => a.id !== id),
                }));
                return true;
            } else {
                const d = await response.json();
                throw new Error(d.detail || "Erro");
            }
        } catch (error) {
            console.error("Erro inativar associação:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    const cancelEntrada = async (id) => {
        if (
            !confirm(
                "Tem certeza que deseja CANCELAR este recebimento? O estoque será recalculado."
            )
        )
            return false;
        try {
            const response = await fetch(`${API_URL}/entradas/${id}`, {
                method: "DELETE",
            });
            if (response.status === 204) {
                setStore((s) => ({
                    ...s,
                    recebimentos: s.recebimentos.filter((r) => r.id !== id),
                }));
                await refreshMateriaisComEstoque();
                return true;
            } else {
                const d = await response.json();
                throw new Error(d.detail || "Erro");
            }
        } catch (error) {
            console.error("Erro cancelar recebimento:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    const cancelVenda = async (id) => {
        if (
            !confirm(
                "Tem certeza que deseja CANCELAR esta venda? O estoque será recalculado."
            )
        )
            return false;
        try {
            const response = await fetch(`${API_URL}/vendas/${id}`, {
                method: "DELETE",
            });
            if (response.status === 204) {
                setStore((s) => ({
                    ...s,
                    vendas: s.vendas.filter((v) => v.id !== id),
                }));
                await refreshMateriaisComEstoque();
                return true;
            } else {
                const d = await response.json();
                throw new Error(d.detail || "Erro");
            }
        } catch (error) {
            console.error("Erro cancelar venda:", error);
            alert(`Erro: ${error.message}`);
            return false;
        }
    };

    // --- Renderização ---
    return (
        <div className="min-h-screen">
            <header className="backdrop-blur bg-white/70 border-b border-black/5 sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-3">
                    <div className="w-9 h-9 rounded-2xl bg-emerald-600 grid place-items-center text-white font-bold">RC</div>
                    <div className="flex-1">
                        <div className="font-semibold leading-tight">Rede de Catadores – Gestão</div>
                        <div className="text-xs text-neutral-500">MVP Conectado</div>
                    </div>
                </div>
            </header>

            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-[240px,1fr] gap-6 px-4 py-6">
                <aside className="md:sticky md:top-16 h-max">
                    <nav className="bg-white/80 rounded-2xl border border-black/5 shadow-sm p-3">
                        <div className="text-xs uppercase tracking-wide text-neutral-500 px-2 pb-2">Navegação</div>
                        <div className="flex flex-wrap md:flex-col gap-2">
                            <Pill active={active === "dashboard"} onClick={() => setActive("dashboard")}>Dashboard</Pill>
                            <Pill active={active === "materiais"} onClick={() => setActive("materiais")}>Materiais</Pill>
                            <Pill active={active === "associacoes"} onClick={() => setActive("associacoes")}>Associações</Pill>
                            <Pill active={active === "recebimentos"} onClick={() => setActive("recebimentos")}>Recebimentos</Pill>
                            <Pill active={active === "vendas"} onClick={() => setActive("vendas")}>Vendas</Pill>
                            <Pill active={active === "relatorios"} onClick={() => setActive("relatorios")}>Relatórios</Pill>
                        </div>
                    </nav>
                </aside>

                <main className="space-y-6">
                    {loading && (
                        <div className="text-center p-6 text-xl text-emerald-600">
                            Carregando dados...
                        </div>
                    )}
                    {!loading && active === "dashboard" && (
                        <DashboardView store={store} />
                    )}
                    {!loading && active === "materiais" && (
                        <MateriaisView
                            data={store.materiais}
                            onCreate={createMaterial}
                            onUpdate={updateMaterial}
                        />
                    )}
                    {!loading && active === "associacoes" && (
                        <AssociacoesView
                            data={store.associacoes}
                            onCreate={createAssociacao}
                            onUpdate={updateAssociacao}
                            onDelete={deleteAssociacao}
                        />
                    )}
                    {!loading && active === "recebimentos" && (
                        <RecebimentosView
                            store={store}
                            setActive={setActive}
                            onCreate={createRecebimento}
                            onCancel={cancelEntrada}
                        />
                    )}
                    {!loading && active === "vendas" && (
                        <VendasView
                            store={store}
                            setActive={setActive}
                            onCreate={createVenda}
                            onCancel={cancelVenda}
                        />
                    )}
                    {!loading && active === "relatorios" && (
                        <RelatoriosView store={store} />
                    )}
                </main>
            </div>
            <footer className="py-8 text-center text-xs text-neutral-500">
                Sistema de Gestão - MVP v0.2
            </footer>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);