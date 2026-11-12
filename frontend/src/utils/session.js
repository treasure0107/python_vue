/**
 * 客户端 Token 会话（localStorage）
 * 流程：登录/注册 → 保存 token → 每次请求头 Authorization: Bearer <token>
 */

const STORAGE_KEY = 'toutiao_auth'

export function loadAuth() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function saveAuth(payload) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
}

export function clearAuth() {
  localStorage.removeItem(STORAGE_KEY)
}

/** 从 localStorage 读取访问令牌（不含 Bearer 前缀） */
export function getToken() {
  const token = loadAuth()?.token
  return token ? String(token).trim() : ''
}

export function getStoredUser() {
  return loadAuth()?.user || null
}

export function isLoggedIn() {
  return Boolean(getToken())
}

/**
 * 登录/注册接口 data 落库：token + 用户信息 + 过期时间
 * @param {object} data 接口返回的 data（含 token、user 或 userInfo）
 */
export function persistAuthFromResponse(data) {
  const token = data?.token
  if (!token) {
    throw new Error('服务端未返回访问令牌')
  }
  const user = data.userInfo || data.user || null
  saveAuth({
    token: String(token).trim(),
    expiresAt: data.expires_at ?? null,
    user,
  })
  return user
}

/** 构造标准请求头：Authorization: Bearer <token> */
export function authorizationHeader() {
  const token = getToken()
  if (!token) return {}
  return { Authorization: `Bearer ${token}` }
}
