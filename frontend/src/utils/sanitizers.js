export function stripHtml(html) {
  if (!html) return '';
  const temp = document.createElement('div');
  temp.textContent = html;
  return temp.innerHTML;
}

export function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

export function sanitizeString(input) {
  if (!input) return '';
  return String(input)
    .replace(/[<>]/g, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+=/gi, '')
    .trim();
}

export function sanitizeObject(obj) {
  if (!obj || typeof obj !== 'object') return obj;
  
  const sanitized = {};
  for (const key in obj) {
    if (typeof obj[key] === 'string') {
      sanitized[key] = sanitizeString(obj[key]);
    } else {
      sanitized[key] = obj[key];
    }
  }
  return sanitized;
}

export function normalizeString(text) {
  if (!text) return '';
  return String(text)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toUpperCase()
    .replace(/\s+/g, ' ')
    .trim();
}

export function sanitizeCNPJ(cnpj) {
  if (!cnpj) return null;
  const limpo = String(cnpj).replace(/\D/g, '');
  if (limpo.length !== 14) return null;
  return limpo;
}

export function sanitizeCPF(cpf) {
  if (!cpf) return null;
  const limpo = String(cpf).replace(/\D/g, '');
  if (limpo.length !== 11) return null;
  return limpo;
}

export function sanitizePhone(phone) {
  if (!phone) return null;
  const limpo = String(phone).replace(/\D/g, '');
  if (limpo.length !== 10 && limpo.length !== 11) return null;
  return limpo;
}