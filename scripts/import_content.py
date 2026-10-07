"""One-time extraction of the supplied websites; uses only Python's standard library."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []
    def text(self):
        return re.sub(r'\s+', ' ', ''.join(c if isinstance(c, str) else (' ' if c.tag == 'br' else c.text()) for c in self.children)).strip()
    def find(self, tag=None, cls=None):
        result = []
        for c in self.children:
            if isinstance(c, Node):
                if (tag is None or c.tag == tag) and (cls is None or cls in c.attrs.get('class', '').split()):
                    result.append(c)
                result.extend(c.find(tag, cls))
        return result

class Tree(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.root = Node()
        self.stack = [self.root]
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].children.append(n)
        if tag not in {'img','br','hr','input','meta','link','source','wbr','area','embed','param','col'}:
            self.stack.append(n)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

assets = {}
def image(node):
    url = node.attrs['src']
    local = 'assets/images/' + Path(urlsplit(url).path).name
    assets[url] = local
    return local

def load(name):
    return Tree((ROOT / 'migration/sources' / (name+'.html')).read_text(encoding='utf-8')).root.find(cls='entry-content')[0]

people = []
group, photo = '', ''
for n in load('people').children:
    if not isinstance(n, Node):
        continue
    if n.tag == 'h4':
        group = n.text()
    if n.find('img'):
        photo = image(n.find('img')[0])
    if n.tag == 'p' and n.find('strong'):
        name = n.find('strong')[0].text()
        people.append({'name':name, 'role':n.text().replace(name,'',1).strip(), 'group':group, 'image':photo, 'bio':'', 'links':[]})
    elif n.tag == 'p' and n.text() and people:
        people[-1]['bio'] += (' ' if people[-1]['bio'] else '') + n.text()
        people[-1]['links'].extend({'label':a.text(), 'url':a.attrs['href']} for a in n.find('a'))

publications, group = [], ''
for n in load('publications').find():
    if not isinstance(n, Node):
        continue
    if n.tag == 'h3':
        group = n.text()
    if n.tag == 'ol':
        for li in n.find('li'):
            citation = li.text()
            years = re.findall(r'\b(?:19|20)\d{2}\b', citation)
            publications.append({'type':group, 'citation':citation, 'year':int(years[-1]) if years else None, 'links':[{'label':a.text(),'url':a.attrs['href']} for a in li.find('a')]})

research = []
for n in load('research').children:
    if not isinstance(n, Node):
        continue
    if n.tag == 'h3':
        research.append({'title':n.text().split(': ',1)[-1], 'paragraphs':[], 'image':''})
    elif research:
        if n.find('img'):
            research[-1]['image'] = image(n.find('img')[0])
        if n.tag == 'p' and n.text():
            research[-1]['paragraphs'].append(n.text())

news, group = [], ''
for n in load('lab-news').children:
    if not isinstance(n, Node):
        continue
    if n.tag == 'h3':
        group = n.text()
    if n.tag == 'p' and n.text():
        news.append({'category':group, 'text':n.text(), 'links':[{'label':a.text(),'url':a.attrs['href']} for a in n.find('a')]})

data = {'people':people, 'publications':publications, 'research':research, 'news':news}
(ROOT/'content').mkdir(exist_ok=True)
(ROOT/'content/site.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'migration/assets.json').write_text(json.dumps([{'url':u,'path':p} for u,p in assets.items()],indent=2)+'\n',encoding='utf-8')
print(json.dumps({'people':len(people),'publications':len(publications),'research':len(research),'news':len(news),'assets':len(assets)}))
for row in research + news:
    print(row)
