<script setup>
import { onMounted, ref } from 'vue'
import { clearAllFavorites, fetchFavorites, removeFavorite } from '../api/favorites'

const emit = defineEmits(['back', 'open-news'])

const DELETE_ACTION_WIDTH = 72

const list = ref([])
const loading = ref(true)
const error = ref('')
const openSwipeId = ref(null)
const drag = ref({
  newsId: null,
  startX: 0,
  startOffset: 0,
  offset: 0,
})

function formatDate(value) {
  if (!value) return ''
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value
  return d.toLocaleString('zh-CN', { hour12: false })
}

function swipeOffset(newsId) {
  if (drag.value.newsId === newsId) return drag.value.offset
  if (openSwipeId.value === newsId) return -DELETE_ACTION_WIDTH
  return 0
}

function onTouchStart(newsId, e) {
  const touch = e.touches[0]
  if (!touch) return
  if (openSwipeId.value != null && openSwipeId.value !== newsId) {
    openSwipeId.value = null
  }
  const current = swipeOffset(newsId)
  drag.value = {
    newsId,
    startX: touch.clientX,
    startOffset: current,
    offset: current,
  }
}

function onTouchMove(newsId, e) {
  if (drag.value.newsId !== newsId) return
  const touch = e.touches[0]
  if (!touch) return
  const delta = touch.clientX - drag.value.startX
  let next = drag.value.startOffset + delta
  if (next > 0) next = 0
  if (next < -DELETE_ACTION_WIDTH) next = -DELETE_ACTION_WIDTH
  drag.value.offset = next
}

function onTouchEnd(newsId) {
  if (drag.value.newsId !== newsId) return
  const shouldOpen = drag.value.offset < -DELETE_ACTION_WIDTH / 2
  openSwipeId.value = shouldOpen ? newsId : null
  drag.value = { newsId: null, startX: 0, startOffset: 0, offset: 0 }
}

function closeSwipe() {
  openSwipeId.value = null
}

async function loadList() {
  loading.value = true
  error.value = ''
  try {
    list.value = await fetchFavorites()
  } catch (e) {
    error.value = e.message || '加载收藏失败，请稍后重试'
    list.value = []
  } finally {
    loading.value = false
  }
}

async function onRemove(newsId) {
  closeSwipe()
  try {
    await removeFavorite(newsId)
    list.value = list.value.filter((item) => item.news_id !== newsId)
  } catch (e) {
    error.value = e.message || '取消收藏失败'
  }
}

async function onClearAll() {
  if (!list.value.length) return
  if (!window.confirm('确定清空全部收藏？')) return
  closeSwipe()
  try {
    await clearAllFavorites()
    list.value = []
  } catch (e) {
    error.value = e.message || '清空失败'
  }
}

function onOpenNews(newsId) {
  if (openSwipeId.value === newsId) {
    closeSwipe()
    return
  }
  if (openSwipeId.value != null) {
    closeSwipe()
    return
  }
  emit('open-news', newsId)
}

onMounted(() => {
  loadList()
})
</script>

<template>
  <div class="fav">
    <header class="fav__header">
      <button type="button" class="fav__back" @click="emit('back')">‹ 返回</button>
      <button
        type="button"
        class="fav__clear"
        :disabled="!list.length"
        @click="onClearAll"
      >
        清空
      </button>
    </header>

    <p v-if="loading" class="fav__hint">加载中...</p>
    <p v-else-if="error" class="fav__hint fav__hint--error">{{ error }}</p>
    <p v-else-if="!list.length" class="fav__hint">暂无收藏</p>

    <ul v-else class="fav__list" @click="closeSwipe">
      <li v-for="item in list" :key="item.news_id" class="fav__row">
        <div class="fav__actions" aria-hidden="true">
          <button
            type="button"
            class="fav__delete"
            @click.stop="onRemove(item.news_id)"
          >
            删除
          </button>
        </div>
        <div
          class="fav__slide"
          :class="{ 'fav__slide--dragging': drag.newsId === item.news_id }"
          :style="{ transform: `translateX(${swipeOffset(item.news_id)}px)` }"
          @touchstart.passive="onTouchStart(item.news_id, $event)"
          @touchmove="onTouchMove(item.news_id, $event)"
          @touchend="onTouchEnd(item.news_id)"
          @touchcancel="onTouchEnd(item.news_id)"
          @click.stop
        >
          <article class="fav__card">
            <button
              type="button"
              class="fav__main"
              @click="onOpenNews(item.news_id)"
            >
              <img
                v-if="item.cover_url"
                class="fav__thumb"
                :src="item.cover_url"
                :alt="item.title"
                loading="lazy"
              />
              <div v-else class="fav__thumb fav__thumb--placeholder" />
              <div class="fav__body">
                <h2 class="fav__headline">{{ item.title }}</h2>
                <p class="fav__meta">
                  {{ item.source || '头条资讯' }}
                  <template v-if="item.published_at">
                    {{ ' ' }}{{ formatDate(item.published_at) }}
                  </template>
                </p>
                <p class="fav__time">收藏时间：{{ formatDate(item.favorited_at) }}</p>
              </div>
            </button>
          </article>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.fav {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  padding-bottom: var(--safe-bottom);
}

.fav__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 12px 12px;
  border-bottom: 1px solid var(--color-border);
}

.fav__back {
  font-size: 1rem;
  color: var(--color-primary);
}

.fav__clear {
  font-size: 0.9375rem;
  color: var(--color-primary);
}

.fav__clear:disabled {
  color: var(--color-text-secondary);
}

.fav__hint {
  margin: 24px 16px;
  text-align: center;
  font-size: 0.9375rem;
  color: var(--color-text-secondary);
}

.fav__hint--error {
  color: #c0392b;
}

.fav__list {
  margin: 0;
  padding: 12px 16px;
  list-style: none;
}

.fav__row {
  position: relative;
  margin-bottom: 12px;
  border-radius: 10px;
  overflow: hidden;
}

.fav__actions {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 72px;
  display: flex;
  align-items: stretch;
}

.fav__delete {
  flex: 1;
  border: none;
  font-size: 0.875rem;
  font-weight: 600;
  color: #fff;
  background: #e74c3c;
  cursor: pointer;
}

.fav__slide {
  position: relative;
  z-index: 1;
  transition: transform 0.2s ease;
  touch-action: pan-y;
}

.fav__slide--dragging {
  transition: none;
}

.fav__card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

.fav__main {
  display: flex;
  gap: 10px;
  width: 100%;
  padding: 10px;
  text-align: left;
  border: none;
  background: transparent;
  min-width: 0;
}

.fav__thumb {
  flex-shrink: 0;
  width: 88px;
  height: 66px;
  object-fit: cover;
  border-radius: 6px;
}

.fav__thumb--placeholder {
  background: #eef0f3;
}

.fav__body {
  flex: 1;
  min-width: 0;
}

.fav__headline {
  margin: 0 0 6px;
  font-size: 0.9375rem;
  line-height: 1.4;
  font-weight: 600;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.fav__meta,
.fav__time {
  margin: 0 0 4px;
  font-size: 0.75rem;
  line-height: 1.4;
  color: var(--color-text-secondary);
}
</style>
