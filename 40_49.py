# chapter5

# 40.係り受け解析結果の読み込み（形態素）
class Morph():
    def __init__(self,surface,base,pos,pos1):
        self.surface=surface
        self.base=base
        self.pos=pos
        self.pos1=pos1
    
    def introduce(self):
        return "{}\t{}\t{}\t{}".format(self.surface,self.base,self.pos,self.pos1)

def make_sent_list(filename):
    sentences=[]
    with open(filename,"r")as input_file:
        tmp_sent=[]
        for line in input_file:
            col_list=line.split()
            if(col_list[0]=="*" or col_list[0]=="EOS"):
                continue
            else:
                col_list=col_list[0].split(",")+col_list[1].split(",")
                morph=Morph(surface=col_list[0],base=col_list[7],pos=col_list[1],pos1=col_list[2])
                tmp_sent.append(morph)
                if morph.pos1=="句点":
                    sentences.append(tmp_sent)
                    tmp_sent=[]
        return sentences

print("A40:")
A40_result=make_sent_list("./neko.txt.cabocha")
#for s in A40_result[2]:
#    print(s.introduce())

# 41.係り受け解析結果の読み込み（文節・係り受け）
class Chunk():
    def __init__(self,morphs=[],dst=-1,srcs=[]):
        self.morphs=morphs
        self.dst=dst
        self.srcs=srcs

def make_chunk(filename):
    sentences=[]
    tmp_sent=[]
    with open(filename,"r")as input_file:
        for line in input_file:
            if line=="EOS\n":
                for idx,c in enumerate(tmp_sent[:-1]):
                    if c.dst!=-1:
                        tmp_sent[c.dst].srcs.append(idx)
                sentences.append(tmp_sent)
                tmp_sent=[]
            elif line[0]=="*":
                chunk=Chunk()
                chunk.dst=int(line.split()[2].strip("D"))
                tmp_sent.append(chunk)
            else:
                tmp=line[:-1].split("\t")
                surface=tmp[0]
                other=tmp[1]
                others=other.split(",")
                base,pos,pos1=others[6],others[0],others[1]
                morph=Morph(surface,base,pos,pos1)
                tmp_sent[-1].morphs.append(morph)
    return sentences

print("A41:")
A41_result=make_chunk("./neko.txt.cabocha")

# 42.係り元と係り先の文節の表示
print("A42:")
pairs=[]
for sent in A41_result:
    pair=[]
    for chunk in sent:
        if chunk.dst!=-1:
            pair.append((chunk,sent[chunk.dst]))
    pairs.append(pair)

'''
for sent in pairs:
    for p in sent:
        print("\t".join([str(chunk) for chunk in p]))
'''

# 43.名詞を含む文節が動詞を含む文節に係るものを抽出

print("A43:")

def NVcheck(pair):
    return "名詞" in [morph.pos for morph in pair[0].morphs] and "動詞" in [morph.pos for morph in pair[1].morphs]

'''
NVpairs=[]
for sent in pairs:
    for chunk_pair in sent:
        if NVcheck(chunk_pair):
            NVpairs.append(chunk_pair)


for NVpair in NVpairs:
    noun,verb=NVpair
    print("{}\t{}".format(noun,verb))
'''

# 44.係り受け木の可視化
print("A44:")

def sent2DOT(index,sent):
    head="digraph sentence{0}".format(index)
    body_head="{ graph [rankdir=LR];"
    body=""
    for chunk_pair in sent:
        start,end=chunk_pair
        body+='"'+str(start)+"->"+str(end)+'";'
    return head+body_head+body+"}"

'''
for i,sent in enumerate(pairs):
    print(sent2DOT(i,sent))
'''

# 45.動詞の格パターンの抽出
print("A45:")

def extractPattern(sent):
    result=[]
    for chunk in sent:
        if "動詞" in [morph.surface for morph in chunk.morphs if morph.pos!="記号"]:
            src_chunks = [sent[src] for src in chunk.srcs]
            src_chunks_case=list(filter(lambda src_chunks: [morph for morph in src_chunks.morphs if morph.pos1=="格助詞"],src_chunks))
            if src_chunks_case:
                result.append((chunk,src_chunks_case))
    return result

'''
Patterns=[]
for sent in A41_result:
    Patterns.append(extractPattern(sent))

for vp in Patterns:
    for verb,src_chunks in vp:
        v=[morph for morph in verb.morphs if morph.pos=="動詞"][-1].base
        ps=[[morph for morph in src_chunk.morphs if morph.pos1=="格助詞"][-1].base for src_chunk in src_chunks]
        p="".join(sorted(ps))
        print("{}\t{}".format(v,p))
'''

