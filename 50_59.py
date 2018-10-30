# chapter6

# 50.文区切り
import re

print("A50:")
pt=re.compile("(?P<punt>[\.:;!\?]) (?P<head>[A-Z])")

A50_result=[]
with open("./nlp.txt","r")as read_file:
    for line in read_file:
        txt=line.strip()
        A50_result.append(pt.sub(r"\g<punt>\n\g<head>",txt))

# 51.単語の切り出し
print("A51:")
A51_result=[]
for line in A50_result:
    txt=line.strip()
    for word in txt.split():
        A51_result.append(re.sub(r"\W","",word))

# 52.ステミング
from nltk.stem.porter import PorterStemmer

print("A52:")
for line in A51_result:
    stemmer=PorterStemmer()
    txt=line.strip()
    if len(txt)>0:
        print("{}\t{}".format(txt,stemmer.stem(txt)))
    else:
        print()

# 53.Tokenization
print("A53:")
token_pt=re.compile(r"<word>(\w+)</word>")

with open("nlp.txt.xml","r")as read_file:
    for line in read_file:
        word=token_pt.search(line.strip())
        if word:
            print(word.group(1))

# 54.品詞タグ付け
print("A54:")
W=re.compile(r"<word>(\w+)</word>")
L=re.compile(r"<lemma>(\w+)</lemma>")
P=re.compile(r"<POS>(\w+)</POS>")

tmp_word=[]
with open("./nlp.txt.xml","r")as read_file:
    for line in read_file:
        if len(tmp_word)==3:
            print("\t".join(tmp_word))
            tmp_word=[]
        else:
            line=line.strip()
            word=W.search(line)
            if len(tmp_word)==0 and word:
                tmp_word.append(word.group(1))
                continue
            lemma=L.search(line)
            if len(tmp_word)==1 and lemma:
                tmp_word.append(lemma.group(1))
                continue
            pos=P.search(line)
            if len(tmp_word)==2 and pos:
                tmp_word.append(pos.group(1))

# 55.固有表現抽出
print("A55:")
W=re.compile(r"<word>(\w+)</word>")
N=re.compile(r"<NER>(\w+)</NER>")

with open("nlp.txt.xml","r")as read_file:
    for line in read_file:
        word=W.search(line.strip())
        if word:
            token=word.group(1)
            continue
        ner=N.search(line.strip())
        if ner:
            if ner.group(1)=="PERSON":
                print(token)

# 56.共参照解析
import xml.etree.ElementTree as et
from functools import partial

print("A56:")
LRB = re.compile(r"-LRB- ")
RRB = re.compile(r" -RRB-")
NOTATION = re.compile(r" ([,\.:;])")
LDQ = re.compile(r"`` ")
RDQ = re.compile(r" \'\'")
SQ = re.compile(r" \'")
SQS = re.compile(r" \'s")

class StanfordDocument():
    def __init__(self, file):
        self.xmltree = et.parse(file)
        root = self.xmltree.getroot()
        self.sentences = root.find('document/sentences')
        self.coreferences = root.find('document/coreference')

    def getListOfSentences(self):
        sentences = []
        for sentence in self.sentences.findall('sentence'):
            sentences.append([word.text for word in sentence.findall('tokens/token/word')])
        return sentences

def analysis(file):
    doc = StanfordDocument(file)
    sentences = doc.getListOfSentences()

    for coref in doc.coreferences.findall('coreference'):
        mentions = coref.findall('mention')
        represent = coref.find('mention[@representative="true"]')
        for mention in mentions:
            if mention != represent:
                sentence_i = int(mention.find('sentence').text) - 1
                start_i = int(mention.find('start').text) - 1
                end_i = int(mention.find('end').text) - 2

                target_sentence = sentences[sentence_i]
                target_sentence[start_i] = represent.find('text').text.strip() + ' (' + target_sentence[start_i]
                # print list(represent)
                # target_sentence[start_i] = "[" + str(sentence_i) +","+ str(start_i) +","+ str(end_i) +","+str(sentences[sentence_i][start_i])+ "]" + ' (' + target_sentence[start_i]
                target_sentence[end_i] = target_sentence[end_i] + ')'
    return sentences

