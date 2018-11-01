import { http } from '@/utils/http.js';

export function getRepository(data) {
  return http.post('/api/repositories/external/get_commits/', data)
    .then(response => response.data);
}

export function downloadRepository(data) {
  return http.post('/api/repositories/external/download/', data)
    .then(response => response.data);
}
