import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import axios from 'axios'
import VueAxios from "vue-axios"
import VueTouchKeyboard from "vue-touch-keyboard";
import style from "vue-touch-keyboard/dist/vue-touch-keyboard.css"; // load default style

 
Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(VueTouchKeyboard);
axios.defaults.baseURL = process.env.API_ENDPOINT;

new Vue({
  render: h => h(App),
}).$mount('#app')
