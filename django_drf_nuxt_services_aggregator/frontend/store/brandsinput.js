export const state = () => ({
    brandsinputs_list: [],
    item_list: [],
})

export const mutations = {
    Setbrandsinputs(state, data) {
        state.brandsinputs_list.push(data)

    },

    Setitem_list(state, item) {
        state.item_list.push(item)
    },

    SetRemove(state) {
        state.item_list = []
        state.brandsinputs_list = [];
    }
}

export const getters = {
    brandsinputs_list: s => [...s.brandsinputs_list],
    item_list: s => s.item_list,
}
