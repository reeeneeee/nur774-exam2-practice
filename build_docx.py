"""Merge parts/*.md into one .docx (no external deps) and a combined .md."""
import glob, re, zipfile, html, sys
parts = sorted(glob.glob('parts/*.md'))
md = "\n\n".join(open(p).read().strip() for p in parts)
open('NUR774_Exam2_Practice_100Q.md','w').write("# NUR 774 Pediatrics Exam 2 — 100-Question Practice Test\n\n" + md + "\n")
def runs(text, base_bold=False):
    out=[]
    for i,seg in enumerate(re.split(r'\*\*', text)):
        if not seg: continue
        b = base_bold or (i%2==1)
        out.append('<w:r><w:rPr>%s<w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % ('<w:b/>' if b else '', html.escape(seg, quote=False)))
    return ''.join(out)
def para(text, style=None, bold=False, space_after=80, color=None, size=None):
    ppr = '<w:pPr>%s<w:spacing w:after="%d"/></w:pPr>' % (f'<w:pStyle w:val="{style}"/>' if style else '', space_after)
    r = runs(text, bold)
    if color: r = r.replace('<w:rPr>', f'<w:rPr><w:color w:val="{color}"/>')
    if size: r = r.replace('<w:sz w:val="22"/>', f'<w:sz w:val="{size}"/>')
    return f'<w:p>{ppr}{r}</w:p>'
body=[para('NUR 774 Pediatrics — Exam 2 Practice Test (100 Questions)', bold=True, size=36), para('Built from your Exam 2 blueprint. Answers follow the professor’s notes; rationales flag where textbooks differ.', color='555555', space_after=240)]
qcount=0
for line in md.splitlines():
    s=line.rstrip()
    if not s.strip(): continue
    if s.strip()=='---':
        body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="BBBBBB"/></w:pBdr><w:spacing w:after="200"/></w:pPr></w:p>'); continue
    if re.match(r'\*\*Q\d+\.', s): qcount+=1; body.append(para(s, space_after=120)); continue
    if s.startswith('**Answer:**'): body.append(para(s, color='1F6B2E')); continue
    if s.startswith('**Rationale:**'): body.append(para(s, color='333333', space_after=160)); continue
    if s.startswith('#'): body.append(para(s.lstrip('# '), bold=True, size=28)); continue
    body.append(para(s, space_after=40))
doc=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
     + ''.join(body) + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
ct='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
rels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
with zipfile.ZipFile('NUR774_Exam2_Practice_100Q.docx','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml',ct); z.writestr('_rels/.rels',rels); z.writestr('word/document.xml',doc)
print(f"parts={len(parts)} questions={qcount} sata={md.count('[SATA]')} single={md.count('[Single]')}")
