<template>
  <div class="placeholder">
  <div class="placeholder__icon" aria-hidden="true">
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M5 6.5A2.5 2.5 0 017.5 4h9A2.5 2.5 0 0119 6.5v7A2.5 2.5 0 0116.5 16H10l-4.2 3.15A.8.8 0 015 18.5v-12z"
        stroke="currentColor"
        stroke-width="1.6"
        stroke-linejoin="round"
      />
    </svg>
  </div>
  <p class="placeholder__title">AI 问答</p>
  <p class="placeholder__desc">功能开发中，敬请期待</p>
  </div>
</template>

<style scoped>
.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 40vh;
  padding: 2rem 1.5rem;
  text-align: center;
}

.placeholder__icon {
  width: 3.5rem;
  height: 3.5rem;
  margin-bottom: 1rem;
  color: var(--color-text-secondary);
  opacity: 0.45;
}

.placeholder__icon svg {
  width: 100%;
  height: 100%;
}

.placeholder__title {
  margin: 0 0 0.5rem;
  font-size: 1.0625rem;
  font-weight: 600;
  color: var(--color-text);
}

.placeholder__desc {
  margin: 0;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}
</style>
