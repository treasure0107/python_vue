import { apiRequest } from './http'

/** @returns {Promise<object[]>} */
export async function fetchFavorites() {
  const data = await apiRequest('/favorites', { requireAuth: true })
  return Array.isArray(data) ? data : []
}

/** @returns {Promise<{ news_id: number, favorited: boolean }>} */
export function toggleFavorite(newsId) {
  return apiRequest(`/favorites/${newsId}`, {
    method: 'POST',
    requireAuth: true,
  })
}

export function removeFavorite(newsId) {
  return apiRequest(`/favorites/${newsId}`, {
    method: 'DELETE',
    requireAuth: true,
  })
}

export function clearAllFavorites() {
  return apiRequest('/favorites', {
    method: 'DELETE',
    requireAuth: true,
  })
}
