import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import App from './App.vue';
import router from './router';

// import * as ElementPlusIconsVue from '@element-plus/icons-vue';
// import store from './store';
import axios from 'axios';


const app = createApp(App);



axios.defaults.baseURL = 'http://localhost:8443/api';

app.provide('axios', axios);
// app.use(router);
// app.use(store);
app.use(ElementPlus);



app.use(router);

app.mount('#app');
