import { apiRequest } from './http'

/** @returns {Promise<{ token: string, expires_at: string, user: object }>} */
export function login({ username, password }) {
  return apiRequest('/auth/login', {
    method: 'POST',
    body: { username, password },
  })
}

/** @returns {Promise<{ token: string, expires_at: string, user: object }>} */
export function fetchCurrentUser() {
  return apiRequest('/auth/me')
}

export function register({ username, password, email, nickname }) {
  return apiRequest('/auth/register', {
    method: 'POST',
    body: {
      username,
      password,
      email: email || undefined,
      nickname: nickname || username,
    },
  })
}

/** 更新昵称、头像、个人简介 */
export function updateProfile(body) {
  return apiRequest('/auth/profile', {
    method: 'PATCH',
    body,
  })
}

/** 修改登录密码 */
export function changePassword({ old_password, new_password }) {
  return apiRequest('/auth/password', {
    method: 'POST',
    body: { old_password, new_password },
  })
}
