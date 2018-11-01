import Vue from 'vue';
import Router from 'vue-router';
import AppMain from '@/modules/main/AppMain.vue';
import Graph from '@/modules/graph/Graph.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: AppMain,
      children: [
        {
          path: '/niceGraphics',
          name: 'niceGraphics',
          component: Graph,
        },
      ],
    },

  ],
});
