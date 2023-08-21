export const state = () => {
  return {
    cities: [],
    activeCity: {},
    // activeCity: {
    //   // TODO: get default city from DB
    //   name: 'Москва',
    //   subdomain: { name: 'moscow' },
    // },
  }
}

export const mutations = {
  setcities(state, cities) {
    state.cities = cities
  },
  setactiveCity(state, name) {
    state.activeCity = name
    // console.log(name)
    // console.log(state.activeCity)
  },
}

export const actions = {
  async fetch({ commit, state }) {
    const cities = await this.$axios.$get(`api/v1/cities/`)

    // Sort Cities Top
    let cities_sorted = cities
    const cities_top = ['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск']
    cities_top.reverse().forEach(city => {
      cities_sorted.unshift(cities_sorted.splice(cities_sorted.findIndex(item => {
        if (item.name === city) {
          item.city_top = true
        }
        return item.name === city
      }), 1)[0])
    })

    commit('setcities', cities_sorted)
  }
}

export const getters = {
  cities: s => s.cities,
  activeCity: s => s.activeCity,
}
