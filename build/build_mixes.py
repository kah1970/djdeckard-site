#!/usr/bin/env python3
"""Regenerate the djdeckard.com Mixes catalog shelves from build/catalog.csv.
Run: python3 build/build_mixes.py   (from site root). Injects into mixes.html
between the Featured grid and the btn-row. Featured 4 are hand-maintained.
Thumbnails: python3 build/build_mixes.py then run the download loop for any new build/downloads.txt rows."""
import csv, re, html, sys, os

CSV='build/catalog.csv'
PAGE='mixes.html'

# --- Curation overrides (keyed by permalink slug) ---
# sort  = volume position within its series shelf (overrides Series #)
# title = display-title override for the tile/list
OVERRIDES = {
    'deckard-50-1': {'sort': 8},   # 50th Birthday Set Pt.1  -> Vol 8 (between Vol 7 Brazil and Vol X)
    'deckard-50-2': {'sort': 9},   # 50th Birthday Set Pt.2  -> Vol 9
}

# --- Productions: original tracks, remixes, edits & bootlegs (own section, not mixes) ---
PRODUCTION_SLUGS = {
    'jack-the-ripper', 'myagi-viper-deckard-rumblemunk',
    'deckard-vs-rumblemunk-i-would-like-to-shout', 'deckard-rumblemunk-too-difficult-to-broadcast',
    'rocket-to-the-afterlife-bootletg', 'duck-that-shot-bootleg',
    'dance-to-the-music-deckard-re-edit',
}

rows=list(csv.DictReader(open(CSV,encoding='utf-8')))
def has_art(u): return bool(u) and 'avatars-' not in u
def slug(u): return re.sub(r'\?.*$','',(u or '').rstrip('/')).split('/')[-1]
def year(d): return (d or '')[:4]
def t200(u): return u.replace('-t500x500.','-t200x200.')

LIVE_KW=['live','ripecast','breakfast of champions',' boc','snowfest','campout','hoedown',
         'haunted','shoonanigans','boat party','end up','iand','playa','ghost ship asylum']

def clean(t):
    t=t.strip()
    for p in ['Deckard RIPEcast - ','Deckard RIPEcast: ','Deckard RIPEcast ','Deckard - ','Deckard_','Deckard ']:
        if t.startswith(p):
            rest=t[len(p):]
            # keep "Deckard" in collaboration credits (Deckard & X, Deckard vs X)
            if p in ('Deckard - ','Deckard_','Deckard ') and re.match(r'(?i)\s*(&|vs\b)', rest):
                break
            t=rest; break
    return t.strip()

def disp_title(r):
    o=OVERRIDES.get(slug(r['Permalink URL']),{})
    if o.get('title'): return o['title']
    t=clean(r['Title'])
    sh=r.get('_shelf')
    if sh=='mdoc': t=re.sub(r'(?i)^my definition of chill\b','',t)
    elif sh=='pp': t=re.sub(r'(?i)^party people\b','',t)
    if sh in ('mdoc','pp'):
        t=re.sub(r'^\s*[-\u2013\u2014:]\s*','',t)   # leading separator
        t=re.sub(r'\s{2,}',' ',t).strip()
    return t or clean(r['Title'])

def is_featured(r):
    t=r['Title'].lower(); d=r['Date'] or ''; sl=slug(r['Permalink URL'])
    if sl in ('after-party-2-into-the-night','mdoc-underworld','deckard-my-definition-of-chill-xii'): return True
    if d.startswith('2026-01') and 'breakfast of champions' in t and '26' in t: return True
    return False

def shelf(r):
    if slug(r['Permalink URL']) in PRODUCTION_SLUGS: return 'productions'
    if is_featured(r): return 'featured'
    s=r['Series']; t=r['Title'].lower()
    if s=='My Definition of Chill': return 'mdoc' if has_art(r['Artwork URL']) else 'more'
    if s=='Party People': return 'pp' if has_art(r['Artwork URL']) else 'more'
    if has_art(r['Artwork URL']) and any(k in t for k in LIVE_KW): return 'live'
    return 'more'

