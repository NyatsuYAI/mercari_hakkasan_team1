# from asyncore import file_dispatcher
# from calendar import c
# from multiprocessing import allow_connection_pickling
import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, Depends
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


@app.get("/user/{user_name}")
def get_userid_from_name(user_name):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    try:
        cur.execute("""select * from users where name = (?)""", (user_name,))
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
        cur.execute("""insert or ignore into users(name) values (?)""", (user_name,))
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
def get_follows():
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    try:
        cur.execute("""select * from follows""")
        follows = cur.fetchall()
        return follows
    except AssertionError as e:
        logger.info(f"ERR: {e}")


@app.get("/follows/{user_name}")
def get_follows_from_name(user_name):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    try:
        cur.execute("""select * from users where name = (?)""", (user_name,))
        user_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "Please register account"

    cur.execute("""select * from follows where user_id = (?)""", (user_id,))
    following = cur.fetchall()
    print(following)
    follows_list = []
    for i in range(len(following)):
        cur.execute("""select * from users where id = (?)""", (following[i][2],))
        name = cur.fetchone()
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
        cur.execute("""select * from users where name = (?)""", (user_name,))
        user_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "Please register account"

    try:
        cur.execute("""select * from users where name = (?)""", (following_name,))
        following_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "Account dont't exist"

    cur.execute(
        """insert or ignore into follows(user_id,following_id) values (?,?)""",
        (user_id, following_id),
    )
    cur.execute("""select * from follows where user_id = (?)""", (user_id,))
    follows = cur.fetchall()
    conn.commit()
    conn.close()
    logger.info(f"Post follows : {follows}")
    return "Post follows"


@app.get("/items/{user_name}")
def get_all_item_from_user_id(user_name):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        init_database()
    try:
        cur.execute("""select * from users where name = (?)""", (user_name,))
        user_id = cur.fetchone()[0]
    except AssertionError as e:
        logger.info(f"ERR: {e}")
        return "account don't exsist"

    try:
        cur.execute(
            """select * from items where user_id = (?) order by timestamp asc""",
            (user_id,),
        )
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
    timestamp: str = Depends(get_now_timestamp),
):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        init_database()

    try:
        cur.execute("""select * from users where name = (?)""", (user_name,))
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
            """insert into items(user_id,name,category,info,timestamp,image) values (?,?,?,?,?,?)""",
            (user_id, item_name, category, info, timestamp, hashed_filename),
        )
        cur.execute(
            """select * from items where timestamp = (?) and user_id = (?)""",
            (timestamp, user_id),
        )
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


@app.delete("/items")
def init_item():
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    cur.execute("""drop table items;""")
    conn.commit()
    cur.close()
    conn.close()
    return "deleted users table "


@app.delete("/users")
def init_user():
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    cur.execute("""drop table users;""")
    conn.commit()
    cur.close()
    conn.close()
    return " deleted users table"


@app.delete("/follows")
def init_follows():
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    cur.execute("""drop table follows;""")
    conn.commit()
    cur.close()
    conn.close()
    return " deleted users table"


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
