# -*- coding: utf-8 -*-
"""单文件页面的结构自检：括号平衡、id 唯一性、i18n 键对齐、标签闭合。

用法:  python3 tools/validate.py [index.html]

这个游戏没有构建步骤，所有代码都在一个 HTML 文件里，所以改动之后靠这个脚本
兜底 —— 它抓的都是历史上真实踩过的坑：正则替换吃掉了半个函数、
applyLang 改成自递归、重复 id 让 getElementById 静默返回第一个。
"""
import io,re,sys,collections
p=sys.argv[1] if len(sys.argv)>1 else "index.html"
s=io.open(p,encoding="utf-8").read()
bad=[]

def strip_js(t):
    """去掉字符串/正则/注释，返回同长度的骨架(替换成空格)"""
    out=list(t); i=0; n=len(t); st=None; prev=''
    while i<n:
        c=t[i]
        if st is None:
            if c in "\"'`":
                st=c; out[i]=' '
            elif c=='/' and i+1<n and t[i+1]=='/':
                while i<n and t[i]!='\n': out[i]=' '; i+=1
                continue
            elif c=='/' and i+1<n and t[i+1]=='*':
                while i<n and not (t[i]=='*' and i+1<n and t[i+1]=='/'): out[i]=' '; i+=1
                out[i]=' ';out[i+1]=' ';i+=2;continue
            elif c=='/' and prev in '(,=:[!&|?{;+-*%~^<>' :
                # 正则字面量
                out[i]=' '; i+=1
                while i<n and t[i]!='/':
                    if t[i]=='\\': out[i]=' ';i+=1
                    if i<n: out[i]=' ';i+=1
                if i<n: out[i]=' ';i+=1
                continue
            if not c.isspace(): prev=c
        else:
            out[i]=' '
            if c=='\\': out[i+1]=' '; i+=2; continue
            if c==st: st=None; prev='x'
        i+=1
    return ''.join(out)

# ---- script 块括号平衡 + 顶层函数深度 ----
blocks=re.findall(r'<script[^>]*>([\s\S]*?)</script>',s)
for bi,b in enumerate(blocks):
    sk=strip_js(b)
    d=0;par=0;br=0;ok=True
    for ch in sk:
        if ch=='{':d+=1
        elif ch=='}':
            d-=1
            if d<0: bad.append("script#%d 花括号提前闭合"%bi); ok=False; break
        elif ch=='(':par+=1
        elif ch==')':par-=1
        elif ch=='[':br+=1
        elif ch==']':br-=1
    if ok and (d or par or br):
        bad.append("script#%d 不平衡 {}=%d ()=%d []=%d"%(bi,d,par,br))
    else:
        print("script#%d 括号平衡 ok (%d 行)"%(bi,b.count('\n')+1))

# ---- CSS 平衡 ----
css=re.findall(r'<style[^>]*>([\s\S]*?)</style>',s)
for c in css:
    if c.count('{')!=c.count('}'): bad.append("CSS 不平衡")
print("CSS %d/%d"%(sum(c.count('{') for c in css),sum(c.count('}') for c in css)))

# ---- 重复 id / 未定义 $() ----
ids=re.findall(r'\sid="([^"]+)"',s)
dup=[k for k,v in collections.Counter(ids).items() if v>1]
if dup: bad.append("重复 id: "+",".join(dup))
refs=set(re.findall(r'\$\("([A-Za-z0-9_]+)"\)',s))
miss=sorted(r for r in refs if r not in ids)
if miss: bad.append("未定义 id: "+",".join(miss))
print("id: %d 个, 重复 %d, 未定义引用 %d"%(len(ids),len(dup),len(miss)))

# ---- applyLang 自递归 ----
m=re.search(r'function applyLang\(\)\{',s)
if m:
    i=m.end(); d=1
    while d>0 and i<len(s):
        if s[i]=='{':d+=1
        elif s[i]=='}':d-=1
        i+=1
    if 'applyLang(' in s[m.end():i-1]: bad.append("applyLang 直接自递归")
    print("applyLang 自递归检查 ok")

# ---- i18n 键 ----
L=s.split("\n")
iz=next(i for i,l in enumerate(L) if l.strip()=="zh:{")
ie=next(i for i,l in enumerate(L) if l.strip()=="en:{")
iend=next(i for i,l in enumerate(L) if i>ie and l.strip()=="};")
zh="\n".join(L[iz+1:ie]); en="\n".join(L[ie+1:iend])
def keys(b): return set(re.findall(r'^\s*([A-Za-z][A-Za-z0-9_]*)\s*:',b,re.M))|set(re.findall(r',\s*([A-Za-z][A-Za-z0-9_]*)\s*:',b))
K1,K2=keys(zh),keys(en)
need=set(re.findall(r'data-i18n(?:-html)?="([^"]+)"',s))|set(re.findall(r'T\("([A-Za-z0-9_]+)"\)',s))
if K1-K2: bad.append("仅中文有: "+",".join(sorted(K1-K2)))
if K2-K1: bad.append("仅英文有: "+",".join(sorted(K2-K1)))
if need-K1: bad.append("缺翻译: "+",".join(sorted(need-K1)))
orph=K1-need
print("i18n zh=%d en=%d, 用到 %d, 孤儿键: %s"%(len(K1),len(K2),len(need),",".join(sorted(orph)) or "none"))

# ---- 标签平衡 ----
for tag in ("div","section","span","p","article","label","button"):
    o=len(re.findall(r'<%s[\s>]'%tag,s)); c=len(re.findall(r'</%s>'%tag,s))
    sc=len(re.findall(r'<%s[^>]*/>'%tag,s))
    if o-sc!=c: bad.append("<%s> %d 开 / %d 闭"%(tag,o-sc,c))
print("标签平衡检查完毕")

print("\n=== %s ==="%("全部通过" if not bad else "发现 %d 处问题"%len(bad)))
for b in bad: print(" ! "+b)
sys.exit(1 if bad else 0)