for r in rows: r['_shelf']=shelf(r)

def vol_key(r):
    o=OVERRIDES.get(slug(r['Permalink URL']),{})
    if 'sort' in o: return float(o['sort'])
    sn=r['Series #'] or '999'
    try: return float(sn)
    except: return 999.0
def date_key(r): return r['Date'] or '0000'

B={k:[r for r in rows if r['_shelf']==k] for k in ['featured','mdoc','pp','live','productions','more']}
B['mdoc'].sort(key=vol_key); B['pp'].sort(key=vol_key)
B['live'].sort(key=date_key,reverse=True); B['more'].sort(key=date_key,reverse=True)
B['productions'].sort(key=date_key,reverse=True)
print("SHELF COUNTS:",{k:len(v) for k,v in B.items()})

dl=[]
for k in ['mdoc','pp','live']:
    for r in B[k]:
        fn=slug(r['Permalink URL'])+'.jpg'
        if not os.path.exists(f'assets/img/mixes/catalog/{fn}'): dl.append((fn,t200(r['Artwork URL'])))
open('build/downloads.txt','w').write("".join(f"{fn}\t{u}\n" for fn,u in dl))
print("NEW THUMBS NEEDED:",len(dl))

def tile(r):
    fn=slug(r['Permalink URL'])+'.jpg'; t=html.escape(disp_title(r))
    return (f'        <a class="mix-tile" href="{html.escape(r["Permalink URL"])}" target="_blank" rel="noopener">\n'
            f'          <img class="mix-tile__art" src="assets/img/mixes/catalog/{fn}" alt="{t} cover art" loading="lazy">\n'
            f'          <div class="mix-tile__title">{t}</div>\n'
            f'          <div class="mix-tile__year">{year(r["Date"]) or ""}</div>\n        </a>')

def shelf_html(title,items,blurb):
    return (f'    <div class="shelf">\n      <div class="shelf__head">\n'
            f'        <h2 class="shelf__title">{title}</h2>\n'
            f'        <span class="shelf__meta">{blurb} &middot; {len(items)}</span>\n      </div>\n'
            f'      <div class="shelf__track">\n'+"\n".join(tile(r) for r in items)+'\n      </div>\n    </div>')

def list_html(title,items,blurb):
    lis="\n".join(
        f'        <li><a href="{html.escape(r["Permalink URL"])}" target="_blank" rel="noopener">'
        f'<span class="mix-index__t">{html.escape(disp_title(r))}</span>'
        f'<span class="mix-index__y">{year(r["Date"]) or ""}</span></a></li>' for r in items)
    return (f'    <div class="more-list">\n      <div class="shelf__head"><h2 class="shelf__title">{title}</h2>'
            f'<span class="shelf__meta">{blurb} &middot; {len(items)}</span></div>\n'
            f'      <ul class="mix-index">\n{lis}\n      </ul>\n    </div>')

frag="\n".join([
    shelf_html("My Definition of Chill",B['mdoc'],"downtempo series, vol. I &rarr; now"),
    shelf_html("Party People",B['pp'],"the dancefloor series"),
    shelf_html("Live &amp; Events",B['live'],"RIPEcast, BoC &amp; festival recordings"),
    list_html("Productions",B['productions'],"originals, remixes, edits &amp; bootlegs"),
    list_html("More mixes &amp; one-offs",B['more'],"mixes, one-offs &amp; art-pending"),
])
open('build/mixes_shelves.html','w',encoding='utf-8').write(frag)

# inject: swap region between first .shelf and the btn-row
m=open(PAGE,encoding='utf-8').read()
a=m.index('    <div class="shelf">'); b=m.index('    <div class="btn-row">')
m=m[:a]+frag+'\n\n'+m[b:]
open(PAGE,'w',encoding='utf-8').write(m)
print("Injected shelves into",PAGE)
