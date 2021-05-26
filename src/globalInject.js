import UtilityMixin from "@/lib/utility";

const GlobalInject = {
  install(Vue) {
    Vue.use(UtilityMixin);
  },
};

export default GlobalInject;
