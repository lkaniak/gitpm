import Vue from 'vue';
import Router from 'vue-router';
import AppMain from '@/modules/main/AppMain.vue';
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: AppMain,
      children: [
      ],
    },

  ],
});
