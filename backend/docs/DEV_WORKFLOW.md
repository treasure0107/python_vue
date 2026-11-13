# 接口实现流程

与项目目录的对应关系：

1. **模块化路由 → API 接口规范**  
   - 规范文档：`docs/api_spec.md`（新接口须补充表行）  
   - 实现：`routers/*.py`（**仅**：参数校验、`Depends` 鉴权、调 `crud`、`success_response`）  
   - 入口：`main.py` → `app.include_router(..., prefix="/api")`

2. **定义模型类 → 数据库表**  
   - 设计文档：`docs/database_design.md`、`sql/01_schema.sql`  
   - 实现：`models/*.py`  
   - 本地建表：`python scripts/init_db.py`

3. **crud 封装数据库操作**  
   - 实现：`crud/*.py`（`select` / `add` / `delete` / 业务组合）  
   - 缓存：`crud/news_cache.py`（Redis，由 news 相关 crud 调用）  
   - **业务逻辑不进 router**（例：收藏校验、详情 `isFavorited` 在 `crud`）

4. **路由调 crud 并响应**  
   - 类型外壳：`schemas/response.py` → `ApiResponse[T]`（OpenAPI）  
   - 构造工厂：`utils/response.py` → `return success_response("提示", data)`  
   - 业务 data：各类 `schemas/*.py`（`ConfigDict(from_attributes=True)` 按需）  
   - 统一异常：`register_exception_handlers(app)`（`utils/exception_handlers.py`）

5. **前端（Vue）**  
   - API 封装：`frontend/src/api/*.js` → `apiRequest` + 统一 `code/message/data`  
   - 页面/组件：`views/`、`components/`

---

## 新功能自检清单（以「收藏 / 浏览历史」为例）

| 步骤 | 收藏模块落点 |
|------|----------------|
| 表已存在 | `models/favorite.py`、`sql/01_schema.sql` |
| data 模型 | `schemas/favorite.py` |
| 数据库操作 | `crud/favorite.py` |
| HTTP 路由 | `routers/favorite.py` + `main.py` 注册 |
| 关联能力 | 详情 `isFavorited` → `crud/news.py` 调 `crud/favorite.py` |
| 需登录 | `dependencies/auth.py` → `get_current_user` / `get_optional_user` |
| 文档 | `docs/api_spec.md`、`docs/database_design.md` |
| 前端 | `api/favorites.js`、`FavoritesView.vue`、`NewsDetail.vue` |
| 浏览历史 | `crud/history.py`、`routers/history.py`；打开详情时 `POST /history/add` |
| 历史前端 | `api/history.js`、`HistoryView.vue` |

---

## 分层原则（简记）

```
请求 → router（薄）→ crud（厚）→ models / DB
                ↓
         schemas（入参/出参）
                ↓
         success_response → { code, message, data }
```

- 主动业务错误：`raise HTTPException(detail="...")` → 全局处理器转统一 JSON。  
- 数据库约束失败：`IntegrityError` 等由全局处理器映射中文提示。
