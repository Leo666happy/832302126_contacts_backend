# schemas.py 文件内容
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# 新增/修改联系人时，前端需要提交的数据格式（输入验证）
class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="姓名不能为空，最多50字")
    phone: str = Field(..., min_length=11, max_length=20, description="手机号至少11位")
    email: Optional[EmailStr] = None  # 可选，自动验证邮箱格式（如 xxx@xxx.com）
    category: str = Field(..., description="分类必须选择（家人/同事/朋友/其他）")
    avatar: Optional[str] = None  # 头像 URL（后端生成，前端可不传）

# 后端返回给前端的联系人数据格式（包含数据库自动生成的字段）
class Contact(ContactCreate):
    id: int  # 数据库自增的主键
    create_time: datetime  # 数据库自动记录的创建时间

    # 配置：允许从 SQLAlchemy 模型（ORM）转换为 Pydantic 模型
    class Config:
        from_attributes = True