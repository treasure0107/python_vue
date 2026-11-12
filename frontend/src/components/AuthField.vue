<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, required: true },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  autocomplete: { type: String, default: '' },
  maxlength: { type: [Number, String], default: undefined },
})

defineEmits(['update:modelValue'])

/** 密码框是否明文显示（仅 type=password 时生效） */
const passwordVisible = ref(false)

const isPasswordField = computed(() => props.type === 'password')

const inputType = computed(() => {
  if (isPasswordField.value) {
    return passwordVisible.value ? 'text' : 'password'
  }
  return props.type
})

function togglePasswordVisible() {
  passwordVisible.value = !passwordVisible.value
}
</script>

<template>
  <label class="field">
    <span class="field__label">{{ label }}</span>
    <div class="field__control" :class="{ 'field__control--password': isPasswordField }">
      <input
        class="field__input"
        :class="{ 'field__input--password': isPasswordField }"
        :type="inputType"
        :value="modelValue"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        :maxlength="maxlength"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <button
        v-if="isPasswordField"
        type="button"
        class="field__toggle"
        :aria-label="passwordVisible ? '隐藏密码' : '显示密码'"
        :aria-pressed="passwordVisible"
        @click="togglePasswordVisible"
      >
        <!-- 显示密码：睁眼 -->
        <svg
          v-if="passwordVisible"
          class="field__icon"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7Z"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linejoin="round"
          />
          <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.8" />
        </svg>
        <!-- 隐藏密码：闭眼 -->
        <svg
          v-else
          class="field__icon"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            d="M3 3l18 18M10.58 10.58A2 2 0 0 0 12 15a2 2 0 0 0 1.42-.59M9.88 5.09A10.94 10.94 0 0 1 12 5c6.5 0 10 7 10 7a16.2 16.2 0 0 1-3.56 4.38M6.1 6.1C3.52 7.73 2 12 2 12s1.5 4.27 4 6"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
    </div>
  </label>
</template>

<style scoped>
.field {
  display: block;
  margin-bottom: 1rem;
}

.field__label {
  display: block;
  margin-bottom: 0.375rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.field__control {
  position: relative;
}

.field__control--password .field__input {
  padding-right: 2.75rem;
}

.field__input {
  width: 100%;
  height: 2.75rem;
  padding: 0 0.875rem;
  font-size: 1rem;
  color: var(--color-text);
  background: #fff;
  border: 1px solid #e8eaed;
  border-radius: 0.5rem;
  outline: none;
  transition: border-color 0.2s, background 0.2s;
}

.field__input:focus {
  background: var(--color-bg);
  border-color: var(--color-primary);
}

.field__input::placeholder {
  color: #c0c4cc;
}

.field__toggle {
  position: absolute;
  right: 0.25rem;
  top: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  padding: 0;
  color: #9aa0a6;
  background: transparent;
  border: none;
  border-radius: 0.375rem;
  transform: translateY(-50%);
  cursor: pointer;
}

.field__toggle:hover {
  color: var(--color-primary);
}

.field__toggle:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 1px;
}

.field__icon {
  width: 1.25rem;
  height: 1.25rem;
}
</style>
