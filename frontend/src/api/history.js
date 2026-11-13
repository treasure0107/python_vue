import { apiRequest } from './http'

/** @returns {Promise<object>} userId / newsId / viewTime */
export function addHistory(newsId) {
  return apiRequest('/history/add', {
    method: 'POST',
    body: { newsId },
    requireAuth: true,
  })
}

/** @returns {Promise<{ list: object[], total: number, hasMore: boolean }>} */
export function fetchHistory({ page = 1, pageSize = 20 } = {}) {
  const params = new URLSearchParams({
    page: String(page),
    pageSize: String(pageSize),
  })
  return apiRequest(`/history/list?${params}`, { requireAuth: true })
}

export function removeHistory(historyId) {
  return apiRequest(`/history/${historyId}`, {
    method: 'DELETE',
    requireAuth: true,
  })
}

export function clearAllHistory() {
  return apiRequest('/history', {
    method: 'DELETE',
    requireAuth: true,
  })
}
