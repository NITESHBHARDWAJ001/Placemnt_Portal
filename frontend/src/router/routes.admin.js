const meta = { roles: ["ADMIN"] }

export default [
  {
    path: "/admin",
    component: () => import("@/layouts/DashboardLayout.vue"),
    meta,
    children: [
      { path: "", redirect: "/admin/dashboard" },
      { path: "dashboard", name: "admin-dashboard", component: () => import("@/views/admin/AdminDashboard.vue"), meta },
      { path: "companies", name: "admin-companies", component: () => import("@/views/admin/CompanyApprovals.vue"), meta },
      { path: "drives", name: "admin-drives", component: () => import("@/views/admin/DriveApprovals.vue"), meta },
      { path: "students", name: "admin-students", component: () => import("@/views/admin/StudentManagement.vue"), meta },
      { path: "activity-logs", name: "admin-activity-logs", component: () => import("@/views/admin/ActivityLogs.vue"), meta },
    ],
  },
]
