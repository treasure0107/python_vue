<script setup>
import { computed, onMounted, ref } from 'vue'
import defaultAvatar from '../assets/hero.png'
import { fetchCurrentUser, updateProfile } from '../api/auth'
import { saveAuth, loadAuth } from '../utils/session'

const emit = defineEmits(['back', 'change-password', 'updated'])

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const profile = ref(null)
const editingBio = ref(false)
const bioDraft = ref('')

const avatarSrc = computed(
  () => profile.value?.avatar || defaultAvatar,
)

const bioText = computed(
  () => profile.value?.bio || '这个人很懒，还没有写简介',
)

async function loadProfile() {
  loading.value = true
  error.value = ''
  try {
    profile.value = await fetchCurrentUser()
    bioDraft.value = profile.value?.bio || ''
  } catch (e) {
    error.value = e.message || '加载失败'
  } finally {
    loading.value = false
  }
}

function startEditBio() {
  bioDraft.value = profile.value?.bio || ''
  editingBio.value = true
}

async function saveBio() {
  saving.value = true
  error.value = ''
  try {
    const next = await updateProfile({ bio: bioDraft.value.trim() || null })
    profile.value = next
    editingBio.value = false
    const saved = loadAuth()
    if (saved?.token) {
      saveAuth({ ...saved, user: next })
    }
    emit('updated', next)
  } catch (e) {
    error.value = e.message || '保存失败'
  } finally {
    saving.value = false
  }
}

function cancelBio() {
  editingBio.value = false
  bioDraft.value = profile.value?.bio || ''
}

onMounted(() => {
  loadProfile()
})
</script>

<template>
  <section class="profile">
    <button type="button" class="profile__back" @click="emit('back')">‹ 返回</button>
    <h1 class="profile__title">个人信息</h1>

    <p v-if="loading" class="profile__hint">加载中...</p>
    <p v-else-if="error && !profile" class="profile__hint profile__hint--error">{{ error }}</p>

    <ul v-else-if="profile" class="profile__list">
      <li class="profile__row profile__row--avatar">
        <span class="profile__label">头像</span>
        <img class="profile__avatar" :src="avatarSrc" alt="" />
      </li>
      <li class="profile__row">
        <span class="profile__label">用户名</span>
        <span class="profile__value">{{ profile.username }}</span>
      </li>
      <li class="profile__row">
        <span class="profile__label">账号 ID</span>
        <span class="profile__value">ID: {{ profile.account_id }}</span>
      </li>
      <li class="profile__row profile__row--action" @click="startEditBio">
        <span class="profile__label">个人简介</span>
        <span class="profile__value profile__value--ellipsis">{{ bioText }}</span>
        <span class="profile__chevron" aria-hidden="true">›</span>
      </li>
      <li class="profile__row profile__row--action" @click="emit('change-password')">
        <span class="profile__label profile__label--solo">修改密码</span>
        <span class="profile__chevron" aria-hidden="true">›</span>
      </li>
    </ul>

    <div
      v-if="editingBio"
      class="profile__modal"
      role="dialog"
      aria-modal="true"
      aria-label="编辑个人简介"
      @click.self="cancelBio"
    >
      <div class="profile__modal-card">
        <h2 class="profile__modal-title">个人简介</h2>
        <textarea
          v-model="bioDraft"
          class="profile__textarea"
          rows="4"
          maxlength="512"
          placeholder="写点什么介绍自己"
        />
        <p v-if="error" class="profile__hint profile__hint--error">{{ error }}</p>
        <div class="profile__modal-actions">
          <button type="button" class="profile__btn profile__btn--ghost" @click="cancelBio">
            取消
          </button>
          <button
            type="button"
            class="profile__btn profile__btn--primary"
            :disabled="saving"
            @click="saveBio"
          >
            {{ saving ? '保存中…' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'UserProfileView',
}
</script>

<style scoped>
.profile {
  padding: 0.25rem 0 1.5rem;
}

.profile__back {
  margin-bottom: 0.5rem;
  font-size: 1rem;
  color: var(--color-primary);
}

.profile__title {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
}

.profile__hint {
  margin: 1rem 0;
  text-align: center;
  color: var(--color-text-secondary);
}

.profile__hint--error {
  color: #e74c3c;
}

.profile__list {
  margin: 0;
  padding: 0;
  list-style: none;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.profile__row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-height: 3.25rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--color-border);
}

.profile__row:last-child {
  border-bottom: none;
}

.profile__row--avatar {
  justify-content: space-between;
}

.profile__row--action {
  cursor: pointer;
}

.profile__label {
  flex-shrink: 0;
  font-size: 0.9375rem;
  color: var(--color-text);
}

.profile__label--solo {
  flex: 1;
}

.profile__value {
  flex: 1;
  text-align: right;
  font-size: 0.9375rem;
  color: var(--color-text-secondary);
}

.profile__value--ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile__avatar {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 50%;
  object-fit: cover;
}

.profile__chevron {
  color: #c0c4cc;
  font-size: 1.25rem;
}

.profile__modal {
  position: fixed;
  inset: 0;
  z-index: 120;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.45);
}

.profile__modal-card {
  width: 100%;
  max-width: 22rem;
  padding: 1.25rem;
  background: #fff;
  border-radius: 0.75rem;
}

.profile__modal-title {
  margin: 0 0 0.75rem;
  font-size: 1.0625rem;
  font-weight: 600;
}

.profile__textarea {
  width: 100%;
  padding: 0.75rem;
  font-size: 0.9375rem;
  line-height: 1.5;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  resize: vertical;
}

.profile__modal-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.profile__btn {
  flex: 1;
  height: 2.5rem;
  border-radius: 0.5rem;
  font-size: 0.9375rem;
}

.profile__btn--primary {
  color: #fff;
  background: var(--color-primary);
}

.profile__btn--ghost {
  color: var(--color-text-secondary);
  background: #f4f5f6;
}
</style>
