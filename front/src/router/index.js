import { createRouter, createWebHashHistory } from "vue-router";
import Hello from '../views/HelloWorld.vue';


const routes = [
    {
        path: '/',
        redirect: { name: 'start' },
    },
    {
        path: '/start',
        name: 'start',
        component: Hello,
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
