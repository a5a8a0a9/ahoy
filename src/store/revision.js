const state = () => ({
  revisionList: [],
});

const getters = {};

const mutations = {
  setRevision(state, revisions) {
    state.revisionList = revisions;
  },
};

const actions = {
  setRevision({ commit }, revisions) {
    commit("setRevision", revisions);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
