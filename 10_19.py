# chapter2

# 10.行数のカウント
with open("hightemp.txt","r") as fp:
    print("A10:{}".format(len(fp.readlines())))

# 11.タブをスペースに置換
with open("hightemp.txt","r") as fp:
    print("A11:")
    for line in fp:
        print(line.replace("\t"," "),end="")

# 12.1列目をcol1.txtに,2列目をcol2.txtに保存
with open("col1.txt","w") as col1:
    with open("col2.txt","w") as col2:
        with open("hightemp.txt","r") as fp:
            contents=fp.readlines()
        for line in contents:
            col1.write(line.split()[0]+"\n")
            col2.write(line.split()[1]+"\n")

# 13.col1.txtとcol2.txtをマージ
with open("merge.txt","w") as mf:
    with open("col1.txt","r") as col1f:
        with open("col2.txt","r") as col2f:
            col1_con=col1f.readlines()
            col2_con=col2f.readlines()
    for line1,line2 in zip(col1_con,col2_con):
        mf.write(line1.strip()+"\t"+line2)

# 14.先頭からN行を出力
print("==============")
print("A14:")
def Q14(filename,N):
    with open(filename,"r") as fp:
        cont=fp.readlines()
    for idx in range(N):
        print(cont[idx].strip())

Q14("hightemp.txt",5)

# 15.末尾のN行を出力
print("==============")
print("A15:")
def Q15(filename,N):
    with open(filename,"r") as fp:
        cont=fp.readlines()
        cont=cont[len(cont)-N::]
    for line in cont:
        print(line.strip())

Q15("hightemp.txt",5)

# 16.ファイルをN分割
def Q16(filename,N):
    with open(filename,"r") as fp:
        cont=fp.readlines()
        if len(cont)%N==0:
            for i in range(int(len(cont)/N)):
                with open("sub{}_{}".format(i,filename),"w") as fw:
                    for j in range(N):
                        fw.write(cont[int(j+(N*i))])
        else:
            print("error")

Q16("hightemp.txt",8)

# 17.1列目の文字列の異なり
with open("hightemp.txt","r") as fp:
    contents=fp.readlines()
    result=set()
    for cont in contents:
        result.add(cont.split()[0])

print("A17:{}".format(result))

# 18.各行を3コラム目の数値の降順にソート
print("A18:")
from operator import itemgetter
with open("hightemp.txt","r") as fp:
    contents=fp.readlines()
    for line in sorted(contents,key=itemgetter(3),reverse=True):
        print(line.strip())

# 19.各行の1コラム目の文字列の出現頻度を求め、出現頻度の高い順に並べる
print("A19:")
import numpy as np
with open("hightemp.txt","r") as fp:
    contents=fp.readlines()
    ranks=[]
    keys=set()
    tmp=[]
    for line in contents:
        keys.add(line.split()[0])
        tmp.append(line.split()[0])
    for k in keys:
        ranks.append(tmp.count(k))
    index=np.argsort(ranks)
    Keys=[]
    for idx in index:
        Keys.append(list(keys)[idx])
    result=dict(zip(Keys[::-1],np.sort(ranks)[::-1]))
print(result)
