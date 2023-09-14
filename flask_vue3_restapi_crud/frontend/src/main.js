import 'bootstrap/dist/css/bootstrap.css'
import './assets/main.css'

import * as bootstrap from 'bootstrap'


import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:5000'

const app = createApp(App)

app.use(router)

app.mount('#app')
