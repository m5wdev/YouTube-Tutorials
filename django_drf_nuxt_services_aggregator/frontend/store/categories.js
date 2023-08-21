export const state = () => {
  return {
    categories: [],
  }
}

export const mutations = {
  setcategories(state, categories) {
    state.categories = categories
  },
}

export const actions = {
  async fetch({ commit, state }) {
    const categories = await this.$axios.$get(`api/v1/categories/`)
    commit('setcategories', categories)
  }
}

export const getters = {
  categories: s => s.categories,
}
