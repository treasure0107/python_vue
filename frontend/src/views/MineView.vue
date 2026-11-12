<script setup>
import defaultAvatar from '../assets/hero.png'

defineProps({
  user: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['login', 'register', 'logout', 'profile'])

const displayName = (user) => user?.nickname || user?.username || '用户'
const avatarOf = (user) => user?.avatar || defaultAvatar
</script>

<template>
  <div class="mine">
    <div class="mine__card">
      <img
        class="mine__avatar"
        :src="user ? avatarOf(user) : defaultAvatar"
        alt=""
      />
      <p class="mine__name">{{ user ? displayName(user) : '未登录' }}</p>
      <p class="mine__hint">
        {{ user ? '管理账号与个人资料' : '登录后可同步收藏与历史' }}
      </p>
      <div v-if="!user" class="mine__actions">
        <button type="button" class="mine__btn mine__btn--primary" @click="emit('login')">
          登录
        </button>
        <button type="button" class="mine__btn mine__btn--ghost" @click="emit('register')">
          注册
        </button>
      </div>
      <button
        v-else
        type="button"
        class="mine__btn mine__btn--ghost mine__logout"
        @click="emit('logout')"
      >
        退出登录
      </button>
    </div>
    <ul class="mine__menu">
      <li>
        <button
          type="button"
          class="mine__row"
          :disabled="!user"
          @click="user && emit('profile')"
        >
          个人信息
          <span class="mine__chevron" aria-hidden="true">›</span>
        </button>
      </li>
      <li class="mine__row mine__row--muted">我的收藏（即将上线）</li>
      <li class="mine__row mine__row--muted">浏览历史（即将上线）</li>
    </ul>
  </div>
</template>

<style scoped>
.mine {
  padding: 1rem 0;
}

.mine__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem 1rem;
  margin-bottom: 0.75rem;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.mine__avatar {
  width: 3.5rem;
  height: 3.5rem;
  margin-bottom: 0.75rem;
  border-radius: 50%;
  object-fit: cover;
}

.mine__name {
  margin: 0 0 0.25rem;
  font-size: 1rem;
  font-weight: 600;
}

.mine__hint {
  margin: 0 0 1rem;
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
}

.mine__actions {
  display: flex;
  gap: 0.75rem;
  width: 100%;
  max-width: 16rem;
}

.mine__btn {
  flex: 1;
  height: 2.5rem;
  font-size: 0.9375rem;
  border-radius: 0.5rem;
}

.mine__btn--primary {
  color: #fff;
  background: var(--color-primary);
}

.mine__btn--ghost {
  color: var(--color-primary);
  background: #fff;
  border: 1px solid var(--color-primary);
}

.mine__logout {
  width: 100%;
  max-width: 16rem;
}

.mine__menu {
  margin: 0;
  padding: 0;
  list-style: none;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.mine__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 1rem;
  font-size: 0.9375rem;
  text-align: left;
  border: none;
  border-bottom: 1px solid var(--color-border);
  background: #fff;
  color: var(--color-text);
}

.mine__row:disabled {
  opacity: 0.45;
}

.mine__row--muted {
  color: var(--color-text-secondary);
  cursor: default;
}

.mine__menu li:last-child .mine__row {
  border-bottom: none;
}

.mine__chevron {
  color: #c0c4cc;
  font-size: 1.125rem;
}
</style>
