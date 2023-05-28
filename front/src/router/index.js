import { createRouter, createWebHashHistory } from "vue-router";
import Hello from '../views/HelloWorld.vue';


const routes = [
    {
        path: '/',
        name: 'start',
        component: Hello,
        
    },
   
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
