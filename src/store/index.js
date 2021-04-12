import Vue from "vue";
import Vuex from "vuex";
import revision from "./revision";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    revision,
  },
});
