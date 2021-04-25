const state = () => ({
  revisionList: [],
});

const getters = {
  activeTabList: (state) => {
    return state.revisionList;
  },
};

const mutations = {
  setRevisionMutation(state, revision) {
    if (revision.visible) {
      state.revisionList.push(revision);
    } else {
      let idx = state.revisionList.findIndex((x) => x.id === revision.id);
      state.revisionList.splice(idx, 1);
    }
  },
};

const actions = {
  setRevision({ commit }, revision) {
    commit("setRevisionMutation", revision);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
