import os
from pymongo import MongoClient
import requests
from config import *
import time

auth_url = os.getenv("MONGODB_URI")
cluster = MongoClient(auth_url)
db = cluster["Economy"]
cursor = db["Mine"]

async def open_mine(user):
    try:
        post = {"_id": user.id, "N工人": 0, "R工人": 0,  "SR工人":0, "SSR工人":0, "UR工人":0, "鎬子":1, "礦車":0,"中間商":False,"累積礦物":1,"提煉所":0}

        cursor.insert_one(post)

    except:
        pass

async def set_miner(user, amont=0, mode="N工人"):
    cursor.update_one({"_id": user.id}, {"$set": {str(mode): amont}})

async def update_miner(user, amont=0, mode= "工人"):
    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amont}})

async def get_mine_data(user):
    user_data = cursor.find({"_id": user.id})

    cols = []
    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data