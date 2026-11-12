import { apiRequest } from './http'

/** 登录：返回 data.token，由 persistAuthFromResponse 写入本地 */
export function login({ username, password }) {
  return apiRequest('/auth/login', {
    method: 'POST',
    body: { username, password },
  })
}

/** @returns {Promise<{ token: string, expires_at: string, user: object }>} */
/** 需 Bearer Token，请求头 Authorization: Bearer <token> */
export function fetchCurrentUser() {
  return apiRequest('/auth/me', { requireAuth: true })
}

/** 注册：仅需用户名与密码，返回 { token, userInfo, expires_at? } */
export function register({ username, password }) {
  return apiRequest('/auth/register', {
    method: 'POST',
    body: { username, password },
  })
}

/** 更新昵称、头像、个人简介 */
export function updateProfile(body) {
  return apiRequest('/auth/profile', {
    method: 'PATCH',
    body,
    requireAuth: true,
  })
}

/** 修改登录密码 */
export function changePassword({ old_password, new_password }) {
  return apiRequest('/auth/password', {
    method: 'POST',
    body: { old_password, new_password },
    requireAuth: true,
  })
}
