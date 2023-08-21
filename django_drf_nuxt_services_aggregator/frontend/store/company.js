export const state = () => ({
    current_company: {},
})

export const mutations = {
    SetCurrentCompany(state, data) {
        state.current_company = data
    },
}

export const getters = {
    get_current_company: s => s.current_company,
}
