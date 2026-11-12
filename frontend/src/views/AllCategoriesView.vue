<script setup>
import CategoryIcon from '../components/CategoryIcon.vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
  activeCategory: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['back', 'select'])

function isActive(name) {
  return name === props.activeCategory
}
</script>

<template>
  <section class="all-cat" aria-label="全部分类">
    <header class="all-cat__header">
      <button type="button" class="all-cat__back" @click="emit('back')">
        <span class="all-cat__back-icon" aria-hidden="true">‹</span>
        返回
      </button>
      <h1 class="all-cat__title">全部分类</h1>
      <span class="all-cat__header-spacer" aria-hidden="true" />
    </header>

    <div class="all-cat__body">
      <div class="all-cat__panel">
        <p class="all-cat__tip">选择频道，浏览你关心的资讯</p>
        <ul class="all-cat__grid">
          <li v-for="name in categories" :key="name">
            <button
              type="button"
              class="all-cat__card"
              :class="{ 'all-cat__card--active': isActive(name) }"
              @click="emit('select', name)"
            >
              <span class="all-cat__icon">
                <CategoryIcon :name="name" />
              </span>
              <span class="all-cat__label">{{ name }}</span>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.all-cat {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  background: #f3f5f8;
}

.all-cat__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  padding: 0.75rem 1rem;
  padding-top: calc(0.75rem + var(--safe-top));
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
}

.all-cat__back {
  display: flex;
  align-items: center;
  gap: 0.125rem;
  min-width: 4.5rem;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--color-primary);
}

.all-cat__back-icon {
  font-size: 1.5rem;
  line-height: 1;
  margin-top: -0.15rem;
}

.all-cat__title {
  margin: 0;
  font-size: 1.0625rem;
  font-weight: 600;
  color: var(--color-text);
  letter-spacing: 0.02em;
}

.all-cat__header-spacer {
  min-width: 4.5rem;
}

.all-cat__body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-y: contain;
  padding: 0.75rem 1rem 1rem;
}

.all-cat__panel {
  padding: 1rem 0.875rem 1.25rem;
  background: var(--color-bg);
  border-radius: 0.625rem;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
}

.all-cat__tip {
  margin: 0 0 0.875rem;
  padding: 0 0.125rem;
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
}

.all-cat__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.625rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.all-cat__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  aspect-ratio: 1;
  max-height: 6.25rem;
  padding: 0.625rem 0.375rem;
  background: #f6f7f9;
  border: 1.5px solid transparent;
  border-radius: 0.5rem;
  transition:
    background 0.15s,
    border-color 0.15s,
    transform 0.1s;
}

.all-cat__card:active {
  transform: scale(0.98);
}

.all-cat__card--active {
  background: rgba(47, 124, 246, 0.08);
  border-color: rgba(47, 124, 246, 0.35);
}

.all-cat__card--active .all-cat__icon {
  color: var(--color-primary);
}

.all-cat__card--active .all-cat__label {
  color: var(--color-primary);
  font-weight: 600;
}

.all-cat__icon {
  display: flex;
  width: 2rem;
  height: 2rem;
  margin-bottom: 0.375rem;
  color: #5b8def;
}

.all-cat__icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.all-cat__label {
  font-size: 0.8125rem;
  line-height: 1.2;
  color: var(--color-text);
}
</style>
