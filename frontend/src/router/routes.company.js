const meta = { roles: ["COMPANY"] }

export default [
  {
    path: "/company",
    component: () => import("@/layouts/DashboardLayout.vue"),
    meta,
    children: [
      { path: "", redirect: "/company/dashboard" },
      { path: "dashboard", name: "company-dashboard", component: () => import("@/views/company/CompanyDashboard.vue"), meta },
      { path: "profile", name: "company-profile", component: () => import("@/views/company/CompanyProfile.vue"), meta },
      { path: "drives", name: "company-drives", component: () => import("@/views/company/MyDrives.vue"), meta },
      { path: "drives/:driveId/applicants", name: "company-drive-applicants", component: () => import("@/views/company/DriveApplicants.vue"), meta },
      { path: "interviews", name: "company-interviews", component: () => import("@/views/company/InterviewSchedule.vue"), meta },
    ],
  },
]
