import re, collections
import urllib2
import os

# change work directory
# os.chdir('C:\\Users\\lenovo\\Desktop')
# print os.getcwd()

def download(url):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate, sdch',
               'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
               'Connection':'keep-alive',
               'Host':'www.norvig.com',
               'Upgrade-Insecure-Requests':'1',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    req = urllib2.Request(url = url, headers = headers)
    filename = re.findall('[^\/]+$', url)[0]
    netfile = urllib2.urlopen(req).read()
    fhand = open(filename, 'w')
    fhand.write(netfile)
    fhand.close()

# download("http://norvig.com/big.txt")

# Extract the individual words from the file
def words(text): return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    # model = {}
    # for f in features:
    #     model[f] = model.get(f, 1) + 1
    return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

print correct('speling')