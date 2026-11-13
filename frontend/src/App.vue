<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { fetchCategories, fetchNewsDetail, fetchNewsList } from './api/news'
import NewsHeader from './components/NewsHeader.vue'
import CategoryTabBar from './components/CategoryTabBar.vue'
import BottomTabBar from './components/BottomTabBar.vue'
import NewsListItem from './components/NewsListItem.vue'
import NewsDetail from './components/NewsDetail.vue'
import AiChatView from './views/AiChatView.vue'
import MineView from './views/MineView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import ChangePasswordView from './views/ChangePasswordView.vue'
import FavoritesView from './views/FavoritesView.vue'
import AllCategoriesView from './views/AllCategoriesView.vue'
import { fetchCurrentUser } from './api/auth'
import { clearAuth, getStoredUser, loadAuth, saveAuth } from './utils/session'

const activeTab = ref('home')
const authScreen = ref(null)
/** @type {import('vue').Ref<null | 'password' | 'favorites'>} */
const mineScreen = ref(null)
const currentUser = ref(getStoredUser())
const tabTitles = {
  home: '新闻资讯',
  ai: 'AI问答',
  mine: '我的',
  login: '用户登录',
  register: '用户注册',
  password: '修改密码',
  favorites: '我的收藏',
}

const pageTitle = computed(() => {
  if (activeTab.value === 'mine' && authScreen.value === 'login') return tabTitles.login
  if (activeTab.value === 'mine' && authScreen.value === 'register') return tabTitles.register
  if (activeTab.value === 'mine' && mineScreen.value === 'password') return tabTitles.password
  if (activeTab.value === 'mine' && mineScreen.value === 'favorites') return tabTitles.favorites
  return tabTitles[activeTab.value] || '新闻资讯'
})

const isLoggedIn = computed(() => Boolean(currentUser.value && loadAuth()?.token))

const showAllCategories = ref(false)

const hideBottomBar = computed(() => Boolean(authScreen.value || mineScreen.value))

const DEFAULT_HOME_CATEGORY = '头条'
const HOME_TAB_ORDER = ['头条', '社会', '国内', '国际', '娱乐', '体育']
const ALL_CATEGORY_ORDER = [
  '头条',
  '社会',
  '国内',
  '国际',
  '娱乐',
  '体育',
  '科技',
  '财经',
  '推荐',
  '热点',
  '视频',
  '军事',
]
const PAGE_SIZE = 10
const LOAD_MORE_THRESHOLD_PX = 120

const categories = ref([])
const categoryRecords = ref([])
const allCategories = ref([...ALL_CATEGORY_ORDER])
const activeCategory = ref(DEFAULT_HOME_CATEGORY)
const newsList = ref([])
const listPage = ref(1)
const hasMore = ref(false)
const loading = ref(true)
const loadingMore = ref(false)
const error = ref('')
const contentRef = ref(null)

const detailVisible = ref(false)
const detailLoading = ref(false)
const detailArticle = ref(null)

function extractCategoryNames(list) {
  if (!Array.isArray(list)) return []
  return list.map((item) => (typeof item === 'string' ? item : item?.name)).filter(Boolean)
}

function normalizeCategoryNames(list) {
  const names = extractCategoryNames(list)
  const fromApi = HOME_TAB_ORDER.filter((name) => names.includes(name))
  return fromApi.length ? fromApi : names.length ? names.slice(0, 6) : HOME_TAB_ORDER
}

function normalizeAllCategories(list) {
  const names = extractCategoryNames(list)
  const fromOrder = ALL_CATEGORY_ORDER.filter((name) => names.includes(name))
  const extra = names.filter((name) => !ALL_CATEGORY_ORDER.includes(name))
  if (fromOrder.length) return [...fromOrder, ...extra]
  if (names.length) return names
  return [...ALL_CATEGORY_ORDER]
}

function resolveDefaultCategory() {
  return categories.value.includes(DEFAULT_HOME_CATEGORY)
    ? DEFAULT_HOME_CATEGORY
    : categories.value[0] || DEFAULT_HOME_CATEGORY
}

function categoryIdByName(name) {
  const row = categoryRecords.value.find((c) => c.name === name)
  return row?.id
}

async function loadCategories() {
  try {
    const list = await fetchCategories()
    categoryRecords.value = Array.isArray(list)
      ? list.filter((item) => item && typeof item === 'object' && item.id != null)
      : []
    categories.value = normalizeCategoryNames(list)
    allCategories.value = normalizeAllCategories(list)
    activeCategory.value = resolveDefaultCategory()
  } catch (e) {
    categories.value = HOME_TAB_ORDER
    allCategories.value = [...ALL_CATEGORY_ORDER]
    activeCategory.value = DEFAULT_HOME_CATEGORY
    error.value = e.message || '分类加载失败'
  }
}

