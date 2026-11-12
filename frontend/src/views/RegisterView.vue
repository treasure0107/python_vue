<script setup>
import { ref } from 'vue'
import { register } from '../api/auth'
import { persistAuthFromResponse } from '../utils/session'
import AuthField from '../components/AuthField.vue'
import AuthLayout from '../components/AuthLayout.vue'

const emit = defineEmits(['back', 'success', 'go-login'])

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const submitting = ref(false)
const error = ref('')

async function onSubmit() {
  error.value = ''
  const name = username.value.trim()
  if (name.length < 2) {
    error.value = '请输入用户名'
    return
  }
  if (password.value.length < 6) {
    error.value = '密码至少 6 位'
    return
  }
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  submitting.value = true
  try {
    const data = await register({
      username: name,
      password: password.value,
    })
    const user = persistAuthFromResponse(data)
    emit('success', user)
  } catch (e) {
    error.value = e.message || '注册失败'
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
    <AuthLayout title="用户注册">
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
          autocomplete="new-password"
          maxlength="128"
        />
        <AuthField
          v-model="confirmPassword"
          label="确认密码"
          type="password"
          placeholder="请再次输入密码"
          autocomplete="new-password"
          maxlength="128"
        />
        <p v-if="error" class="auth-form__error">{{ error }}</p>
        <button type="submit" class="auth-form__btn" :disabled="submitting">
          {{ submitting ? '提交中…' : '注册' }}
        </button>
      </form>
    </AuthLayout>
    <p class="auth-screen__footer">
      已有账号？
      <button type="button" class="auth-screen__link" @click="emit('go-login')">去登录</button>
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
