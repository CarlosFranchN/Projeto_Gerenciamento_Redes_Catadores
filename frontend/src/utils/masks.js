// src/utils/masks.js

export const formatarCNPJ = (value) => {
  if (!value) return '';
  let formatado = value.replace(/\D/g, '');
  if (formatado.length > 14) formatado = formatado.slice(0, 14);
  
  return formatado
    .replace(/^(\d{2})(\d)/, '$1.$2')
    .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
    .replace(/\.(\d{3})(\d)/, '.$1/$2')
    .replace(/(\d{4})(\d)/, '$1-$2');
};

export const formatarTelefone = (value) => {
  if (!value) return '';
  let formatado = value.replace(/\D/g, '');
  if (formatado.length > 11) formatado = formatado.slice(0, 11);
  
  return formatado
    .replace(/^(\d{2})(\d)/, '($1) $2')
    .replace(/(\d{5})(\d)/, '$1-$2');
};

export const formatarCEP = (value) => {
  if (!value) return '';
  let formatado = value.replace(/\D/g, '');
  if (formatado.length > 8) formatado = formatado.slice(0, 8);
  
  return formatado.replace(/^(\d{5})(\d)/, '$1-$2');
};