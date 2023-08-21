export const state = () => ({
    points_list: [],
    item_list: [],
})

export const mutations = {
    SetPoints(state, data) {
        state.points_list.push(data)

    },

    SetPointsAnalog(state, data) {
        state.points_list = data

    },

    Setitem_list(state, item) {
        state.item_list.push(item)
    },

    SetRemove(state) {
        state.item_list = []
        state.points_list = [];
    }
}

export const getters = {
    points_list: s => [...s.points_list],
    item_list: s => s.item_list,
}
