import axios from 'axios';

// allow use http client without Vue instance

const url = process.env.VUE_APP_API_URL ? process.env.VUE_APP_API_URL : `${location.protocol}//localhost:8080`;

export const http = axios.create({
  baseURL: url,
});

/**
* Helper method to set the header with the token
*/
export function setToken(token) {
  http.defaults.headers.common['X-Credentials'] = token;
}

// receive store and data by options
export function install(Vue) {
  Object.defineProperty(Vue.prototype, '$http', {
    get() {
      return http;
    },
  });
}
