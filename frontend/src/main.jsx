import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
// 1. Importar o React Query
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// 2. Criar a instância do cliente
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false, // Não recarrega os dados só de mudar de aba do navegador
      staleTime: 1000 * 60 * 5, // Mantém os dados em cache "frescos" por 5 minutos
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* 3. Envolver o App com o Provider */}
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);