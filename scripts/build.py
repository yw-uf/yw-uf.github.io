"""Generate a portable, dependency-free GitHub Pages website from content/site.json."""
from pathlib import Path
from html import escape as esc
import json
import shutil
import argparse
import hashlib

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
RESEARCH = json.loads((ROOT/'content/research.json').read_text(encoding='utf-8'))
SCHOLAR = 'https://scholar.google.com/citations?user=vwYRxDoAAAAJ&hl=en'
PROFILE = 'https://mae.ufl.edu/people/profiles/yu-wang/'
NOTES = 'https://drive.google.com/file/d/1JTJWcs9-e6gTbjv6CqWd5kB8aI3zXcfB/view'
STYLE_VERSION = hashlib.sha256((ROOT/'assets/style.css').read_bytes()).hexdigest()[:12]
NAV = [('index.html','PI'),('research.html','Research'),('teaching.html','Teaching'),('people.html','Team')]

def link(url, label, cls=''):
    if url == 'yu-wang.html':
        url = 'index.html'
    return f'<a href="{esc(url,quote=True)}" class="{cls}">{label}</a>'

def title(kicker, heading, description=''):
    intro = f'<p class="lede">{description}</p>' if description else ''
    return f'<header class="page-heading wrap"><p class="eyebrow">{kicker}</p><h1>{heading}</h1>{intro}</header>'

