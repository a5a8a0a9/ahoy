import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

import VueClipboard from "vue-clipboard2";

import GlobalInject from "@/globalInject";
import GlobalComponents from "@/globalComponents";
import "@/globalStyle";

Vue.use(VueClipboard);
Vue.use(GlobalInject);
Vue.use(GlobalComponents);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");

Vue.use(global);
