<script setup>
import { ref } from 'vue'
import { login } from '../api/auth'
import { persistAuthFromResponse } from '../utils/session'
import AuthField from '../components/AuthField.vue'
import AuthLayout from '../components/AuthLayout.vue'

const emit = defineEmits(['back', 'success', 'go-register'])

const username = ref('')
const password = ref('')
const submitting = ref(false)
const error = ref('')

async function onSubmit() {
  error.value = ''
  if (!username.value.trim()) {
    error.value = '请输入用户名'
    return
  }
  if (password.value.length < 6) {
    error.value = '密码至少 6 位'
    return
  }
  submitting.value = true
  try {
    const data = await login({
      username: username.value.trim(),
      password: password.value,
    })
    const user = persistAuthFromResponse(data)
    emit('success', user)
  } catch (e) {
    error.value = e.message || '登录失败'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="auth-screen">
    <button type="button" class="auth-screen__back" aria-label="返回" @click="emit('back')">
      ‹
    </button>
    <AuthLayout title="用户登录">
      <form class="auth-form" @submit.prevent="onSubmit">
        <AuthField
          v-model="username"
          label="用户名"
          placeholder="请输入用户名"
          autocomplete="username"
          maxlength="64"
        />
        <AuthField
          v-model="password"
          label="密码"
          type="password"
          placeholder="请输入密码"
          autocomplete="current-password"
          maxlength="128"
        />
        <p v-if="error" class="auth-form__error">{{ error }}</p>
        <button type="submit" class="auth-form__btn" :disabled="submitting">
          {{ submitting ? '登录中…' : '登录' }}
        </button>
      </form>
      <p class="auth-form__demo">
        测试账号：admin<br />
        测试密码：123456
      </p>
    </AuthLayout>
    <p class="auth-screen__footer">
      还没有账号？
      <button type="button" class="auth-screen__link" @click="emit('go-register')">立即注册</button>
    </p>
  </div>
</template>

<style scoped>
.auth-screen {
  position: relative;
  padding: 0 0.25rem;
}

.auth-screen__back {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  font-size: 1.75rem;
  line-height: 1;
  color: var(--color-text);
}

.auth-form__error {
  margin: 0 0 0.75rem;
  font-size: 0.8125rem;
  color: #e74c3c;
}

.auth-form__btn {
  width: 100%;
  height: 2.75rem;
  margin-top: 0.25rem;
  font-size: 1rem;
  font-weight: 500;
  color: #fff;
  background: var(--color-primary);
  border-radius: 0.5rem;
}

.auth-form__btn:disabled {
  opacity: 0.65;
}

.auth-form__demo {
  margin: 1rem 0 0;
  padding-top: 0.75rem;
  font-size: 0.8125rem;
  line-height: 1.6;
  color: var(--color-text-secondary);
  text-align: center;
  border-top: 1px solid var(--color-border);
}

.auth-screen__footer {
  margin: 1.25rem 0 0;
  font-size: 0.875rem;
  text-align: center;
  color: var(--color-text-secondary);
}

.auth-screen__link {
  color: var(--color-primary);
  font-size: inherit;
}
</style>
