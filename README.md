# python_vue

头条资讯全栈示例：FastAPI 后端 + Vue 3 前端。

## 目录

- `backend/` — API（FastAPI、MySQL）
- `frontend/` — Web（Vite + Vue 3）

## 本地运行

详见 `backend/docs/DEV_WORKFLOW.md`。需配置根目录 `.env`（勿提交仓库），各自安装依赖：

```bash
# 后端
cd backend && python -m venv .venv && pip install -r requirements.txt

# 前端
cd frontend && npm install
```
