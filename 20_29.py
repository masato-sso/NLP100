# chapter3

# 20.JSONデータの読み込み
import json

print("A20:")
with open("jawiki-country.json") as f:
    articles=f.readlines()
    for con in articles:
        a_dic=json.loads(con)
        if a_dic["title"]=="イギリス":
            texts=a_dic["text"]
            print(texts)

# 21.カテゴリ名を含む行を抽出
categories=[]
print("A21:")
for c in texts.split("\n"):
    if "Category" in c:
        categories.append(c)
print(categories)

# 22.カテゴリ名の抽出
import re

categories2=[]
print("A22:")
for c in texts.split("\n"):
    c_obj=re.search("^\[\[Category:(.*?)(|\|.*)\]\]$",c)
    if not(c_obj ==None):
        categories2.append(c_obj.group(1))
print(categories2)

# 23.セクション構造
print("A23:")
for sec in texts.split("\n"):
    sec_obj=re.search("^(=+)\s*(.*?)\s*(=+)$",sec)
    if not(sec_obj ==None):
        print(sec_obj.group(2),len(sec_obj.group(1))-1)

# 24.ファイル参照の抽出
print("A24:")
for f in texts.split("\n"):
    f_obj=re.search("(File|ファイル):(.*?)\|",f)
    if not(f_obj ==None):
        print(f_obj.group(2))

# 25.テンプレートの抽出
print("A25:")

template_dict={}
temps=re.split("\n[\|}]",texts)

for t in temps:
    t_obj=re.search("^(.*?)\s=\s(.*)",t,re.S)
    if not(t_obj ==None):
        template_dict[t_obj.group(1)]=t_obj.group(2)
print(template_dict)


# 26.強調マークアップの除去
print("A26:")

template_dict2={}
temps=re.split("\n[\|}]",texts)

for t in temps:
    t_obj=re.search("^(.*?)\s=\s(.*)",t,re.S)
    if not(t_obj ==None):
        template_dict2[t_obj.group(1)]=re.sub("'{2,5}","",t_obj.group(2))
print(template_dict2)


# 27.内部リンクの除去
print("A27:")

template_dict3={}
temps=re.split("\n[\|}]",texts)

for t in temps:
    t_obj=re.search("^(.*?)\s=\s(.*)",t,re.S)
    if not(t_obj ==None):
        template_dict3[t_obj.group(1)]=re.sub("\[{2}([^|\]]+?\|)*(.+?)\]{2}","\2",(re.sub("'{2,5}","",t_obj.group(2))))
print(template_dict3)

# 28.MediaWikiマークアップの除去
print("A28:")

template_dict4={}
temps=re.split("\n[\|}]",texts)

for t in temps:
    t_obj=re.search("^(.*?)\s=\s(.*)",t,re.S)
    if not(t_obj ==None):
        value=re.sub("\[{2}([^|\]]+?\|)*(.+?)\]{2}","\2",(re.sub("'{2,5}","",t_obj.group(2))))
        value=re.sub("\{{2}.+?\|.+?\|(.+?)\}{2}","\1",value)
        value=re.sub("\[.*?\]","",re.sub("<.*?>","",value))
        template_dict4[t_obj.group(1)]=value
print(template_dict4)

# 29.国旗画像のURLを取得する
import requests

# template_dict4を使用
url_base = 'https://commons.wikimedia.org/w/api.php?'
url_prefix = 'action=query&titles=File:'
url_file = template_dict4['国旗画像'].replace(' ', '_')
url_suffix = '&prop=imageinfo&iiprop=url&format=json'
url = url_base + url_prefix + url_file + url_suffix

data = requests.get(url)
result=re.search(r'"url":"(.+?)"', data.text).group(1)

print("A29:{}".format(result))
