# database.py 文件内容
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量获取数据库连接地址
DATABASE_URL = os.getenv("DATABASE_URL")

# 创建数据库引擎（负责与 MySQL 通信）
engine = create_engine(DATABASE_URL)

# 创建会话工厂（每次操作数据库时，通过工厂创建一个会话）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 数据库模型基类（所有表模型都继承这个类）
Base = declarative_base()

# 依赖函数：提供数据库会话（供 API 接口使用）
def get_db():
    db = SessionLocal()
    try:
        yield db  # 把会话传递给 API
    finally:
        db.close()  # 接口调用结束后，关闭会话