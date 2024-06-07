import Vue from "vue";
import VueRouter from "vue-router";
// import HomeView from '../views/HomeView.vue'
import NamePlateView from "../views/nameplate.vue";
import UploadImageView from "../views/UploadImage.vue";
Vue.use(VueRouter);

const routes = [
  // {
  //   path: '/',
  //   name: 'home',
  //   component: HomeView
  // },
  {
    path: "/nameplate",
    name: "nameplate",
    component: NamePlateView,
  },
  {
    path: "/upload",
    name: "upload",
    component: UploadImageView,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
