<script setup>
defineProps({
  title: {
    type: String,
    default: '新闻资讯',
  },
})
</script>

<template>
  <header class="news-header">
    <h1 class="news-header__title">{{ title }}</h1>
  </header>
</template>

<style scoped>
.news-header {
  flex-shrink: 0;
  padding: 0.875rem 1rem 0.75rem;
  background: var(--color-bg);
}

.news-header__title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.3;
  text-align: center;
  color: var(--color-text);
  letter-spacing: 0.02em;
}
</style>
