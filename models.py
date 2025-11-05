# models.py 文件内容
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

# 联系人表模型（对应 MySQL 中的 contacts 表）
class Contact(Base):
    __tablename__ = "contacts"  # 表名

    # 字段定义
    id = Column(Integer, primary_key=True, index=True)  # 主键（自增）
    name = Column(String(50), index=True, nullable=False)  # 姓名（非空）
    phone = Column(String(20), unique=True, index=True, nullable=False)  # 电话（唯一、非空）
    email = Column(String(100), nullable=True)  # 邮箱（可选）
    category = Column(String(20), nullable=False)  # 分类（如“家人”“同事”，非空）
    avatar = Column(String(255), nullable=True)  # 头像 URL（可选）
    create_time = Column(DateTime, default=datetime.now)  # 创建时间（默认当前时间）