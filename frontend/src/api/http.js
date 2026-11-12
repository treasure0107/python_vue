import { getToken } from '../utils/session'

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

export async function apiRequest(path, options = {}) {
  const headers = {
    Accept: 'application/json',
    ...options.headers,
  }

  let body = options.body
  if (body !== undefined && body !== null && typeof body === 'object' && !(body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
    body = JSON.stringify(body)
  }

  const token = getToken()
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const res = await fetch(`/api${path}`, { ...options, headers, body })
  const text = await res.text()

  if (!res.ok) {
    throw new Error(parseErrorBody(text, res.status))
  }

  if (!text) return null
  const payload = JSON.parse(text)
  return unwrapApiPayload(payload)
}
