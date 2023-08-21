import Vue from 'vue'
import YmapPlugin from 'vue-yandex-maps'

const settings = {
    apiKey: '1e4f5a3b-edc5-4fb6-a346-9ec48a913d7b',
    lang: 'ru_RU',
    coordorder: 'latlong',
    enterprise: false,
    version: '2.1'
} // настройки плагина

Vue.use(YmapPlugin, settings);