def shell(filename, heading, body):
    active = filename
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url==active else '')+f'>{label}</a>' for url,label in NAV)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{heading} | Yu Wang</title>
<meta name="description" content="Embodied Intelligence Lab at the University of Florida. Yu Wang's research in assured autonomy, machine learning, formal methods, and control theory.">
<meta name="theme-color" content="#123d48"><meta property="og:title" content="{heading} | Embodied Intelligence Lab"><meta property="og:description" content="Assured autonomy through learning, logic, and control. University of Florida · Yu Wang."><meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css?v={STYLE_VERSION}"><script defer src="assets/site.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<div class="university-bar"><div class="wrap">University of Florida <span>Mechanical &amp; Aerospace Engineering</span></div></div>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="Embodied Intelligence Lab home"><span>Embodied Intelligence Lab<small>Yu Wang · University of Florida</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation">{nav}</nav></div></header>
<main id="main">{body}</main>
<footer><div class="wrap footer-grid"><div><a class="footer-brand" href="index.html">Yu Wang · University of Florida</a></div></div></footer></body></html>'''

def publications(rows):
    out = ''
    for p in rows:
        links = ''.join(link(a['url'], 'Paper ↗', 'text-link') for a in p['links'])
        out += f'<li class="publication" data-type="{esc(p["type"])}" data-year="{p["year"] or "Undated"}"><span class="pub-year">{p["year"] or "—"}</span><div><p>{esc(p["citation"])}</p>{links}<span class="pub-type">{esc(p["type"])}</span></div></li>'
    return out

def group():
    body = title('Embodied Intelligence Lab', 'Embodied Intelligence Lab', esc(RESEARCH['introduction']))
    body += '<section class="wrap section"><h2>Research themes</h2><div class="theme-grid">'
    for theme in RESEARCH['themes']:
        body += f'<a class="theme-card" href="research.html#{theme["id"]}"><img src="{theme["image"]}" alt="{esc(theme["image_alt"])}" width="1536" height="1024" loading="lazy"><h3>{esc(theme["title"])}</h3><p>{esc(theme["question"])}</p><span class="text-link">Explore research →</span></a>'
    body += '</div></section>'
    body += '<section class="wrap section home-links"><div><h2>Principal investigator</h2><p>Yu Wang<br>Assistant Professor, University of Florida<br>Mechanical and Aerospace Engineering</p>'+link('yu-wang.html','Meet the PI →','text-link')+'</div><div><h2>Our people</h2><p>Meet our researchers, students, and alumni.</p>'+link('people.html','People →','text-link')+'</div><div><h2>News</h2><p>Lab milestones, awards, and presentations.</p>'+link('news.html','Lab news →','text-link')+'</div></section>'
    return body

def home():
    body = title('Embodied Intelligence Lab', 'Embodied Intelligence Lab', esc(RESEARCH['introduction']))
    for section_id, render in [('pi',profile),('research',research),('teaching',teaching),('people',people),('news',news)]:
        content = (research(embedded=True) if section_id=='research' else render()).replace('<h1>', '<h2>').replace('</h1>', '</h2>')
        body += f'<section id="{section_id}" class="page-section">{content}</section>'
    return body

def research(embedded=False):
    body = title('Research','Research','' if embedded else esc(RESEARCH['introduction']))
    for theme in RESEARCH['themes']:
        # Retain old fragment links while replacing the old project content.
        alias = '<span id="decision-making"></span>' if theme['id']=='human-guided-learning' else ('<span id="verification"></span>' if theme['id']=='reliable-planning' else '')
        papers = ''.join('<li>'+esc(p['authors'])+', “'+ (link(p['url'],esc(p['title'])) if p['url'] else esc(p['title'])) +'.” <em>'+esc(p['venue'])+'</em>'+(', '+esc(p['details']) if p.get('details') else '')+'.</li>' for p in theme['papers'])
        body += f'<section id="{theme["id"]}" class="wrap section research-theme">{alias}<div class="theme-intro"><figure><img src="{theme["image"]}" alt="{esc(theme["image_alt"])}" width="1536" height="1024" loading="lazy"></figure><div><h2>{esc(theme["title"])}</h2><p class="theme-question">{esc(theme["question"])}</p><p>{esc(theme["description"])}</p></div></div><h3>Selected work</h3><ul class="theme-papers">{papers}</ul></section>'
    logos = ''.join(link(s['url'],f'<img src="{s["image"]}" alt="{esc(s["name"])}" loading="lazy"><span>{esc(s["name"])}</span>','sponsor') for s in RESEARCH['sponsors'])
    body += '<section class="wrap research-more">'+link(SCHOLAR,'Full publication list on Google Scholar ↗','text-link')+'</section>'
    return body + '<section class="wrap sponsors"><h2>Sponsors</h2><div class="sponsor-row">'+logos+'</div></section>'

def people():
    body = title('Our team','Team','Researchers, students, and alumni of the Embodied Intelligence Lab at the University of Florida.')
    groups = list(dict.fromkeys(p['group'] for p in DATA['people']))
    groups = [g for g in groups if g != 'Alumni'] + (['Alumni'] if 'Alumni' in groups else [])
    for group in groups:
        if group == 'Undergraduate Researchers':
            body += '<section class="wrap people-section"><h2>Undergraduate Researchers</h2><p class="subtle">To be updated.</p></section>'
            continue
        body += '<section class="wrap people-section"><h2>'+esc(group.replace('Master Students',"Master’s Students"))+'</h2><div class="people-grid">'
        for p in [p for p in DATA['people'] if p['group']==group]:
            links = ''
            for a in p['links']:
                if a.get('kind')=='video':
                    links += link(a['url'],esc(a['label'])+' ↗','text-link')
                else:
                    links += link(a['url'],esc(a['label'])+' ↗' if a.get('kind')=='overview' else esc(a.get('kind','Dissertation'))+': '+esc(a['label'])+' ↗','text-link')
            photo = ''
            dates = f'<p class="person-dates">{esc(p["dates"])}</p>' if p.get('dates') else ''
            bio = f'<p class="person-bio">{esc(p["bio"])}</p>' if p.get('bio') and p['name']!='Yu Wang' else ''
            body += f'<article class="person">{photo}<div class="person-copy"><h3>{esc(p["name"])}</h3><p class="person-role">{esc(p["role"])}</p>{dates}{bio}{links}</div></article>'
        body += '</div></section>'
    return body

def pubs():
    types = list(dict.fromkeys(p['type'] for p in DATA['publications']))
    years = sorted({p['year'] for p in DATA['publications'] if p['year']},reverse=True)
    body = title('Publications','Publications','Journal articles, conference proceedings, and workshop presentations on learning, verification, privacy, and control.')
    body += '<section class="wrap publications-section"><div class="pub-tools"><label>Search publications<input id="pub-search" type="search" placeholder="Title, author, or keyword…"></label><label>Publication type<select id="pub-type"><option value="">All types</option>'+''.join(f'<option>{esc(t)}</option>' for t in types)+'</select></label><label>Year<select id="pub-year"><option value="">All years</option>'+''.join(f'<option>{y}</option>' for y in years)+'<option>Undated</option></select></label></div><div class="pub-toolbar"><p id="pub-count" role="status">'+str(len(DATA['publications']))+' publications</p>'+link(SCHOLAR,'Google Scholar ↗','text-link')+'</div><p class="subtle">Publication details and submission statuses are retained from the original lab website.</p><ul class="publication-list" id="publications">'+publications(DATA['publications'])+'</ul><p id="pub-empty" hidden>No publications match these filters. Try a different keyword or year.</p></section>'
    return body

def profile():
    body = f'''<section class="wrap faculty-hero"><div><p class="eyebrow">Faculty profile</p><h1>Yu Wang</h1><p class="lede">Assistant Professor<br>Mechanical &amp; Aerospace Engineering<br>University of Florida</p><p>Affiliations: UF Transportation Institute, Florida Institute for National Security, and Florida Institute for Cybersecurity Research.</p><div class="hero-actions">{link(PROFILE,'UF directory &amp; contact ↗','text-link')}</div></div></section>
