export function isValidEmail(email) {
  if (!email) return false;
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export function isValidCNPJ(cnpj) {
  if (!cnpj) return false;
  const limpo = String(cnpj).replace(/\D/g, '');
  return limpo.length === 14;
}

export function isValidCPF(cpf) {
  if (!cpf) return false;
  const limpo = String(cpf).replace(/\D/g, '');
  return limpo.length === 11;
}

export function isValidPhone(phone) {
  if (!phone) return false;
  const limpo = String(phone).replace(/\D/g, '');
  return limpo.length === 10 || limpo.length === 11;
}

export function validateRequired(value, fieldName = 'Campo') {
  if (!value || String(value).trim() === '') {
    return { valid: false, message: `${fieldName} é obrigatório` };
  }
  return { valid: true, message: '' };
}

export function validateMinLength(value, minLength, fieldName = 'Campo') {
  if (!value) return { valid: false, message: `${fieldName} é obrigatório` };
  if (String(value).length < minLength) {
    return { valid: false, message: `${fieldName} deve ter pelo menos ${minLength} caracteres` };
  }
  return { valid: true, message: '' };
}

export function validateMaxLength(value, maxLength, fieldName = 'Campo') {
  if (!value) return { valid: true, message: '' };
  if (String(value).length > maxLength) {
    return { valid: false, message: `${fieldName} deve ter no máximo ${maxLength} caracteres` };
  }
  return { valid: true, message: '' };
}

export function validateNumber(value, fieldName = 'Campo') {
  if (value === null || value === undefined || value === '') {
    return { valid: true, message: '' };
  }
  if (isNaN(Number(value))) {
    return { valid: false, message: `${fieldName} deve ser um número válido` };
  }
  return { valid: true, message: '' };
}

export const validateLogin = (username, password) => {
  const errors = {};
  
  if (!username || username.trim() === '') {
    errors.username = 'Usuário é obrigatório';
  }
  if (!password || password.length < 6) {
    errors.password = 'Senha deve ter pelo menos 6 caracteres';
  }
  
  return {
    valid: Object.keys(errors).length === 0,
    errors
  };
};


export function validateContactForm(data) {
  const errors = {};
  let isValid = true;
  
  const nameValidation = validateRequired(data.name, 'Nome');
  if (!nameValidation.valid) {
    errors.name = nameValidation.message;
    isValid = false;
  }
  
  const emailValidation = validateRequired(data.email, 'E-mail');
  if (!emailValidation.valid) {
    errors.email = emailValidation.message;
    isValid = false;
  } else if (!isValidEmail(data.email)) {
    errors.email = 'E-mail inválido';
    isValid = false;
  }
  
  const messageValidation = validateRequired(data.message, 'Mensagem');
  if (!messageValidation.valid) {
    errors.message = messageValidation.message;
    isValid = false;
  }
  
  return { valid: isValid, errors };
}