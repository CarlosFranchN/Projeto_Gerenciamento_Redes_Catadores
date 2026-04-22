const toastContainer = document.getElementById('toastContainer');

export function showToast(message, type = 'info', duration = 3000) {
  if (!toastContainer) {
    console.warn('Toast container não encontrado');
    return;
  }

  const toast = document.createElement('div');
  
  const colors = {
    success: 'bg-green-600',
    error: 'bg-red-600',
    warning: 'bg-yellow-600',
    info: 'bg-blue-600'
  };

  const icons = {
    success: '✓',
    error: '✖',
    warning: '⚠',
    info: 'ℹ'
  };

  toast.className = `${colors[type] || colors.info} text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-2 transform transition-all duration-300 translate-x-full opacity-0`;
  toast.innerHTML = `<span class="font-bold">${icons[type] || icons.info}</span><span>${message}</span>`;
  
  toastContainer.appendChild(toast);

  // Animação de entrada
  requestAnimationFrame(() => {
    toast.classList.remove('translate-x-full', 'opacity-0');
  });

  // Remove após o tempo
  setTimeout(() => {
    toast.classList.add('translate-x-full', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

export function showSuccess(message) {
  showToast(message, 'success');
}

export function showError(message) {
  showToast(message, 'error', 5000);
}

export function showWarning(message) {
  showToast(message, 'warning');
}

export function showInfo(message) {
  showToast(message, 'info');
}