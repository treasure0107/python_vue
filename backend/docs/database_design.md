# 1-5 数据库设计

| 表名 | 模型 | 说明 |
|------|------|------|
| `user` | `models/users.py` | 用户名、bcrypt 密码、昵称、头像、邮箱 |
| `user_token` | `models/user_token.py` | 登录令牌、`expires_at` |
| `news_category` | `models/news_category.py` | 新闻分类 |
| `news` | `models/news.py` | 资讯正文、`category_id`、来源、浏览量 |
| `favorite` | `models/favorite.py` | 用户收藏（user_id + news_id 唯一） |
| `history` | `models/history.py` | 浏览历史（user_id + news_id 唯一） |

建表脚本：`sql/01_schema.sql`  
本地初始化：`python scripts/init_db.py`
