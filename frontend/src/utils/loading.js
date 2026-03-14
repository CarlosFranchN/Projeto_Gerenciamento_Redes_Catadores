export function createSkeletonCard() {
  const div = document.createElement('div');
  div.className = 'rounded-xl border bg-white p-4 animate-pulse';
  div.innerHTML = `
    <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
    <div class="h-3 bg-gray-200 rounded w-1/2"></div>
  `;
  return div;
}

export function createSkeletonTable(rows = 6) {
  const div = document.createElement('div');
  div.className = 'overflow-hidden rounded-xl border animate-pulse';
  
  let rowsHtml = '';
  for (let i = 0; i < rows; i++) {
    rowsHtml += `
      <tr class="odd:bg-white even:bg-neutral-50">
        <td class="px-4 py-2"><div class="h-4 bg-gray-200 rounded w-20"></div></td>
        <td class="px-4 py-2"><div class="h-4 bg-gray-200 rounded w-16"></div></td>
      </tr>
    `;
  }
  
  div.innerHTML = `
    <table class="min-w-full text-sm">
      <thead class="bg-neutral-50">
        <tr>
          <th class="px-4 py-2"><div class="h-4 bg-gray-200 rounded w-20"></div></th>
          <th class="px-4 py-2"><div class="h-4 bg-gray-200 rounded w-16"></div></th>
        </tr>
      </thead>
      <tbody>${rowsHtml}</tbody>
    </table>
  `;
  return div;
}

export function createSkeletonChart() {
  const div = document.createElement('div');
  div.className = 'h-40 bg-gray-200 rounded-xl animate-pulse mt-6';
  return div;
}

export function createSkeletonGrid(count = 6) {
  const div = document.createElement('div');
  div.className = 'grid sm:grid-cols-2 gap-4';
  
  for (let i = 0; i < count; i++) {
    const card = createSkeletonCard();
    div.appendChild(card);
  }
  
  return div;
}

export function showLoading(element, type = 'card') {
  if (!element) return;
  
  element.dataset.originalContent = element.innerHTML;
  
  switch (type) {
    case 'card':
      element.innerHTML = '';
      element.appendChild(createSkeletonCard());
      break;
    case 'table':
      element.innerHTML = '';
      element.appendChild(createSkeletonTable());
      break;
    case 'chart':
      element.innerHTML = '';
      element.appendChild(createSkeletonChart());
      break;
    case 'grid':
      element.innerHTML = '';
      element.appendChild(createSkeletonGrid());
      break;
    default:
      element.innerHTML = '<div class="animate-pulse text-gray-400">Carregando...</div>';
  }
}

export function hideLoading(element) {
  if (!element || !element.dataset.originalContent) return;
  element.innerHTML = element.dataset.originalContent;
  delete element.dataset.originalContent;
}

export function setContent(element, content) {
  if (!element) return;
  element.innerHTML = content;
}

export function appendContent(element, content) {
  if (!element) return;
  element.insertAdjacentHTML('beforeend', content);
}

export function clearContent(element) {
  if (!element) return;
  element.innerHTML = '';
}