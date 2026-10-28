#!/usr/bin/env python3
"""Optional network acquisition. Standard library only. Dataset CC BY-NC-SA 4.0.

Usage: python notes/acquire_sigla_words.py BROWSE_HTML CACHE_DIRECTORY OUTPUT_JSON
The sequence inventory is for discovery: boundaries are not certified by this parser.
"""
import concurrent.futures as cf
import datetime, hashlib, html, json, re, sys, urllib.parse, urllib.request
from pathlib import Path

browse, cache, output = map(Path, sys.argv[1:4])
cache.mkdir(parents=True, exist_ok=True)
docs = sorted(set(html.unescape(s) for s in re.findall(r'title="View document" href="document/([^/"]+)/"', browse.read_text())))
def fetch(doc):
    url='https://sigla.phis.me/document/'+urllib.parse.quote(doc,safe='')+'/index-word.html'
    path=cache/(doc.replace(' ','_')+'.html')
    try:
        raw=path.read_bytes() if path.exists() else urllib.request.urlopen(url, timeout=40).read()
        if not path.exists(): path.write_bytes(raw)
        txt=raw.decode()
        words=[]
        for num,body in re.findall(r'id="word-(\d+)">(.+?) \(\d+ signs?\)</span>',txt):
            a=re.search(r'<a[^>]*>(.+)</a>',body)
            if not a: continue
            signspans=re.findall(r'<span class="([^"]*reading[^\"]*)">(.*?)</span>',a.group(1))
            form=html.unescape(re.sub('<[^>]*>','',a.group(1))).upper()
            words.append({'sequence_index_zero_based':int(num),'form':form,'reading_classes':[x[0] for x in signspans],'signs':[html.unescape(re.sub('<[^>]*>','',x[1])).upper() for x in signspans]})
        metadata=re.search(r'<div class="document-metadata">(.*?)</div>',txt,re.S)
        return {'document_face':doc,'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'metadata_text':html.unescape(re.sub('<[^>]+>',' ',metadata.group(1))) if metadata else None,'sequences':words,'error':None}
    except Exception as e:
        return {'document_face':doc,'url':url,'error':str(e)}

rows=[]
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for i,row in enumerate(ex.map(fetch,docs),1):
        rows.append(row)
        if i%50==0: print(i,'/',len(docs),'completed',flush=True)
obj={'acquired_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'SigLA, Ester Salgarella and Simon Castellan','license':'CC BY-NC-SA 4.0','license_url':'https://creativecommons.org/licenses/by-nc-sa/4.0/','browse_sha256':hashlib.sha256(browse.read_bytes()).hexdigest(),'coverage':'All document-face links in the supplied browse page; sequence indexing can include fragments and face segments. Not a critical edition.','documents':rows}
output.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'total':len(rows),'errors':sum(bool(x['error']) for x in rows),'sequences':sum(len(x.get('sequences',[])) for x in rows)}),flush=True)
