<script setup>
import defaultAvatar from '../assets/hero.png'

defineProps({
  title: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="auth-page">
    <div class="auth-page__brand">
      <img class="auth-page__logo" :src="defaultAvatar" alt="" />
      <p class="auth-page__app-name">新闻资讯</p>
    </div>
    <h1 class="auth-page__title">{{ title }}</h1>
    <div class="auth-page__card">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout',
}
</script>

<style scoped>
.auth-page {
  min-height: 100%;
  padding: 0.5rem 0 2rem;
}

.auth-page__brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.25rem;
}

.auth-page__logo {
  width: 4.5rem;
  height: 4.5rem;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}

.auth-page__app-name {
  margin: 0.75rem 0 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text);
}

.auth-page__title {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
}

.auth-page__card {
  display: block;
  padding: 1.25rem 1rem 1.5rem;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
</style>
