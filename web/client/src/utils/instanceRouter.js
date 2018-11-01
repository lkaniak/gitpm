import VueRouter from 'vue-router';

export default function setRouter(routes) {
  const router = new VueRouter({
    routes,
  });
  return router;
}
