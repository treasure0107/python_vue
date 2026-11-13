# 接口实现流程

与项目目录的对应关系：

1. **模块化路由 → API 接口规范**  
   - 规范文档：`docs/api_spec.md`  
   - 实现：`routers/*.py`（仅参数校验、调 crud、`success()` 响应）

2. **定义模型类 → 数据库表**  
   - 设计文档：`docs/database_design.md`、`sql/01_schema.sql`  
   - 实现：`models/*.py`

3. **crud 封装数据库操作**  
   - 实现：`crud/*.py`（`select` / `add` / 赋值更新 / `delete`）  
   - 缓存读写：`crud/news_cache.py`（Redis，供 crud 业务方法调用）

4. **路由调 crud 并响应**  
   - 类型外壳：`schemas/response.py` → `ApiResponse[T]`（OpenAPI）  
   - 构造工厂：`utils/response.py` → `success()` / `ApiResponseFactory`  
   - 业务 data：各类 `schemas/*.py`（`ConfigDict(from_attributes=True)`）  
   - 统一异常：`utils/exception_handlers.py` → `register_exception_handlers(app)`（HTTP / 422 / IntegrityError / SQLAlchemy / 兜底）
