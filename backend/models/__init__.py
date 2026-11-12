"""导入全部模型，供 create_all 与关系解析使用。"""

from models.favorite import Favorite
from models.history import History
from models.news import News
from models.news_category import NewsCategory
from models.user_token import UserToken
from models.users import User

__all__ = [
    "User",
    "UserToken",
    "NewsCategory",
    "News",
    "Favorite",
    "History",
]
