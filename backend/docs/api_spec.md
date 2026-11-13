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
- 实现：`utils/response.py`（`ApiResponseFactory.success` / `success_response`），路由声明 `response_model=ApiResponse[某 schemas 模型]`，各接口 `data` 类型见对应 `schemas/*.py`。

---

## Token 认证（无状态 HTTP）

1. **登录 / 注册** → 后端签发 token（**有效期 7 天**），先删除该用户旧令牌再写入，**每个 `user_id` 仅保留一条**，在 `data.token` 返回  
2. **前端** 将 token 存 localStorage（`toutiao_auth`）  
3. **后续请求** 在请求头携带：`Authorization: Bearer <token>`  
4. **需登录的接口** 通过 `get_current_user` 查库校验 token 是否有效、未过期  

| 项 | 说明 |
|----|------|
| Header | `Authorization` |
| 类型 | `Bearer`（持有者令牌） |
| 凭证 | `<token>` 字符串（注册/登录返回的 `data.token`） |

---

## 认证 `routers/auth.py`

| 方法 | 路径 | 说明 | data 类型 |
|------|------|------|-----------|
| POST | `/auth/register` | 注册：查重→bcrypt 入库→UUID 令牌 | `RegisterResponseData`（`token`、`userInfo`） |
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
| GET | `/news/{id}` | 详情（浏览量+1，含相关推荐；登录时带 `isFavorited`） | `NewsDetailData` |
| POST | `/news` | 创建 | `NewsOut`（code 201） |
| PUT | `/news/{id}` | 更新 | `NewsOut` |
| DELETE | `/news/{id}` | 删除 | `null` |

---

## 收藏 `routers/favorite.py`（需 Bearer）

| 方法 | 路径 | 说明 | data |
|------|------|------|------|
| GET | `/favorites` | 我的收藏列表 | `FavoriteListItem[]` |
| POST | `/favorites/{news_id}` | 切换收藏 | `FavoriteToggleData` |
| DELETE | `/favorites/{news_id}` | 取消单条 | `null` |
| DELETE | `/favorites` | 清空 | `FavoriteClearData` |

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
| `favorites` | `crud/favorite.py` |
