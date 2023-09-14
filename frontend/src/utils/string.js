
export function strip(str) {
  return str.replace(/<\/?[^>]+(>|$)/g, '');
}

export function repoOwnerFormat(str) {
  if (!str) {
    return 'Forneça o link de um reposítório.';
  }
  let calls = 0;
  calls = str.split('/');
  let callsSize = calls.length;
  if (calls.pop() === '') {
    callsSize -= 1;
  }
  if (callsSize === 5) {
    return true;
  }
  return 'Repositório inválido. Forneça no formato "https://github.com/dono_do_repositorio/repositorio/"';
}
