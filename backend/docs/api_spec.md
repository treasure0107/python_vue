# API 接口规范

- 基础路径：`/api`
- 统一响应：

```json
{
  "code": 200,
  "message": "状态提示",
  "data": {}
}
```

- 失败：`code` 与 HTTP 状态一致，`data` 为 `null`，`message` 为错误说明。

---

## 认证 `routers/auth.py`

| 方法 | 路径 | 说明 | data 类型 |
|------|------|------|-----------|
| POST | `/auth/register` | 注册并返回令牌 | `AuthResponse` |
| POST | `/auth/login` | 登录 | `AuthResponse` |
| GET | `/auth/me` | 当前用户个人信息（Bearer） | `UserProfileOut`（含 `account_id`、`bio`） |
| PATCH | `/auth/profile` | 更新昵称/头像/简介 | `UserProfileOut` |
| POST | `/auth/password` | 修改密码 | `null` |

**AuthResponse**：`token`, `expires_at`, `user`（`UserOut`）

**UserProfileOut**：`UserOut` + `account_id`（如 `heima-00001`）

---

## 资讯 `routers/news.py`

| 方法 | 路径 | 说明 | data 类型 |
|------|------|------|-----------|
| GET | `/news/categories` | 分类列表 | `NewsCategoryOut[]`（id、name、sort_order、created_at、updated_at） |
| GET | `/news/list` | 列表 `?categoryId=&page=&pageSize=`（pageSize≤100） | `NewsListPageData` |
| GET | `/news` | 旧版列表 `?category=&skip=&limit=` | `NewsOut[]` |
| GET | `/news/{id}` | 详情（浏览量+1，含同分类相关推荐） | `NewsDetailData`（`views`、`relatedNews` 等） |
| POST | `/news` | 创建 | `NewsOut`（code 201） |
| PUT | `/news/{id}` | 更新 | `NewsOut` |
| DELETE | `/news/{id}` | 删除 | `null` |

---

## 用户 `routers/users.py`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/users` | 用户列表 |
| GET | `/users/{id}` | 用户详情 |
| POST | `/users` | 创建用户 |
| PUT | `/users/{id}` | 更新 |
| DELETE | `/users/{id}` | 删除 |

---

## 模块与 crud 映射

| 路由模块 | crud |
|----------|------|
| `auth` | `crud/auth.py`, `crud/users.py`, `crud/user_token.py` |
| `news` | `crud/news.py`, `crud/news_category.py`, `crud/news_cache.py` |
| `users` | `crud/users.py` |
