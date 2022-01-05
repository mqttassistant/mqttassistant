import BootstrapVue3 from 'bootstrap-vue-3'



import { createApp } from 'vue'
import App from './App.vue'
import { createWebHashHistory, createRouter } from "vue-router";
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

/******************* ROUNTING ***********************/
import Nodes from './components/Nodes.vue'
import Login from './components/Login.vue'
const routes = [
    { path: '/', component: Nodes },
    { path: '/login', component: Login },
]
const router = createRouter({
    history: createWebHashHistory(),
    routes, 
})
/******************* ROUNTING ***********************/


const app = createApp(App);
app.use(BootstrapVue3);
app.use(router);
app.mount('#app');

