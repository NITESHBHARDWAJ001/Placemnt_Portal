<template>
  <div class="pp-auth-shell d-flex align-items-center justify-content-center min-vh-100">
    <div class="pp-auth-panel row g-0 shadow-lg overflow-hidden">
      <div class="col-lg-6 d-none d-lg-flex pp-auth-hero flex-column justify-content-center p-5">
        <i class="bi bi-mortarboard-fill display-3 mb-4"></i>
        <h2 class="fw-bold mb-3">Placement Portal</h2>
        <p class="opacity-75">
          Connecting students, companies, and campus placement teams on one modern platform.
        </p>
      </div>
      <div class="col-lg-6 bg-white p-4 p-lg-5">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.pp-auth-shell {
  background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 60%);
}
.pp-auth-panel {
  width: 100%;
  max-width: 920px;
  border-radius: var(--pp-radius-lg);
  background: #fff;
}
.pp-auth-hero {
  background: linear-gradient(160deg, var(--pp-primary) 0%, var(--pp-secondary) 100%);
  color: #fff;
}
</style>
