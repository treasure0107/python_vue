<script setup>
defineProps({
  name: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <!-- 头条 -->
    <template v-if="name === '头条'">
      <path
        d="M14 10h20l2 4v24H12V14l2-4z"
        stroke="currentColor"
        stroke-width="2"
        stroke-linejoin="round"
      />
      <path d="M18 20h12M18 26h12M18 32h8" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
      <circle cx="30" cy="16" r="5" fill="currentColor" opacity="0.25" />
    </template>
    <!-- 社会 -->
    <template v-else-if="name === '社会'">
      <circle cx="18" cy="16" r="4" stroke="currentColor" stroke-width="2" />
      <circle cx="30" cy="16" r="4" stroke="currentColor" stroke-width="2" />
      <path
        d="M10 38c0-5 4-8 8-8s8 3 8 3M22 38c0-5 4-8 8-8s8 3 8 3"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
      />
    </template>
    <!-- 国内 -->
    <template v-else-if="name === '国内'">
      <path
        d="M16 36V20l8-6 8 6v16"
        stroke="currentColor"
        stroke-width="2"
        stroke-linejoin="round"
      />
      <path d="M20 36v-8h8v8" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
    </template>
    <!-- 国际 -->
    <template v-else-if="name === '国际'">
      <circle cx="24" cy="24" r="13" stroke="currentColor" stroke-width="2" />
      <path
        d="M24 11c-4 4-6 8-6 13s2 9 6 13M24 11c4 4 6 8 6 13s-2 9-6 13M11 24h26M14 18h20M14 30h20"
        stroke="currentColor"
        stroke-width="1.5"
        stroke-linecap="round"
      />
    </template>
    <!-- 娱乐 -->
    <template v-else-if="name === '娱乐'">
      <path
        d="M16 14l4 12 4-8 4 8 4-12"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <circle cx="24" cy="34" r="2" fill="currentColor" />
    </template>
    <!-- 体育 -->
    <template v-else-if="name === '体育'">
      <circle cx="24" cy="24" r="12" stroke="currentColor" stroke-width="2" />
      <path
        d="M24 12v24M12 24h24M15 17l18 14M33 17L15 31"
        stroke="currentColor"
        stroke-width="1.5"
        stroke-linecap="round"
      />
    </template>
    <!-- 科技 -->
    <template v-else-if="name === '科技'">
      <rect x="14" y="14" width="20" height="20" rx="3" stroke="currentColor" stroke-width="2" />
      <path d="M18 20h12M18 26h8M18 32h5" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
      <circle cx="32" cy="32" r="2" fill="currentColor" />
    </template>
    <!-- 财经 -->
    <template v-else-if="name === '财经'">
      <path d="M14 34V18M22 34V14M30 34V22M38 34V10" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" />
      <path d="M12 34h28" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
    </template>
    <template v-else>
      <rect x="12" y="10" width="24" height="30" rx="2" stroke="currentColor" stroke-width="2" />
      <path d="M18 18h12M18 24h12M18 30h8" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
    </template>
  </svg>
</template>
