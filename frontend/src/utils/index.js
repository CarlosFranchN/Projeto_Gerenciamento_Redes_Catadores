// frontend/src/utils/index.js

// Formatters
export {
  formatCurrency,
  formatNumber,
  formatDate,
  formatDateTime,
  formatCNPJ,
  formatCPF,
  formatPhone,
  formatWeight,
  truncateText,
  toTitleCase
} from './formatters.js';

// Validators
export {
  isValidEmail,
  isValidCNPJ,
  isValidCPF,
  isValidPhone,
  validateRequired,
  validateMinLength,
  validateMaxLength,
  validateNumber,
  validateLogin,
  validateContactForm
} from './validators.js';

// Sanitizers
export {
  stripHtml,
  escapeHtml,
  sanitizeString,
  sanitizeObject,
  normalizeString,
  sanitizeCNPJ,
  sanitizeCPF,
  sanitizePhone
} from './sanitizers.js';

export {
  createSkeletonCard,
  createSkeletonTable,
  createSkeletonChart,
  createSkeletonGrid,
  showLoading,
  hideLoading,
  setContent,
  appendContent,
  clearContent
} from './loading.js';

export {
  showToast,
  showSuccess,
  showError,
  showWarning,
  showInfo
} from './toast.js';