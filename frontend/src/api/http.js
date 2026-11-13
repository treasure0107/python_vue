import { authorizationHeader, clearAuth, getToken } from '../utils/session'

function parseErrorBody(bodyText, httpStatus) {
  if (!bodyText) return `请求失败 ${httpStatus}`
  try {
    const data = JSON.parse(bodyText)
    if (typeof data.message === 'string' && data.message) return data.message
    if (typeof data.detail === 'string') return data.detail
    if (Array.isArray(data.detail)) {
      return data.detail.map((d) => d.msg || JSON.stringify(d)).join('；')
    }
  } catch {
    if (bodyText.length < 200) return bodyText
  }
  return `请求失败 ${httpStatus}`
}

function unwrapApiPayload(payload) {
  if (
    payload &&
    typeof payload === 'object' &&
    !Array.isArray(payload) &&
    Object.prototype.hasOwnProperty.call(payload, 'code') &&
    Object.prototype.hasOwnProperty.call(payload, 'message')
  ) {
    const ok = payload.code === 200 || payload.code === 201
    if (!ok) {
      throw new Error(payload.message || '请求失败')
    }
    return payload.data
  }
  return payload
}

/**
 * 统一请求：若本地有 token，自动附加请求头 `Authorization: Bearer <token>`
 * @param {string} path 相对 /api 的路径
 * @param {object} [options]
 * @param {boolean} [options.requireAuth] 为 true 且无 token 时直接报错
 */
const DEFAULT_TIMEOUT_MS = 20000

function networkFriendlyError(error) {
  if (error?.name === 'AbortError') {
    return new Error('请求超时，请确认后端已启动（默认端口 8000）')
  }
  const msg = error?.message || ''
  if (/fetch|network|failed|reset|refused/i.test(msg)) {
    return new Error('无法连接服务，请确认后端已启动（默认端口 8000）')
  }
  return error instanceof Error ? error : new Error(String(error))
}

export async function apiRequest(path, options = {}) {
  const { requireAuth = false, timeout = DEFAULT_TIMEOUT_MS, ...fetchOptions } = options

  if (requireAuth && !getToken()) {
    throw new Error('请先登录')
  }

  const headers = {
    Accept: 'application/json',
    ...authorizationHeader(),
    ...fetchOptions.headers,
  }

  let body = fetchOptions.body
  if (
    body !== undefined &&
    body !== null &&
    typeof body === 'object' &&
    !(body instanceof FormData)
  ) {
    headers['Content-Type'] = 'application/json'
    body = JSON.stringify(body)
  }

  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeout)
  let res
  try {
    res = await fetch(`/api${path}`, {
      ...fetchOptions,
      headers,
      body,
      signal: controller.signal,
    })
  } catch (error) {
    throw networkFriendlyError(error)
  } finally {
    clearTimeout(timer)
  }
  const text = await res.text()

  if (res.status === 401) {
    clearAuth()
    throw new Error(parseErrorBody(text, 401) || '登录已失效，请重新登录')
  }

  if (!res.ok) {
    throw new Error(parseErrorBody(text, res.status))
  }

  if (!text) return null
  const payload = JSON.parse(text)
  return unwrapApiPayload(payload)
}
