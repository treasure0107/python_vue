<script setup>
import { ref } from 'vue'
import { changePassword } from '../api/auth'
import AuthField from '../components/AuthField.vue'

const emit = defineEmits(['back', 'success'])

const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const submitting = ref(false)
const error = ref('')

async function onSubmit() {
  error.value = ''
  if (oldPassword.value.length < 6) {
    error.value = '请输入原密码'
    return
  }
  if (newPassword.value.length < 6) {
    error.value = '新密码至少 6 位'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    error.value = '两次输入的新密码不一致'
    return
  }
  submitting.value = true
  try {
    await changePassword({
      old_password: oldPassword.value,
      new_password: newPassword.value,
    })
    emit('success')
  } catch (e) {
    error.value = e.message || '修改失败'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="pwd">
    <header class="pwd__header">
      <button type="button" class="pwd__back" @click="emit('back')">‹ 返回</button>
    </header>
    <p class="pwd__tip">保存后请使用新密码重新登录。</p>

    <form class="pwd__card" @submit.prevent="onSubmit">
      <AuthField
        v-model="oldPassword"
        label="原密码"
        type="password"
        placeholder="请输入当前密码"
        autocomplete="current-password"
      />
      <AuthField
        v-model="newPassword"
        label="新密码"
        type="password"
        placeholder="至少 6 位"
        autocomplete="new-password"
      />
      <AuthField
        v-model="confirmPassword"
        label="确认新密码"
        type="password"
        placeholder="再次输入新密码"
        autocomplete="new-password"
      />
      <p v-if="error" class="pwd__error">{{ error }}</p>
      <button type="submit" class="pwd__btn" :disabled="submitting">
        {{ submitting ? '提交中…' : '确认修改' }}
      </button>
    </form>
  </section>
</template>

<style scoped>
.pwd {
  padding: 0 0 1.5rem;
}

.pwd__header {
  padding: 8px 0 12px;
  border-bottom: 1px solid var(--color-border);
}

.pwd__back {
  font-size: 1rem;
  color: var(--color-primary);
}

.pwd__tip {
  margin: 1rem 0 1rem;
  font-size: 0.8125rem;
  text-align: center;
  color: var(--color-text-secondary);
}

.pwd__card {
  padding: 1.25rem 1rem;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.pwd__error {
  margin: 0 0 0.75rem;
  font-size: 0.8125rem;
  color: #e74c3c;
}

.pwd__btn {
  width: 100%;
  height: 2.75rem;
  margin-top: 0.25rem;
  font-size: 1rem;
  font-weight: 500;
  color: #fff;
  background: var(--color-primary);
  border-radius: 0.5rem;
}

.pwd__btn:disabled {
  opacity: 0.65;
}
</style>
