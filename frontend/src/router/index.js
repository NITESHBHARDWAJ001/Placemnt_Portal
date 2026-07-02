import { createRouter, createWebHistory } from "vue-router"
import { authGuard } from "./guards"
import adminRoutes from "./routes.admin"
import companyRoutes from "./routes.company"
import studentRoutes from "./routes.student"

const routes = [
  { path: "/", redirect: "/login" },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/auth/LoginView.vue"),
    meta: { public: true, guestOnly: true },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/auth/RegisterView.vue"),
    meta: { public: true, guestOnly: true },
  },
  ...adminRoutes,
  ...companyRoutes,
  ...studentRoutes,
  {
    path: "/403",
    name: "forbidden",
    component: () => import("@/views/Forbidden.vue"),
    meta: { public: true },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/views/NotFound.vue"),
    meta: { public: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach(authGuard)

export default router
