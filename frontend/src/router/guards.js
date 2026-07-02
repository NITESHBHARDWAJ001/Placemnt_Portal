import { useAuthStore } from "@/stores/auth.store"

export function authGuard(to) {
  const auth = useAuthStore()

  if (to.meta.public) {
    if (to.meta.guestOnly && auth.isAuthenticated) {
      return auth.homeRouteForRole()
    }
    return true
  }

  if (!auth.isAuthenticated) {
    return { path: "/login", query: { redirect: to.fullPath } }
  }

  if (to.meta.roles && !to.meta.roles.includes(auth.role)) {
    return "/403"
  }

  return true
}
