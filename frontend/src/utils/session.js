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

export function getToken() {
  return loadAuth()?.token || ''
}

export function getStoredUser() {
  return loadAuth()?.user || null
}
