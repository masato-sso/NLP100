# chapter7

# 60.KVSの構築

# using LevelDB
import gzip
import json
#import leveldb

print("A60:")

filename="artist.json.gz"
DB_NAME="KVS_Test_DB"

'''
db=leveldb.LevelDB(DB_NAME)
with gzip.open(filename,"rt")as data:
    for line in data:
        data_json=json.loads(line)
        key=data_json["name"]+"\t"+str(data_json["id"])
        value=data_json.get("area","")
        db.Put(key.encode(),value.encode())
'''

# 61.KVSの検索
import re

print("A61:")
'''
pt=re.compile(r"^(.*)\t(\d+)$",re.VERBOSE+re.DOTALL)

db=leveldb.LevelDB(DB_NAME)

artist_name=input("artist_name:")

for key,value in db.RangeIter(key_from=(artist_name+"\t").encode()):
    match=pt.match(key.decode())
    name=match.group(1)
    id=match.group(2)
    if name!=artist_name:
        break
    area=value.decode()
    if area!="":
        print("{}(id:{})の活動場所は{}です。".format(artist_name,id,area))
    else:
        print("Not Found")
'''

# 62.KVS内の反復処理
print("A62:")
'''
db=leveldb.LevelDB(DB_NAME)

AREA="Japan".encode()
hit_counts=0
for value in db.RangeIter():
    if value[1]==AREA:
        hit_counts+=1
print("{}件ヒット".format(hit_counts))
'''

# 63.オブジェクトを値に格納したKVS
print("A63:")
'''
DB_NAME2="KVS2_Test_DB"

db=leveldb.LevelDB(DB_NAME2)

pt=re.compile(r"^(.*)\t(\d+)$",re.VERBOSE+re.DOTALL)

with gzip.open(filename, 'rt') as data_file:
    for line in data_file:
        data_json = json.loads(line)
        key = data_json['name'] + '\t' + str(data_json['id'])
        value = data_json.get('tags')
        if value is None:
            value = []
        db.Put(key.encode(), json.dumps(value).encode())

artist_name=input("artist name:")

for key,value in db.RangeIter(key_from=(artist_name+"\t").encode()):
    match=pt.match(key.decode())
    name=match.group(1)
    id=match.group(2)
    if name!=artist_name:
        break
    tags=json.loads(value.decode())
    print("{}({})".format(name,id))
    if len(tags)>0:
        for tag in tags:
            print("[{}]:{}".format(tag["count"],tag["value"]))
    else:
        print("Not Found")
'''

# 64.MongoDBの構築
import pymongo
from pymongo import MongoClient

print("A64:")
'''
client=MongoClient()
db=client["Artist_DB"]
collection=db["artist"]

with gzip.open(filename,"rt")as data:
    for line in data:
        collection.insert_one(json.loads(line))
    print("構築完了")

collection.create_index([("name",pymongo.ASCENDING)])
collection.create_index([("aliases.name",pymongo.ASCENDING)])
collection.create_index([("tags.value",pymongo.ASCENDING)])
collection.create_index([("rating.value",pymongo.ASCENDING)])
'''

# 65.MongoDBの検索
print("A65:")
print("> db.artist.find({name: 'Queen'})")
'''
client=MongoClient()
db=client["Artist_DB"]
collection=db["artist"]

for Queen in collection.find({"name":"Queen"}):
    print(Queen)
'''

# 66.検索件数の取得
print("A66:")
print("> db.artist.find({area:'Japan'}).count()")

# 67.複数のドキュメントの取得
print("A67:")
'''
client=MongoClient()
db=client["Artist_DB"]
collection=db["artist"]

artist_name=input("artist name:")

for doc in collection.find({'aliases.name': artist_name}):
    print(doc)
'''

# 68.ソート
print("A68:")
'''
client=MongoClient()
db=client["Artist_DB"]
collection=db["artist"]

dancer=[]
for dance in collection.find({"tags.value":"dance"}):
    if "rating" in dance:
        dancer.append([dance["name"],dance["rating"]["count"]])
    top10=sorted(dancer,key=lambda x:x[1],reverse=True)

print("Ranking Top10")
n=0
for d in top10:
    if n>9:
        break
    print("{}\t{}".format(d[0],d[1]))
    n+=1
'''

# 69.Webアプリケーションの作成
from flask import Flask,render_template,request,redirect,url_for

print("A69:")

app=Flask(__name__)
client=pymongo.MongoClient()
db=client["Artist_DB"]
collection=db["artist"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/result",methods=["GET","POST"])
def post():
    title="artist"
    if request.method=="POST":
        result=[]
        name=request.form["name"]
        tag=request.form["tag"]
        order=[]
        if name:
            for artist in collection.find({"name":name}):
                if "rating" in artist:
                    result.append([artist["name"],artist["rating"]["count"]])
                order=sorted(result,key=lambda x:x[1],reverse=True)
        if tag:
            for artist in collection.find({"tags.value":tag}):
                if "rating" in artist:
                    result.append([artist["name"],artist["rating"]["count"]])
                order=sorted(result,key=lambda x:x[1],reverse=True)
        
        if len(order)==0:
            order.append("Not Found")
        return render_template("index.html",message=order)
    else:
        print("リダイレクト")
        return redirect(url_for("index"))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