def prettifySentence(sentence):
    s = " ".join(sentence)
    partials = map(
        lambda x: partial(x[0], x[1]),
        [
            (LRB.sub, '('),
            (RRB.sub, ')'),
            (LDQ.sub, '\"'),
            (RDQ.sub, '\"'),
            (SQS.sub, "\'s"),
            (SQ.sub, "\'"),
            (NOTATION.sub, r'\1')
        ]
    )
    for part in partials:
        s = part(s)
    return s

sents=analysis("./nlp.txt.xml")
for sent in sents:
    print(prettifySentence(sent))

# 57.係り受け解析
print("A57:")

def dependToDot(i, dependency):
    header = "digraph sentence{0} ".format(i)
    body_head = "{ graph [rankdir = LR]; "
    body = ""
    for dep in dependency:
        governor, dependent, label = dep.find('governor').text, dep.find('dependent').text, dep.get('type')
        body += '"{gov}"->"{dep}" [label = "{label}"]; '.format(gov=governor, dep=dependent, label=label)

    dotString = header + body_head + body + "}"
    return dotString

def read_xml(file):
    doc = StanfordDocument(file)
    sentences = doc.sentences.findall('sentence')
    dotSentences = []
    for i, sentence in enumerate(sentences):
        dependency = sentence.find("dependencies[@type='collapsed-dependencies']")
        dotSentences.append(dependToDot(i+1, dependency))
    return dotSentences

for dot_sent in read_xml("./nlp.txt.xml"):
    print(dot_sent)

# 58.タプルの抽出
print("A58:")

def extractTuples(sentence):
    dependencies = sentence.find("dependencies[@type='collapsed-dependencies']")
    dep_triple = []
    dep_dic = {}

    for dep in dependencies:
        gov = (dep.find('governor').get('idx'), dep.find('governor').text)
        if dep.get('type') in ['nsubj', 'dobj']:
            dep_dic.setdefault(gov, []).append((dep.get('type'), dep.find('dependent').text))

    verbs = [key for key, value in dep_dic.items() if set([t for (t, d) in value]) == set(['nsubj', 'dobj'])]

    for verb in verbs:
        nsubj = [d for (t, d) in dep_dic[verb] if t == 'nsubj']
        dobj = [d for (t, d) in dep_dic[verb] if t == 'dobj']
        dep_triple += [[verb[1], n, d] for n in nsubj for d in dobj]

    return dep_triple

doc=StanfordDocument("./nlp.txt.xml")
sents=doc.sentences.findall("sentence")
dep_triple=[]

for sent in sents:
    dep_triple.append(extractTuples(sent))

for dep in dep_triple:
    for d in dep:
        print("{}\t{}\t{}".format(d[1],d[0],d[2]))

# 59.S式の解析
print("A59:")

class TreeParser():
    def __init__(self):
        self.root = None
        self._stack = [[]]

    def parse(self, tree_string):
        read = []
        for character in tree_string.strip():
            if character == "(":
                self._stack.append([])
            elif character == " ":
                if read:
                    self._stack[-1].append("".join(read))
                    read = []
            elif character == ")":
                if read:
                    self._stack[-1].append("".join(read))
                    read = []
                self._stack[-2].append(self._stack.pop())
            else:
                read.append(character)
        self.root = self._stack.pop()

    def get_phrase(self, tag):
        s = self.root[0][1]
        return self._recursive_finder(s, tag)

    def _recursive_finder(self, lst, tag):
        res = []
        if lst[0] == tag:
            res.append(lst)
        for l in lst[1:]:
            if isinstance(l, list):
                res.extend(self._recursive_finder(l, tag))
        return res

def str_phrase(phrase):
    res = []
    for p in phrase:
        if isinstance(p, list):
            if isinstance(p[1], list):
                res += str_phrase(p)
            else:
                res.append(p[1])
    return res

doc=StanfordDocument("./nlp.txt.xml")
sents=doc.sentences.findall("sentence")
tag_phases=[]

for sent in sents:
    parser=TreeParser()
    parser.parse(sent.find("parse").text)
    tag_phases.append(parser.get_phrase("NP"))

for tag_phase in tag_phases:
    for tag in tag_phase:
        print(prettifySentence(str_phrase(tag)))