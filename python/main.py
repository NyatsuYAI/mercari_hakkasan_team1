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

import function

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


def get_timestamp():
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        logger.info(f"table not exists")
        with open("../db/item.db") as schema_file:
            schema = schema_file.read()
            logger.debug("Read schema file.")
        cur.executescript(f"""{schema}""")
        conn.commit()
    cur.execute("""SELECT datetime('now', '+9 hours')""")
    timestamp = cur.fetchone()
    conn.commit()
    conn.close()
    return timestamp


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


@app.get("/")
def root():
    return {"message": "Hello, world!"}


def get_post(user_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        logger.info(f"table not exists")
        with open("../db/item.db") as schema_file:
            schema = schema_file.read()
            logger.debug("Read schema file.")
        cur.executescript(f"""{schema}""")
        conn.commit()
    user_id = get_user(user_name)
    cur.execute("""select following_id from follows where user_id = (?)""", user_id)
    follows = cur.fetchall()
    conn.commit()
    conn.close()
    logger.info("Get follows")
    return follows


@app.get("/items")
def get_user_id(user_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        logger.info(f"table not exists")
        with open("../db/item.db") as schema_file:
            schema = schema_file.read()
            logger.debug("Read schema file.")
        cur.executescript(f"""{schema}""")
        conn.commit()
    user_id = get_user(user_name)
    cur.execute("""select * from items where user_id = (?)""", user_id)
    items = cur.fetchall()
    conn.commit()
    conn.close()
    logger.info("Get items")
    return items


@app.get("/user")
def get_userid_from_name(user_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        with open("../db/item.db") as schema_file:
            schema = schema_file.read()
        cur.executescript(f"""{schema}""")
        conn.commit()
    cur.execute("""select user_id from users where name = (?)""", (user_name,))
    user_id = cur.fetchone()
    conn.commit()
    conn.close()
    return user_id


@app.post("/user")
def add_user(user_name: str = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        logger.info(f"table not exists")
        with open("../db/item.db") as schema_file:
            schema = schema_file.read()
            logger.debug("Read schema file.")
        cur.executescript(f"""{schema}""")
        conn.commit()
    cur.execute("""insert or ignore into users(name) values (?)""", (user_name,))
    logger.info(f"insert user: {user_name}")
    cur.execute("""select * from users""")
    user = cur.fetchall()
    conn.commit()
    conn.close()
    logger.info(f"Post user: {user}")


@app.post("/follows")
def add_user(user_name: int = Form(...), following_name: int = Form(...)):
    conn = sqlite3.connect(data_base_name)
    cur = conn.cursor()
    if cur.fetchone() == None:
        logger.info(f"table not exists")
        with open("../db/item.db") as schema_file:
            schema = schema_file.read()
            logger.debug("Read schema file.")
        cur.executescript(f"""{schema}""")
        conn.commit()
    user_id = get_user(user_name)
    following_id = get_user(following_name)
    cur.execute(
        """select * from follows where user_id = (?) and following_id = (?)""",
        user_id,
        following_id,
    )
    follows = cur.fetchone()
    conn.commit()
    conn.close()
    logger.info(f"Post follows : {follows}")


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
        logger.info(f"table not exists")
        with open("../db/item.db") as schema_file:
            schema = schema_file.read()
            logger.debug("Read schema file.")
        cur.executescript(f"""{schema}""")
        conn.commit()
    user_id = get_user(user_name)
    timestamp = get_timestamp()
    cur.execute(
        """insert into items(name,user_id,category,info,timestamp,image) values (?,?,?,?,?,?)""",
        (item_name, user_id, category, info, timestamp, image),
    )
    cur.execute("""select timestamp from items where timestamp = (?)""", timestamp)
    item = cur.fetchone()
    conn.commit()
    conn.close()
    logger.info(f"Post item: {item}")


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
