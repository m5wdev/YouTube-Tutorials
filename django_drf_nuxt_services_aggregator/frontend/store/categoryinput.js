export const state = () => ({
    categorysinputs_list: [],
    item_list: [],
})

export const mutations = {
    Setcategorysinputs(state, data) {
        state.categorysinputs_list.push(data)

    },

    Setitem_list(state, item) {
        state.item_list.push(item)
    },

    SetRemove(state) {
        state.item_list = []
        state.categorysinputs_list = [];
    }
}

export const getters = {
    categorysinputs_list: s => [...s.categorysinputs_list],
    item_list: s => s.item_list,
}
