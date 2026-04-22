export default function Dashboard({ onLogout }) {
  return (
    <div>
      <h1>Bem-vindo ao Painel, Gestor!</h1>
      <button onClick={onLogout}>Sair</button>
    </div>
  );
}