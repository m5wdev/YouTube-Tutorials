export const state = () => ({
  group_name_url: '',
  value_url: ''
})

export const mutations = {
  SetGroup_name_url(state, name) {
    state.group_name_url = name
  },
  Setvalue_url(state, val) {
    state.value_url = val
  }

}

export const getters = {
  group_name_url: s => s.group_name_url,
  value_url: s => s.value_url
}