async function loadNews() {
  if (!activeCategory.value) return
  const categoryId = categoryIdByName(activeCategory.value)
  if (!categoryId) return
  loading.value = true
  loadingMore.value = false
  error.value = ''
  listPage.value = 1
  hasMore.value = false
  try {
    const page = await fetchNewsList({
      categoryId,
      page: 1,
      pageSize: PAGE_SIZE,
    })
    newsList.value = page?.list || []
    hasMore.value = Boolean(page?.hasMore)
  } catch (e) {
    newsList.value = []
    error.value = e.message || '列表加载失败，请确认后端已启动 (8000)'
  } finally {
    loading.value = false
    await nextTick()
    if (contentRef.value) contentRef.value.scrollTop = 0
    await maybeFillViewport()
  }
}

async function maybeFillViewport() {
  await nextTick()
  const el = contentRef.value
  if (
    !el ||
    !hasMore.value ||
    loadingMore.value ||
    loading.value ||
    activeTab.value !== 'home'
  ) {
    return
  }
  if (el.scrollHeight <= el.clientHeight + LOAD_MORE_THRESHOLD_PX) {
    await loadMoreNews()
    if (hasMore.value) await maybeFillViewport()
  }
}

async function loadMoreNews() {
  if (!hasMore.value || loadingMore.value || loading.value) return
  if (!activeCategory.value || activeTab.value !== 'home') return
  const categoryId = categoryIdByName(activeCategory.value)
  if (!categoryId) return

  loadingMore.value = true
  const nextPage = listPage.value + 1
  try {
    const page = await fetchNewsList({
      categoryId,
      page: nextPage,
      pageSize: PAGE_SIZE,
    })
    const batch = page?.list || []
    if (batch.length) {
      newsList.value = [...newsList.value, ...batch]
    }
    listPage.value = nextPage
    hasMore.value = Boolean(page?.hasMore)
  } catch (e) {
    error.value = e.message || '加载更多失败'
  } finally {
    loadingMore.value = false
  }
}

function onContentScroll() {
  const el = contentRef.value
  if (
    !el ||
    activeTab.value !== 'home' ||
    detailVisible.value ||
    showAllCategories.value
  ) {
    return
  }
  if (!hasMore.value || loadingMore.value || loading.value) return
  const distanceToBottom = el.scrollHeight - el.scrollTop - el.clientHeight
  if (distanceToBottom <= LOAD_MORE_THRESHOLD_PX) {
    loadMoreNews()
  }
}

async function openDetail(id) {
  detailVisible.value = true
  detailLoading.value = true
  detailArticle.value = null
  try {
    detailArticle.value = await fetchNewsDetail(id)
  } catch (e) {
    error.value = e.message || '详情加载失败'
    detailVisible.value = false
  } finally {
    detailLoading.value = false
  }
}

function closeDetail() {
  detailVisible.value = false
  detailArticle.value = null
  loadNews()
}

watch(activeCategory, () => {
  if (activeTab.value === 'home') {
    loadNews()
  }
})

watch(activeTab, (tab) => {
  if (tab !== 'mine') {
    authScreen.value = null
    mineScreen.value = null
  }
  if (tab !== 'home') {
    detailVisible.value = false
    detailArticle.value = null
    showAllCategories.value = false
  }
  if (tab === 'home' && activeCategory.value && !newsList.value.length && !loading.value) {
    loadNews()
  }
  if (tab === 'mine' && loadAuth()?.token) {
    syncCurrentUserProfile().catch(() => {})
  }
})

function openLogin() {
  authScreen.value = 'login'
}

function openRegister() {
  authScreen.value = 'register'
}

function closeAuth() {
  authScreen.value = null
}

function openAllCategories() {
  detailVisible.value = false
  detailArticle.value = null
  showAllCategories.value = true
}

function closeAllCategories() {
  showAllCategories.value = false
}

function onPickCategoryFromAll(name) {
  activeCategory.value = name
  showAllCategories.value = false
}

async function syncCurrentUserProfile() {
  const profile = await fetchCurrentUser()
  currentUser.value = profile
  const saved = loadAuth()
  if (saved?.token) {
    saveAuth({ ...saved, user: profile })
  }
  return profile
}

async function onLoginSuccess() {
  try {
    await syncCurrentUserProfile()
  } catch {
    const saved = loadAuth()
    if (saved?.user) currentUser.value = saved.user
  }
  closeAuth()
}

async function onRegisterSuccess() {
  try {
    await syncCurrentUserProfile()
  } catch {
    /* ignore */
  }
  closeAuth()
}

function onLogout() {
  clearAuth()
  currentUser.value = null
  mineScreen.value = null
}

function closeMineSubScreen() {
  mineScreen.value = null
}

function openChangePassword() {
  mineScreen.value = 'password'
}

function openFavorites() {
  if (!isLoggedIn.value) {
    openLogin()
    return
  }
  mineScreen.value = 'favorites'
}

function onDetailNeedLogin() {
  activeTab.value = 'mine'
  openLogin()
}

function onFavoriteChange({ favorited }) {
  if (detailArticle.value) {
    detailArticle.value = { ...detailArticle.value, isFavorited: favorited }
  }
}

