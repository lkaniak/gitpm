import { http } from '@/utils/http.js';

export function generateLog(data) {
  return http.post('/api/eventlog/generate_log/', data)
    .then(response => response.data);
}

export function downloadLog(data) {
  return http.post('/api/eventlog/download/', data)
    .then(response => response);
}
