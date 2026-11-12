<script setup>
defineProps({
  item: {
    type: Object,
    required: true,
  },
})

defineEmits(['select'])
</script>

<template>
  <article class="news-item" @click="$emit('select', item.id)">
    <div class="news-item__body">
      <h2 class="news-item__title">{{ item.title }}</h2>
      <p v-if="item.description || item.summary" class="news-item__summary">
        {{ item.description || item.summary }}
      </p>
      <div class="news-item__meta">
        <span class="news-item__source">{{ item.source || '头条资讯' }}</span>
        <span class="news-item__dot">·</span>
        <span class="news-item__views">{{ item.view_count }} 阅读</span>
      </div>
    </div>
    <img
      v-if="item.cover_url"
      class="news-item__thumb"
      :src="item.cover_url"
      :alt="item.title"
      loading="lazy"
    />
  </article>
</template>

<style scoped>
.news-item {
  display: flex;
  gap: 12px;
  padding: 14px 0;
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
}

.news-item__body {
  flex: 1;
  min-width: 0;
}

.news-item__title {
  margin: 0 0 8px;
  font-size: 1.0625rem;
  font-weight: 600;
  line-height: 1.35;
  color: var(--color-text);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-item__summary {
  margin: 0 0 8px;
  font-size: 0.8125rem;
  line-height: 1.45;
  color: var(--color-text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-item__meta {
  font-size: 0.75rem;
  color: var(--color-text-muted, #999);
}

.news-item__dot {
  margin: 0 4px;
}

.news-item__thumb {
  flex-shrink: 0;
  width: 112px;
  height: 72px;
  object-fit: cover;
  border-radius: 6px;
  background: var(--color-border);
}
</style>
