const meta = { roles: ["STUDENT"] }

export default [
  {
    path: "/student",
    component: () => import("@/layouts/DashboardLayout.vue"),
    meta,
    children: [
      { path: "", redirect: "/student/dashboard" },
      { path: "dashboard", name: "student-dashboard", component: () => import("@/views/student/StudentDashboard.vue"), meta },
      { path: "profile", name: "student-profile", component: () => import("@/views/student/StudentProfile.vue"), meta },
      { path: "drives", name: "student-drives", component: () => import("@/views/student/BrowseDrives.vue"), meta },
      { path: "applications", name: "student-applications", component: () => import("@/views/student/MyApplications.vue"), meta },
      { path: "placement-history", name: "student-placement-history", component: () => import("@/views/student/PlacementHistory.vue"), meta },
    ],
  },
]
