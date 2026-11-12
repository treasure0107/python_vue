import { apiRequest } from './http'

export function fetchCategories() {
  return apiRequest('/news/categories')
}

/** @returns {Promise<{ list: object[], total: number, hasMore: boolean }>} */
export function fetchNewsList({ categoryId, page = 1, pageSize = 10 }) {
  const params = new URLSearchParams({
    categoryId: String(categoryId),
    page: String(page),
    pageSize: String(pageSize),
  })
  return apiRequest(`/news/list?${params}`)
}

export function fetchNewsDetail(id) {
  return apiRequest(`/news/${id}`)
}
