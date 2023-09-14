import '@babel/polyfill';
import Vue from 'vue';
import './plugins/vuetify';
import App from './App.vue';
import { install as http } from '@/utils/http.js';
import router from './plugins/router';

import './assets/css/main/main.styl';
import 'vue2vis/dist/vue2vis.css';

Vue.use(http);

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
