export const state = () => ({
    firstPoint: [],
    Point:[],
    companyName:''
})

export const mutations = {
    SetfirstPoint(state, data) {
        state.firstPoint = data
    },

    SetPoint(state, data) {
        state.Point = data
    },
    SetCompany(state,data){
        console.log(11,data);
        state.companyName = data
    }
}

export const getters = {
    firstPoint: s => s.firstPoint,
    Point: s => s.Point,
    companyName: s => s.companyName
}