<section class="wrap career-grid section"><div><p class="eyebrow">Experience</p><h2>Academic appointments</h2><div class="career-item"><span>2021–Present</span><h3>University of Florida</h3><p>Assistant Professor<br>Mechanical and Aerospace Engineering</p></div><div class="career-item"><span>2018–2021</span><h3>Duke University</h3><p>Postdoctoral Associate<br>Electrical and Computer Engineering</p></div></div><div><p class="eyebrow">Education</p><h2>Academic background</h2><div class="career-item"><h3>University of Illinois<br>at Urbana-Champaign</h3><ul><li>Ph.D. in Mechanical Engineering, 2018</li><li>M.S. in Statistics, 2017</li><li>M.S. in Mathematics, 2016</li><li>M.S. in Mechanical Engineering, 2014</li></ul></div><div class="career-item"><h3>Tsinghua University</h3><p>B.E. in Engineering Mechanics, 2012</p></div></div></section>'''
    return body

def teaching():
    return title('Teaching','Teaching','Course materials and notes from Yu Wang at the University of Florida.') + f'''<section class="wrap course section"><div class="course-number">EML<br><strong>6352</strong><span>University of Florida</span></div><div><p class="eyebrow">Graduate course</p><h2>Optimal Estimation<br>and Kalman Filtering</h2><p>Notes on estimation, probability, and filtering.</p>{link(NOTES,'Read the course notes ↗','button')}<div class="course-notes"><h3>About the notes</h3><p>In developing these notes, I have drawn inspiration from the excellent treatments in Casella &amp; Berger’s <em>Mathematical Statistics</em> and Bruce Hajek’s <em>Random Processes for Engineers</em>. Special thanks to Prabir Barooah and Sanjay Lall for helping develop these materials. I also used AI tools to help polish the final text.</p><p>I really enjoyed the pedagogical style of David Tong’s {link('https://www.damtp.cam.ac.uk/user/tong/teaching.html','lecture notes on theoretical physics')}. I try to follow his example, but I’m not quite there yet.</p></div></div></section>'''

def news():
    body = title('Lab news','Lab news','Awards, graduations, talks, and posters from the Embodied Intelligence Lab archive.')
    for group in dict.fromkeys(n['category'] for n in DATA['news']):
        body += '<section class="wrap section news-section"><h2>'+esc(group)+'</h2><div class="news-list">'
        for n in [n for n in DATA['news'] if n['category']==group]:
            text = n['text']
            # Separate dates without rewriting the original announcements.
            parts = text.split(' – ',1) if ' – ' in text else text.split(' — ',1)
            if len(parts)==1:
                import re
                parts = re.split(r'(?:\s+)[–—�](?:\s+)',text,maxsplit=1)
            date, announcement = parts if len(parts)==2 else ('',text)
            import re
            announcement = re.sub(r'https?://\S+','',announcement).strip()
            links = ''.join(link(a['url'],'Source ↗','text-link') for a in n['links'])
            body += f'<article class="news-item"><p class="news-date">{esc(date)}</p><div><p>{esc(announcement)}</p><div class="news-links">{links}</div></div></article>'
        body += '</div></section>'
    return body

def build():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',default='_site')
    args = parser.parse_args()
    dest = (ROOT/args.output).resolve()
    if not dest.is_relative_to(ROOT) or dest==ROOT:
        raise ValueError('Build output must be a subdirectory of this repository')
    dest.mkdir(parents=True,exist_ok=True)
    (dest/'assets').mkdir(exist_ok=True)
    for asset in ['style.css','site.js','favicon.svg']:
        shutil.copy2(ROOT/'assets'/asset,dest/'assets'/asset)
    for directory in ['research','sponsors','videos']:
        shutil.copytree(ROOT/'assets'/directory,dest/'assets'/directory,dirs_exist_ok=True)
    # Remove obsolete generated pages when rebuilding an older local preview.
    for filename in ['group.html','publications.html','yu-wang.html','news.html']:
        (dest/filename).unlink(missing_ok=True)
    pages = [('index.html','PI',profile),('research.html','Research',research),('teaching.html','Teaching',teaching),('people.html','Team',people)]
    for filename,heading,render in pages:
        (dest/filename).write_text(shell(filename,heading,render()),encoding='utf-8')
    (dest/'.nojekyll').write_text('',encoding='utf-8')
    print(f'Built {len(pages)} pages in {dest}')

if __name__=='__main__':
    build()