# 46.動詞の格フレーム情報の抽出
print("A46:")
'''
for vp in Patterns:
    for verb,src_chunks in vp:
        col1=[morph for morph in verb.morphs if morph.pos=="動詞"][-1].base
        tmp_ps=[[morph for morph in src_chunk.morphs if morph.pos1=="格助詞"][-1].base for src_chunk in src_chunks]
        tmp_p=sorted(tmp_ps,key=lambda x:x[0])
        col2="".join([col[0] for col in tmp_p])
        col3="".join([col[1] for col in tmp_p])
        print("{}\t{}\t{}".format(col1,col2,col3))
'''

# 47.機能動詞構文のマイニング
print("A47:")
def extractSahen(src_chunks):
    for idx,src_chunk in enumerate(src_chunks):
        morphs=src_chunk.morphs
        if len(morphs)>1:
            if morphs[-2].pos1=="サ変接続" and morphs[-1].pos=="助詞" and morphs[-1].base=="を":
                src_chunks.pop(1)
                return src_chunk,src_chunks

'''
Patterns=[]
for sent in A41_result:
    Patterns.append(extractPattern(sent))
for vp in Patterns:
    for verb,src_chunks in vp:
        sahen_set=extractSahen(src_chunks)
        if sahen_set:
            col1=[morph for morph in verb.morphs if morph.pos=="動詞"][-1].base
            tmp_ps=[[morph for morph in src_chunk.morphs if morph.pos1=="格助詞"][-1].base for src_chunk in src_chunks]
            tmp_p=sorted(tmp_ps,key=lambda x:x[0])
            col2="".join([col[0] for col in tmp_p])
            col3="".join([col[1] for col in tmp_p])
            print("{}\t{}\t{}".format(col1,col2,col3))
'''

# 48.名詞から根へのパスの抽出
print("A48:")

def extractPath(chunk,sentence):
    path=[chunk]
    dst=chunk.dst
    while dst!=-1:
        path.append(sentence[dst])
        dst=sentence[dst].dst
    return path

'''
paths=[]
for sent in A41_result:
    for chunk in sent:
        if "名詞" in [morph.pos for morph in chunk.morphs] and chunk.dst!=-1:
            paths.append(extractPath(chunk,sent))
for path in paths:
    print(" -> ".join([str(chunk) for chunk in path]))
'''

# 49.名詞間の係り受けパスの抽出
print("A49:")

from collections import namedtuple
from itertools import combinations

def extractPathIndex(i_chunk, sentence):
    i, chunk = i_chunk
    path_index = [i]
    dst = chunk.dst
    while dst != -1:
        path_index.append(dst)
        dst = sentence[dst].dst
    return path_index

def posReplace(chunks, pos, repl, k=1):
    replaced_str = ""
    for morph in chunks[0].morphs:
        if morph.pos == pos and k > 0:
            replaced_str += repl
            k -= 1
        else:
            if morph.pos != '記号':
                replaced_str += morph.surface
    return [replaced_str] + [str(chunk) for chunk in chunks[1:]]

paths=[]
N2Npath=namedtuple("N2Npath",["X","Y","is_linear"])

for sent in A41_result:
    noun_chunks = [(i, chunk) for i, chunk in enumerate(sentence) if chunk.include_pos('名詞')]
        if len(noun_chunks) > 1:
            for former, latter in combinations(noun_chunks, 2):
                f_index = extractPathIndex(former, sentence)
                l_index = extractPathIndex(latter, sentence)
                f_i, l_i = list(zip(reversed(f_index), reversed(l_index)))[-1]
                linear_flag = (f_i == l_i)
                if linear_flag:
                    f_index2 = f_index[:f_index.index(f_i)+1]
                    l_index2 = l_index[:l_index.index(l_i)+1]
                else:
                    f_index2 = f_index[:f_index.index(f_i)+2]
                    l_index2 = l_index[:l_index.index(l_i)+2]
                X = [sentence[k] for k in f_index2]
                Y = [sentence[k] for k in l_index2]
                paths.append(N2Npath(X=X, Y=Y, is_linear=linear_flag))

for path in paths:
    x=posReplace(path.X,"名詞","X")
    y=posReplace(path.Y,"名詞","Y")
    if path.is_linear:
        X[-1]="Y"
        print(" -> ".join(x))
    else:
        print("{} | {} | {}".format(" -> ".join(x[:-1])," -> ".join(y[:-1]),path.X[-1]))
