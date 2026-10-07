"""Check generated pages for missing local links, images, fragments, and content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/'_site'
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.refs, self.ids, self.h1, self.lang = [], set(), 0, ''
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            assert a['id'] not in self.ids, 'Duplicate HTML id'
            self.ids.add(a['id'])
        if tag=='h1': self.h1 += 1
        if tag=='html': self.lang = a.get('lang','')
        if tag=='img': assert a.get('alt'), 'Image missing alternative text'
        for key in ('src','href'):
            if a.get(key): self.refs.append(a[key])

pages = {p:Page(p) for p in SITE.glob('*.html')}
assert {p.name for p in pages}=={'index.html','research.html','teaching.html','people.html'}, 'Expected exactly four tab pages'
for path,page in pages.items():
    assert page.h1==1 and page.lang=='en', f'Invalid page structure: {path}'
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        target = (path.parent/unquote(url.path)).resolve() if url.path else path
        assert target.is_relative_to(SITE.resolve()), f'Link escapes site: {ref}'
        assert target.exists(), f'Missing local resource: {path.name} → {ref}'
        if url.fragment and target.suffix=='.html':
            assert unquote(url.fragment) in pages[target].ids, f'Missing fragment: {ref}'
data = json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
research = json.loads((ROOT/'content/research.json').read_text(encoding='utf-8'))
research_html = (SITE/'research.html').read_text(encoding='utf-8')
selected = [p for theme in research['themes'] for p in theme['papers']]
from html import escape
assert all(escape(p['title']) in research_html for p in selected), 'Selected paper lost during rendering'
people_html = (SITE/'people.html').read_text(encoding='utf-8')
visible_people = [p for p in data['people'] if p['group']!='Undergraduate Researchers']
assert people_html.count('class="person"')==len(visible_people), 'Person lost during rendering'
assert 'Undergraduate Researchers</h2><p class="subtle">To be updated.</p>' in people_html, 'Undergraduate section should show the update notice'
print(f'Validated {len(pages)} pages, local resources, fragments, {len(selected)} selected papers, and {len(visible_people)} people.')
