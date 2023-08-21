export const state = () => {
  return {
    brands: [],
  }
}

export const mutations = {
  setbrands(state, brands) {
    state.brands = brands
  },
}

export const actions = {
  async fetch({ commit, state }) {
    // store.getters["cities/activeCity"].subdomain.name
    // const subdomain = store.getters["cities/activeCity"].subdomain.name;
    const brands = await this.$axios.$get(`api/v1/brands/?popular=10&subdomain=moscow`)
    commit('setbrands', brands)
  },
}

export const getters = {
  brands: s => s.brands,
}
