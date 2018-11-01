import { http } from '@/utils/http.js';

export function generateProcess(data) {
  return http.post('/api/process/generate_process/', data)
    .then(response => response.data);
}

export function downloadProcess(data) {
  return http.post('/api/process/download/', data)
    .then(response => response);
}
