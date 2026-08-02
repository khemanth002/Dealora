import json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
FEEDS=[("USA","Slickdeals","https://slickdeals.net/newsearch.php?mode=frontpage&rss=1&searcharea=deals&searchin=first"),("Canada","RedFlagDeals","https://forums.redflagdeals.com/feed/forum/9"),("India","Google News","https://news.google.com/rss/search?q=India%20Amazon%20Flipkart%20deals&hl=en-IN&gl=IN&ceid=IN:en")]
H={"User-Agent":"DealoraFeedReader/1.0 (+https://khemanth002.github.io/Dealora/)"}
def txt(n,k):
 e=n.find(k);return (e.text or "").strip() if e is not None else ""
def img(item,desc):
 for c in item:
  tag=c.tag.lower();u=c.attrib.get("url","");typ=c.attrib.get("type","")
  if u and ("image" in typ or tag.endswith(("content","thumbnail"))):return u
 m=re.search(r'<img[^>]+src=["\']([^"\']+)',desc,re.I);return unescape(m.group(1)) if m else ""
def price(t,c):
 m=re.search({"USA":r'\$[\d,.]+',"Canada":r'(?:CA\$|\$)[\d,.]+',"India":r'₹[\d,.]+'}[c],t);return m.group(0) if m else "See deal"
def cat(t):
 t=t.lower()
 if any(x in t for x in ("laptop","phone","tv","headphone","tech","camera","gaming")):return "Tech"
 if any(x in t for x in ("shoe","shirt","fashion","jacket","dress")):return "Fashion"
 if any(x in t for x in ("food","coffee","pizza","restaurant")):return "Food"
 if any(x in t for x in ("hotel","flight","travel")):return "Travel"
 return "Home"
out=[]
for country,source,url in FEEDS:
 try:
  req=urllib.request.Request(url,headers=H);root=ET.fromstring(urllib.request.urlopen(req,timeout=25).read())
  for i,item in enumerate(root.findall(".//item")[:12]):
   title=unescape(txt(item,"title"));link=txt(item,"link");desc=txt(item,"description")
   if title and link:out.append({"id":f"{country.lower()}-{i}","country":country,"period":"Monthly" if i%4==0 else "Daily","category":cat(title),"brand":source,"title":re.sub(r"\s+"," ",title)[:150],"price":price(title,country),"was":"","off":"LIVE DEAL","code":"","expires":"Recently posted","emoji":"🔥","color":{"USA":"#6555ef","Canada":"#d52b45","India":"#ff7a21"}[country],"image":img(item,desc),"url":link,"source":source})
 except Exception as e:print(source,e)
with open("deals.json","w",encoding="utf-8") as f:json.dump({"updatedAt":datetime.now(timezone.utc).isoformat(),"deals":out},f,ensure_ascii=False,indent=2)
print("Wrote",len(out),"deals")
