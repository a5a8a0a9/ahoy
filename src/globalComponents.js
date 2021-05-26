import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faLockOpen, faLock } from "@fortawesome/free-solid-svg-icons";

library.add(faLockOpen);
library.add(faLock);
const globalComponents = {
  install(Vue) {
    Vue.component("font-awesome-icon", FontAwesomeIcon);
  },
};

export default globalComponents;
