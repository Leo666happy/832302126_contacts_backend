# crud.py 文件内容
from sqlalchemy.orm import Session
from models import Contact
from schemas import ContactCreate
from fastapi import HTTPException

# 获取所有联系人
def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

# 按 ID 获取单个联系人
def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

# 搜索联系人（姓名或电话包含关键词）
def search_contacts(db: Session, keyword: str):
    return db.query(Contact).filter(
        (Contact.name.contains(keyword)) | (Contact.phone.contains(keyword))
    ).all()

# 创建新联系人
def create_contact(db: Session, contact: ContactCreate):
    # 检查手机号是否已存在（避免重复）
    existing_contact = db.query(Contact).filter(Contact.phone == contact.phone).first()
    if existing_contact:
        raise HTTPException(status_code=400, detail="该手机号已被注册")
    
    # 新建联系人对象，关联到数据库
    db_contact = Contact(
        name=contact.name,
        phone=contact.phone,
        email=contact.email,
        category=contact.category,
        avatar=contact.avatar
    )
    db.add(db_contact)  # 添加到数据库会话
    db.commit()         # 提交事务（保存到 MySQL）
    db.refresh(db_contact)  # 刷新对象，获取数据库自动生成的 id 和 create_time
    return db_contact

# 更新联系人
def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    # 查找要更新的联系人
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    
    # 若修改了手机号，检查新手机号是否已被占用
    if contact.phone != db_contact.phone:
        existing_contact = db.query(Contact).filter(Contact.phone == contact.phone).first()
        if existing_contact:
            raise HTTPException(status_code=400, detail="该手机号已被使用")
    
    # 更新字段（遍历 contact 的所有属性，覆盖到 db_contact）
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

# 删除联系人
def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    
    db.delete(db_contact)
    db.commit()
    return {"detail": "联系人删除成功"}