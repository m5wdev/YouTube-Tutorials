import Vue from 'vue';

Vue.component('search-component', require('./components/SearchComponent').default);

new Vue({
    el: '#app',
});
