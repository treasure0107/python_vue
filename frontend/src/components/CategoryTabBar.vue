<script setup>
import { computed } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue', 'more'])

const activeIndex = computed(() => {
  const idx = props.categories.indexOf(props.modelValue)
  return idx >= 0 ? idx : 0
})

function selectTab(name, index) {
  emit('update:modelValue', name)
}
</script>

<template>
  <nav class="category-bar" aria-label="新闻分类">
    <div class="category-bar__scroll">
      <button
        v-for="(item, index) in categories"
        :key="item"
        type="button"
        class="category-bar__item"
        :class="{ 'category-bar__item--active': activeIndex === index }"
        @click="selectTab(item, index)"
      >
        {{ item }}
      </button>
    </div>
    <button type="button" class="category-bar__more" @click="emit('more')">
      更多
      <span class="category-bar__more-icon" aria-hidden="true">&gt;</span>
    </button>
  </nav>
</template>

<style scoped>
.category-bar {
  display: flex;
  align-items: stretch;
  flex-shrink: 0;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
}

.category-bar__scroll {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0 8px 0 12px;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.category-bar__scroll::-webkit-scrollbar {
  display: none;
}

.category-bar__item {
  flex-shrink: 0;
  position: relative;
  padding: 10px 10px 12px;
  font-size: 15px;
  line-height: 1.2;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.category-bar__item--active {
  color: var(--color-primary);
  font-weight: 500;
}

.category-bar__item--active::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 28px;
  height: 3px;
  margin-left: -14px;
  background: var(--color-primary);
  border-radius: 2px;
}

.category-bar__more {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 0 14px 0 10px;
  font-size: 14px;
  color: var(--color-primary);
  border-left: 1px solid var(--color-border);
}

.category-bar__more-icon {
  font-size: 12px;
  font-weight: 600;
}
</style>
