<script setup>
import { computed } from 'vue'

const props = defineProps({
  article: {
    type: Object,
    default: null,
  },
  loading: Boolean,
})

defineEmits(['close', 'open-related'])

const readCount = computed(
  () => props.article?.views ?? props.article?.view_count ?? 0,
)

const relatedList = computed(() => {
  const list = props.article?.relatedNews
  return Array.isArray(list) ? list : []
})

const timeText = computed(() => {
  if (!props.article?.created_at) return ''
  const d = new Date(props.article.created_at)
  if (Number.isNaN(d.getTime())) return props.article.created_at
  return d.toLocaleString('zh-CN', { hour12: false })
})
</script>

<template>
  <div class="detail" aria-modal="true" role="dialog">
    <header class="detail__header">
      <button type="button" class="detail__back" @click="$emit('close')">‹ 返回</button>
    </header>
    <div class="detail__scroll">
      <p v-if="loading" class="detail__loading">加载中...</p>
      <template v-else-if="article">
        <h1 class="detail__title">{{ article.title }}</h1>
        <div class="detail__meta">
          <span>{{ article.source || '头条资讯' }}</span>
          <span>{{ timeText }}</span>
          <span>{{ readCount }} 阅读</span>
        </div>
        <img
          v-if="article.cover_url"
          class="detail__hero"
          :src="article.cover_url"
          :alt="article.title"
        />
        <div class="detail__content">{{ article.content }}</div>
        <section v-if="relatedList.length" class="detail__related">
          <h2 class="detail__related-title">相关推荐</h2>
          <ul class="detail__related-list">
            <li
              v-for="item in relatedList"
              :key="item.id"
              class="detail__related-item"
              @click="$emit('open-related', item.id)"
            >
              <img
                v-if="item.cover_url"
                class="detail__related-thumb"
                :src="item.cover_url"
                :alt="item.title"
                loading="lazy"
              />
              <div class="detail__related-body">
                <h3 class="detail__related-headline">{{ item.title }}</h3>
                <p v-if="item.description" class="detail__related-desc">
                  {{ item.description }}
                </p>
                <span class="detail__related-meta">
                  {{ item.source || '头条资讯' }} · {{ item.view_count }} 阅读
                </span>
              </div>
            </li>
          </ul>
        </section>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NewsDetail',
}
</script>

<style scoped>
.detail {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
  padding-top: var(--safe-top);
}

.detail__header {
  flex-shrink: 0;
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-border);
}

.detail__back {
  font-size: 1rem;
  color: var(--color-primary);
}

.detail__scroll {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: calc(var(--safe-bottom) + 24px);
}

.detail__title {
  margin: 0 0 12px;
  font-size: 1.375rem;
  line-height: 1.35;
  font-weight: 700;
}

.detail__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  margin-bottom: 16px;
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
}

.detail__hero {
  width: 100%;
  max-height: 220px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 16px;
}

.detail__content {
  font-size: 1.0625rem;
  line-height: 1.75;
  color: var(--color-text);
  white-space: pre-wrap;
}

.detail__loading {
  margin: 0;
  color: var(--color-text-secondary);
}

.detail__related {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
}

.detail__related-title {
  margin: 0 0 12px;
  font-size: 1.0625rem;
  font-weight: 700;
}

.detail__related-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.detail__related-item {
  display: flex;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
}

.detail__related-item:last-child {
  border-bottom: none;
}

.detail__related-thumb {
  flex-shrink: 0;
  width: 96px;
  height: 72px;
  object-fit: cover;
  border-radius: 6px;
}

.detail__related-body {
  flex: 1;
  min-width: 0;
}

.detail__related-headline {
  margin: 0 0 4px;
  font-size: 0.9375rem;
  line-height: 1.4;
  font-weight: 600;
}

.detail__related-desc {
  margin: 0 0 6px;
  font-size: 0.8125rem;
  line-height: 1.45;
  color: var(--color-text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.detail__related-meta {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
}
</style>
