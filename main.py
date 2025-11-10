# main.py 文件内容
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import shutil

# 导入自定义模块
from database import get_db, engine
from models import Base
from schemas import Contact, ContactCreate
from crud import (
    get_contacts, get_contact, create_contact,
    update_contact, delete_contact, search_contacts
)

# 加载环境变量
load_dotenv()

# 1. 创建数据库表（首次运行时自动创建，已存在则跳过）
Base.metadata.create_all(bind=engine)

# 2. 初始化 FastAPI 应用
app = FastAPI(title="通讯录后端 API", version="1.0")

# 3. 配置 CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 前端 Vue 运行地址（固定，除非你改了前端端口）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET/POST/PUT/DELETE）
    allow_headers=["*"],  # 允许所有请求头
)

# 4. 配置头像存储（创建文件夹，挂载静态文件）
os.makedirs("static/avatars", exist_ok=True)  # 新建文件夹存头像
app.mount("/static", StaticFiles(directory="static"), name="static")  # 前端可通过 URL 访问头像
AVATAR_PATH = "static/avatars/"  # 头像本地存储路径

# 5. 定义 API 接口（核心功能）
# 5.1 获取所有联系人
@app.get("/api/contacts", response_model=list[Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_contacts(db, skip=skip, limit=limit)

# 5.2 搜索联系人（按姓名/电话）
@app.get("/api/contacts/search", response_model=list[Contact])
def search_contact(keyword: str, db: Session = Depends(get_db)):
    return search_contacts(db, keyword=keyword)

# 5.3 获取单个联系人（按 ID）
@app.get("/api/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db, contact_id=contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    return db_contact

# 5.4 添加联系人（支持头像上传）
@app.post("/api/contacts", response_model=Contact)
def create_contact_api(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(None),
    category: str = Form(...),
    avatar: UploadFile = File(None),  # 头像文件（可选）
    db: Session = Depends(get_db)
):
    # 处理头像上传（若有）
    avatar_url = None
    if avatar:
        # 生成唯一文件名（避免重复，用手机号+原文件名）
        filename = f"{phone}_{avatar.filename}"
        file_save_path = os.path.join(AVATAR_PATH, filename)
        # 保存头像到本地文件夹
        with open(file_save_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        # 生成前端可访问的头像 URL（如：http://localhost:8000/static/avatars/13800138000_avatar.jpg）
        avatar_url = f"/static/avatars/{filename}"
    
    # 组装联系人数据，调用 crud 函数保存到数据库
    contact_data = ContactCreate(
        name=name, phone=phone, email=email, category=category, avatar=avatar_url
    )
    return create_contact(db=db, contact=contact_data)

# 5.5 修改联系人
@app.put("/api/contacts/{contact_id}", response_model=Contact)
def update_contact_api(
    contact_id: int,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(None),
    category: str = Form(...),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # 处理新头像（逻辑同添加联系人）
    avatar_url = None
    if avatar:
        filename = f"{phone}_{avatar.filename}"
        file_save_path = os.path.join(AVATAR_PATH, filename)
        with open(file_save_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        avatar_url = f"/static/avatars/{filename}"
    
    contact_data = ContactCreate(
        name=name, phone=phone, email=email, category=category, avatar=avatar_url
    )
    return update_contact(db=db, contact_id=contact_id, contact=contact_data)

# 5.6 删除联系人
@app.delete("/api/contacts/{contact_id}")
def delete_contact_api(contact_id: int, db: Session = Depends(get_db)):
    return delete_contact(db=db, contact_id=contact_id)

# 6. 启动服务（仅在直接运行 main.py 时执行）
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

