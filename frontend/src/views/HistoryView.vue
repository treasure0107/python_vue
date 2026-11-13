<script setup>
import { onMounted, ref } from 'vue'
import {
  clearAllHistory,
  fetchHistory,
  removeHistory,
} from '../api/history'

const emit = defineEmits(['back', 'open-news'])

const DELETE_ACTION_WIDTH = 72

const list = ref([])
const loading = ref(true)
const error = ref('')
const openSwipeId = ref(null)
const drag = ref({
  id: null,
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

function swipeOffset(id) {
  if (drag.value.id === id) return drag.value.offset
  if (openSwipeId.value === id) return -DELETE_ACTION_WIDTH
  return 0
}

function onTouchStart(id, e) {
  const touch = e.touches[0]
  if (!touch) return
  if (openSwipeId.value != null && openSwipeId.value !== id) {
    openSwipeId.value = null
  }
  const current = swipeOffset(id)
  drag.value = {
    id,
    startX: touch.clientX,
    startOffset: current,
    offset: current,
  }
}

function onTouchMove(id, e) {
  if (drag.value.id !== id) return
  const touch = e.touches[0]
  if (!touch) return
  const delta = touch.clientX - drag.value.startX
  let next = drag.value.startOffset + delta
  if (next > 0) next = 0
  if (next < -DELETE_ACTION_WIDTH) next = -DELETE_ACTION_WIDTH
  drag.value.offset = next
}

function onTouchEnd(id) {
  if (drag.value.id !== id) return
  const shouldOpen = drag.value.offset < -DELETE_ACTION_WIDTH / 2
  openSwipeId.value = shouldOpen ? id : null
  drag.value = { id: null, startX: 0, startOffset: 0, offset: 0 }
}

function closeSwipe() {
  openSwipeId.value = null
}

async function loadList() {
  loading.value = true
  error.value = ''
  try {
    const data = await fetchHistory({ page: 1, pageSize: 100 })
    list.value = data?.list || []
  } catch (e) {
    error.value = e.message || '加载浏览历史失败，请稍后重试'
    list.value = []
  } finally {
    loading.value = false
  }
}

async function onRemove(historyId) {
  closeSwipe()
  try {
    await removeHistory(historyId)
    list.value = list.value.filter((item) => item.id !== historyId)
  } catch (e) {
    error.value = e.message || '删除失败'
  }
}

async function onClearAll() {
  if (!list.value.length) return
  if (!window.confirm('确定清空全部浏览历史？')) return
  closeSwipe()
  try {
    await clearAllHistory()
    list.value = []
  } catch (e) {
    error.value = e.message || '清空失败'
  }
}

function onOpenNews(newsId) {
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
  <div class="hist">
    <header class="hist__header">
      <button type="button" class="hist__back" @click="emit('back')">‹ 返回</button>
      <h1 class="hist__title">浏览历史</h1>
      <button
        type="button"
        class="hist__clear"
        :disabled="!list.length"
        @click="onClearAll"
      >
        清空
      </button>
    </header>

    <p v-if="loading" class="hist__hint">加载中...</p>
    <p v-else-if="error" class="hist__hint hist__hint--error">{{ error }}</p>
    <p v-else-if="!list.length" class="hist__hint">暂无浏览记录</p>

    <ul v-else class="hist__list" @click="closeSwipe">
      <li v-for="item in list" :key="item.id" class="hist__row">
        <div class="hist__actions" aria-hidden="true">
          <button
            type="button"
            class="hist__delete"
            @click.stop="onRemove(item.id)"
          >
            删除
          </button>
        </div>
        <div
          class="hist__slide"
          :class="{ 'hist__slide--dragging': drag.id === item.id }"
          :style="{ transform: `translateX(${swipeOffset(item.id)}px)` }"
          @touchstart.passive="onTouchStart(item.id, $event)"
          @touchmove="onTouchMove(item.id, $event)"
          @touchend="onTouchEnd(item.id)"
          @touchcancel="onTouchEnd(item.id)"
          @click.stop
        >
          <article class="hist__card">
            <button
              type="button"
              class="hist__main"
              @click="onOpenNews(item.news_id)"
            >
              <img
                v-if="item.cover_url"
                class="hist__thumb"
                :src="item.cover_url"
                :alt="item.title"
                loading="lazy"
              />
              <div v-else class="hist__thumb hist__thumb--placeholder" />
              <div class="hist__body">
                <h2 class="hist__headline">{{ item.title }}</h2>
                <p class="hist__meta">
                  {{ item.source || '头条资讯' }}
                  <template v-if="item.published_at">
                    {{ ' ' }}{{ formatDate(item.published_at) }}
                  </template>
                </p>
                <p class="hist__time">浏览时间：{{ formatDate(item.viewed_at) }}</p>
              </div>
            </button>
          </article>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.hist {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  padding-bottom: var(--safe-bottom);
}

.hist__header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 8px;
  padding: 8px 12px 12px;
  border-bottom: 1px solid var(--color-border);
}

.hist__back {
  justify-self: start;
  font-size: 1rem;
  color: var(--color-primary);
}

.hist__title {
  margin: 0;
  font-size: 1.0625rem;
  font-weight: 700;
  text-align: center;
}

.hist__clear {
  justify-self: end;
  font-size: 0.9375rem;
  color: var(--color-primary);
}

.hist__clear:disabled {
  color: var(--color-text-secondary);
}

.hist__hint {
  margin: 24px 16px;
  text-align: center;
  font-size: 0.9375rem;
  color: var(--color-text-secondary);
}

.hist__hint--error {
  color: #c0392b;
}

.hist__list {
  margin: 0;
  padding: 12px 16px;
  list-style: none;
}

.hist__row {
  position: relative;
  margin-bottom: 12px;
  border-radius: 10px;
  overflow: hidden;
}

.hist__actions {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 72px;
  display: flex;
  align-items: stretch;
}

.hist__delete {
  flex: 1;
  border: none;
  font-size: 0.875rem;
  font-weight: 600;
  color: #fff;
  background: #e74c3c;
  cursor: pointer;
}

.hist__slide {
  position: relative;
  z-index: 1;
  transition: transform 0.2s ease;
  touch-action: pan-y;
}

.hist__slide--dragging {
  transition: none;
}

.hist__card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

.hist__main {
  display: flex;
  gap: 10px;
  width: 100%;
  padding: 10px;
  text-align: left;
  border: none;
  background: transparent;
  min-width: 0;
}

.hist__thumb {
  flex-shrink: 0;
  width: 88px;
  height: 66px;
  object-fit: cover;
  border-radius: 6px;
}

.hist__thumb--placeholder {
  background: #eef0f3;
}

.hist__body {
  flex: 1;
  min-width: 0;
}

.hist__headline {
  margin: 0 0 6px;
  font-size: 0.9375rem;
  line-height: 1.4;
  font-weight: 600;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hist__meta,
.hist__time {
  margin: 0 0 4px;
  font-size: 0.75rem;
  line-height: 1.4;
  color: var(--color-text-secondary);
}
</style>
