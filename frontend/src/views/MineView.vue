<script setup>
import { computed } from 'vue'
import defaultAvatar from '../assets/hero.png'

const props = defineProps({
  user: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits([
  'login',
  'register',
  'logout',
  'change-password',
  'favorites',
  'history',
])

const avatarSrc = computed(
  () => (props.user?.avatar ? props.user.avatar : defaultAvatar),
)

const accountLabel = computed(() => {
  const u = props.user
  if (!u) return ''
  return u.account_id || (u.id != null ? `ID: ${u.id}` : '')
})

const bioText = computed(() => props.user?.bio?.trim() || '')
</script>

<template>
  <div class="mine">
    <div class="mine__main">
      <div class="mine__card" :class="{ 'mine__card--guest': !user }">
        <template v-if="user">
          <div class="mine__head">
            <img class="mine__avatar" :src="avatarSrc" alt="" />
            <div class="mine__info">
              <p class="mine__user">{{ user.username }}</p>
              <p v-if="accountLabel" class="mine__meta">{{ accountLabel }}</p>
              <p v-if="user.email" class="mine__meta">{{ user.email }}</p>
            </div>
          </div>
          <p v-if="bioText" class="mine__bio">{{ bioText }}</p>
        </template>

        <template v-else>
          <img class="mine__avatar mine__avatar--guest" :src="defaultAvatar" alt="" />
          <p class="mine__guest-title">未登录</p>
          <p class="mine__hint">登录后可查看账号信息、同步收藏与历史</p>
          <div class="mine__actions">
            <button type="button" class="mine__btn mine__btn--primary" @click="emit('login')">
              登录
            </button>
            <button type="button" class="mine__btn mine__btn--ghost" @click="emit('register')">
              注册
            </button>
          </div>
        </template>
      </div>

      <ul class="mine__menu">
        <li v-if="user">
          <button type="button" class="mine__row" @click="emit('change-password')">
            修改密码
            <span class="mine__chevron" aria-hidden="true">›</span>
          </button>
        </li>
        <li v-if="user">
          <button type="button" class="mine__row" @click="emit('favorites')">
            我的收藏
            <span class="mine__chevron" aria-hidden="true">›</span>
          </button>
        </li>
        <li v-if="user">
          <button type="button" class="mine__row" @click="emit('history')">
            浏览历史
            <span class="mine__chevron" aria-hidden="true">›</span>
          </button>
        </li>
      </ul>
    </div>

    <footer v-if="user" class="mine__footer">
      <button type="button" class="mine__logout" @click="emit('logout')">退出登录</button>
    </footer>
  </div>
</template>

<style scoped>
.mine {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  padding: 0.25rem 0 0;
}

.mine__main {
  flex: 1;
}

.mine__card {
  padding: 1rem;
  margin-bottom: 0.75rem;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.mine__card--guest {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.25rem 1rem;
}

.mine__head {
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.mine__avatar {
  flex-shrink: 0;
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 50%;
  object-fit: cover;
}

.mine__avatar--guest {
  width: 3.5rem;
  height: 3.5rem;
  margin-bottom: 0.625rem;
}

.mine__info {
  flex: 1;
  min-width: 0;
}

.mine__user {
  margin: 0 0 0.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.3;
}

.mine__meta {
  margin: 0.125rem 0 0;
  font-size: 0.8125rem;
  line-height: 1.45;
  color: var(--color-text-secondary);
  word-break: break-all;
}

.mine__bio {
  margin: 0.75rem 0 0;
  padding-top: 0.75rem;
  font-size: 0.8125rem;
  line-height: 1.55;
  color: var(--color-text-secondary);
  border-top: 1px solid #f2f3f5;
}

.mine__guest-title {
  margin: 0 0 0.25rem;
  font-size: 1.0625rem;
  font-weight: 600;
}

.mine__hint {
  margin: 0 0 1rem;
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  text-align: center;
  line-height: 1.45;
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

.mine__footer {
  flex-shrink: 0;
  padding: 2rem 0 0.5rem;
  margin-top: auto;
}

.mine__logout {
  width: 100%;
  height: 2.75rem;
  font-size: 0.9375rem;
  color: var(--color-primary);
  background: #fff;
  border: 1px solid var(--color-primary);
  border-radius: 0.5rem;
}

.mine__logout:active {
  opacity: 0.9;
}
</style>
