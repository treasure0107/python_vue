<script setup>
const activeKey = defineModel({ type: String, default: 'home' })

const tabs = [
  { key: 'home', label: '首页', icon: 'home' },
  { key: 'ai', label: 'AI问答', icon: 'chat' },
  { key: 'mine', label: '我的', icon: 'user' },
]

function selectTab(key) {
  activeKey.value = key
}
</script>

<template>
  <footer class="bottom-bar">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      type="button"
      class="bottom-bar__item"
      :class="{ 'bottom-bar__item--active': activeKey === tab.key }"
      @click="selectTab(tab.key)"
    >
      <span class="bottom-bar__icon" aria-hidden="true">
        <svg
          v-if="tab.icon === 'home'"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M4 10.5L12 4l8 6.5V20a1 1 0 01-1 1h-5v-6H10v6H5a1 1 0 01-1-1v-9.5z"
            stroke="currentColor"
            stroke-width="1.6"
            stroke-linejoin="round"
          />
        </svg>
        <svg
          v-else-if="tab.icon === 'chat'"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M5 6.5A2.5 2.5 0 017.5 4h9A2.5 2.5 0 0119 6.5v7A2.5 2.5 0 0116.5 16H10l-4.2 3.15A.8.8 0 015 18.5v-12z"
            stroke="currentColor"
            stroke-width="1.6"
            stroke-linejoin="round"
          />
          <circle cx="9" cy="10" r="1" fill="currentColor" />
          <circle cx="12" cy="10" r="1" fill="currentColor" />
          <circle cx="15" cy="10" r="1" fill="currentColor" />
        </svg>
        <svg
          v-else
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle cx="12" cy="8" r="3.5" stroke="currentColor" stroke-width="1.6" />
          <path
            d="M5 20c0-3.5 3.1-6 7-6s7 2.5 7 6"
            stroke="currentColor"
            stroke-width="1.6"
            stroke-linecap="round"
          />
        </svg>
      </span>
      <span class="bottom-bar__label">{{ tab.label }}</span>
    </button>
  </footer>
</template>

<style scoped>
.bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 100;
  display: flex;
  align-items: stretch;
  justify-content: space-around;
  min-height: var(--bottom-bar-height);
  padding: 0.375rem 0 calc(0.375rem + var(--safe-bottom));
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
}

.bottom-bar__item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 4px 0;
  color: var(--color-text-secondary);
}

.bottom-bar__item--active {
  color: var(--color-primary);
}

.bottom-bar__icon {
  display: flex;
  width: 26px;
  height: 26px;
}

.bottom-bar__icon svg {
  width: 100%;
  height: 100%;
}

.bottom-bar__label {
  font-size: 11px;
  line-height: 1.2;
}
</style>