function openNewsFromFavorites(newsId) {
  activeTab.value = 'home'
  mineScreen.value = null
  openDetail(newsId)
}

function onPasswordChanged() {
  mineScreen.value = null
}

async function restoreSession() {
  const saved = loadAuth()
  if (!saved?.token) return
  try {
    const user = await fetchCurrentUser()
    currentUser.value = user
    saveAuth({ ...saved, user })
  } catch {
    clearAuth()
    currentUser.value = null
  }
}

onMounted(async () => {
  await restoreSession()
  await loadCategories()
  await loadNews()
  await nextTick()
  contentRef.value?.addEventListener('scroll', onContentScroll, { passive: true })
})

onUnmounted(() => {
  contentRef.value?.removeEventListener('scroll', onContentScroll)
})
</script>

<template>
  <div class="news-app">
    <AllCategoriesView
      v-if="activeTab === 'home' && showAllCategories"
      :categories="allCategories"
      :active-category="activeCategory"
      @back="closeAllCategories"
      @select="onPickCategoryFromAll"
    />
    <template v-else>
      <header class="news-app__top">
        <NewsHeader :title="pageTitle" />
        <CategoryTabBar
          v-if="activeTab === 'home'"
          v-model="activeCategory"
          :categories="categories"
          @more="openAllCategories"
        />
      </header>
      <main
        ref="contentRef"
        class="news-app__content"
        :class="{ 'news-app__content--mine': activeTab === 'mine' && !authScreen && !mineScreen }"
      >
      <template v-if="activeTab === 'home'">
        <p v-if="loading && !newsList.length" class="news-app__hint">加载中...</p>
        <p v-else-if="error && !newsList.length" class="news-app__hint news-app__hint--error">
          {{ error }}
        </p>
        <p v-else-if="!loading && !newsList.length" class="news-app__hint">暂无资讯</p>
        <template v-else>
          <NewsListItem
            v-for="item in newsList"
            :key="item.id"
            :item="item"
            @select="openDetail"
          />
          <p v-if="loadingMore" class="news-app__hint news-app__hint--more">加载更多...</p>
          <p
            v-else-if="!hasMore && newsList.length"
            class="news-app__hint news-app__hint--more"
          >
            没有更多了
          </p>
          <p v-else-if="error" class="news-app__hint news-app__hint--error">{{ error }}</p>
        </template>
      </template>
      <AiChatView v-else-if="activeTab === 'ai'" />
      <LoginView
        v-else-if="activeTab === 'mine' && authScreen === 'login'"
        @back="closeAuth"
        @success="onLoginSuccess"
        @go-register="openRegister"
      />
      <RegisterView
        v-else-if="activeTab === 'mine' && authScreen === 'register'"
        @back="closeAuth"
        @success="onRegisterSuccess"
        @go-login="openLogin"
      />
      <ChangePasswordView
        v-else-if="activeTab === 'mine' && mineScreen === 'password'"
        @back="closeMineSubScreen"
        @success="onPasswordChanged"
      />
      <FavoritesView
        v-else-if="activeTab === 'mine' && mineScreen === 'favorites'"
        @back="closeMineSubScreen"
        @open-news="openNewsFromFavorites"
      />
      <MineView
        v-else-if="activeTab === 'mine'"
        class="news-app__mine"
        :user="currentUser"
        @login="openLogin"
        @register="openRegister"
        @logout="onLogout"
        @change-password="openChangePassword"
        @favorites="openFavorites"
      />
      </main>
    </template>
    <BottomTabBar v-show="!hideBottomBar" v-model="activeTab" />
    <NewsDetail
      v-if="detailVisible && activeTab === 'home' && !showAllCategories"
      :article="detailArticle"
      :loading="detailLoading"
      :logged-in="isLoggedIn"
      @close="closeDetail"
      @open-related="openDetail"
      @need-login="onDetailNeedLogin"
      @favorite-change="onFavoriteChange"
    />
  </div>
</template>

<style scoped>
.news-app {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100%;
  height: 100%;
  height: 100dvh;
  overflow: hidden;
  background: var(--color-bg);
}

.news-app__top {
  flex-shrink: 0;
  z-index: 10;
  padding-top: var(--safe-top);
  background: var(--color-bg);
}

.news-app__content {
  flex: 1;
  min-height: 0;
  overflow-x: hidden;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-y: contain;
  padding: 0 16px;
  padding-bottom: calc(var(--bottom-bar-height) + var(--safe-bottom) + 0.75rem);
}

.news-app__hint {
  margin: 20px 0;
  font-size: 0.9375rem;
  color: var(--color-text-secondary);
}

.news-app__hint--error {
  color: #c0392b;
}

.news-app__hint--more {
  text-align: center;
  padding-bottom: 0.5rem;
}

.news-app__content--mine {
  display: flex;
  flex-direction: column;
}

:deep(.news-app__mine) {
  flex: 1;
  width: 100%;
}
</style>
