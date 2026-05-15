import React from 'react';
import ReactDOM from 'react-dom/client';
import * as Sentry from "@sentry/react";
import App from './App.jsx';
import './index.css';
// 1. Importar o React Query
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

if (import.meta.env.VITE_SENTRY_DSN) {
  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN,
    integrations: [
      Sentry.browserTracingIntegration(),
      Sentry.replayIntegration({
        maskAllText: false, // Pode mudar para true se quiser ocultar textos digitados pelo usuário na gravação
        blockAllMedia: false,
      }),
    ],
    // Captura 100% das transações para medir lentidão (ideal para dev)
    tracesSampleRate: 1.0, 
    // Grava a tela do usuário apenas quando um erro acontece
    replaysOnErrorSampleRate: 1.0, 
    replaysSessionSampleRate: 0.1, 
  });
}

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