import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import PageTwo from '../views/PageTwo.vue'
import PageThree from '../views/PageThree.vue'
import NotFound from '../views/NotFound.vue'

const router = createRouter({
  // createWebHistory enables clean URLs (e.g., /page-2) without hashes (#)
  history: createWebHistory(import.meta.env.BASE_URL), 
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/page-2',
      name: 'page-two',
      component: PageTwo
    },
    {
      path: '/page-3',
      name: 'page-three',
      component: PageThree
    },
    {
      // This is a Regex that matches any string
      path: '/:pathMatch(.*)*', 
      name: 'not-found',
      component: NotFound
    }
  ]
})

export default router