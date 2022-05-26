from asyncore import file_dispatcher
from calendar import c
from multiprocessing import allow_connection_pickling
import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import json
from pathlib import Path
import sqlite3
import hashlib
import datetime

data_base_name = "../db/mercari.sqlite3"

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


def get_now_timestamp():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))  # 日本時刻
    string_now = now.strftime("%Y%m%d%H%M%S")
    return string_now

@app.on_event("startup")
def init_database():
    try:
        conn = sqlite3.connect(data_base_name)
        cur = conn.cursor()
        with open("../db/item.db") as schema_file:
            schema = schema_file.read()
            logger.debug("Read schema file.")
        cur.executescript(f"""{schema}""")
        conn.commit()
        logger.info("Completed database initialization.")
    except Exception as e:
        logger.warn(f"Failed to initialize database. Error message: {e}")
        exit()


@app.get("/")
def root():
    return {"message": "Hello, world!"}


@app.get("/user")
def get_userid_from_name(user_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    try:
        cur.execute("""select user_id from users where user_name = (?)""", (user_name,))
        user_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return user_id
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "account don't exsist"



@app.post("/user")
def add_user(user_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        init_database()
    try:
        cur.execute("""insert or ignore into users(user_name) values (?)""", (user_name,))
        logger.info(f"insert user: {user_name}")
        cur.execute("""select * from users""")
        user = cur.fetchall()
        conn.commit()
        conn.close()
        logger.info(f"register account: {user}")
        return "account is published"
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "failed making account"


@app.get("/follows")
def get_follows_from_name(user_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    try:
        cur.execute("""select user_id from users where user_name = (?)""", (user_name,))
        user_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "Please register account"
    
    cur.execute("""select * from follows where user_id = (?)""", (user_id,))
    following = cur.fetchall()
    follows_list=[]
    for i in range(len(following)):
        cur.execute("""select user_name from users where user_id = (?)""", (following[i][2],))
        name=[following[i][2], cur.fetchone()[0]]
        follows_list.append(name)
    conn.commit()
    conn.close()
    return follows_list


@app.post("/follows")
def add_following(user_name: str = Form(...), following_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        init_database()

    try:
        cur.execute("""select user_id from users where user_name = (?)""", (user_name,))
        user_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "Please register account"

    try:
        cur.execute("""select user_id from users where user_name = (?)""", (following_name,))
        following_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "Account dont't exist"

    cur.execute(
        """insert or ignore into follows(user_id,following_id) values (?,?)""",(user_id, following_id))
    cur.execute("""select * from follows where user_id = (?)""", (user_id,))
    follows = cur.fetchall()
    conn.commit()
    conn.close()
    logger.info(f"Post follows : {follows}")

@app.get("/items")
def get_all_item_from_user_id(user_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        init_database()
    try:
        cur.execute("""select user_id from users where user_name = (?)""", (user_name,))
        user_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "account don't exsist"

    try:
        cur.execute("""select * from items where user_id = (?) order by timestamp asc""", (user_id,))
        items = cur.fetchall()
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "failed post items"
    conn.commit()
    logger.info(f"get items: {items}")
    conn.close()
    return items
    



@app.post("/items")
def add_user_item(
    user_name: str = Form(...),
    item_name: str = Form(...),
    category: str = Form(...),
    info: str = Form(...),
    image: str = Form(...),
):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        init_database()

    try:
        cur.execute("""select user_id from users where user_name = (?)""", (user_name,))
        user_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "account don't exsist"
    
    timestamp = get_now_timestamp()
    hashed_filename = (
        hashlib.sha256(image.replace(".jpg", "").encode("utf-8")).hexdigest() + ".jpg"
    )
    try:
        cur.execute(
            """insert into items(user_name,user_id,item_name,category,info,timestamp,image) values (?,?,?,?,?,?,?)""",
            (user_name, user_id, item_name,category, info, timestamp, hashed_filename),
        )
        cur.execute("""select * from items where timestamp = (?) and user_id = (?)""", (timestamp,user_id))
        item = cur.fetchall()
        conn.commit()
        conn.close()
        logger.info(f"Post item: {item}")
        return "post successfully"

    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "failed post items"


@app.get("/image/{image_filename}")
async def get_image(image_filename):
    # Create image path
    image = image / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)

# @app.post("/items")
# def add_item(name: str = Form(...), category: str = Form(...), image: str = Form(...)):
#     conn = sqlite3.connect(data_base_name)
#     cur = conn.cursor()
#     if cur.fetchone() == None:
#         logger.info(f"table not exists")
#         with open("../db/item.db") as schema_file:
#             schema = schema_file.read()
#             logger.debug("Read schema file.")
#         cur.executescript(f"""{schema}""")
#     conn.commit()
#     cur.execute("""insert or ignore into category(name) values (?)""", (category,))
#     cur.execute("""select id from category where name = (?)""", (category,))

#     category_id = cur.fetchone()[0]
#     logger.info(f"Receive item: {category_id}")
#     hashed_filename = (
#         hashlib.sha256(image.replace(".jpg", "").encode("utf-8")).hexdigest() + ".jpg"
#     )
#     cur.execute(
#         """insert into items(name, category_id, image) values(?, ?, ?)""",
#         (name, category_id, hashed_filename),
#     )
#     conn.commit()
#     cur.close()
#     conn.close()
#     logger.info(f"Receive item: {name,category,hashed_filename}")


# @app.get("/items")
# def get_items():
#     conn = sqlite3.connect(data_base_name)
#     cur = conn.cursor()
#     cur.execute("""select * from items""")
#     items = cur.fetchall()
#     cur.execute("""select * from category""")
#     categorys = cur.fetchall()
#     conn.commit()
#     conn.close()
#     logger.info("Get items")
#     return items, categorys


@app.delete("/items")
def init_item():
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    cur.execute("""drop table items;""")
    cur.execute("""drop table category;""")
    conn.commit()
    cur.close()
    conn.close()


@app.get("/search")
def search_item(keyword: str):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    cur.execute(
        """select items.name,category.name as category,items.image from items inner join category on category.id = items.category_id where items.name like (?)""",
        (f"%{keyword}%",),
    )
    items = cur.fetchall()
    conn.close()
    logger.info(f"Get items with name containing {keyword}")
    return items
