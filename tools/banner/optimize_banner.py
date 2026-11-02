"""Compile a layered banner for an animated GitHub <img>.
Usage: python optimize_banner.py source.svg output.svg
Requires Pillow and CairoSVG. Native source remains separate and editable.
"""
import base64, io, re, sys, functools
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
import cairosvg
SVG='http://www.w3.org/2000/svg'
ET.register_namespace('',SVG)
RATE=12
@functools.lru_cache(maxsize=64)
def image_cache(url,width,height):
    mime,payload=url.split(';base64,',1)
    data=base64.b64decode(payload)
    if mime.endswith('svg+xml'):
        data=cairosvg.svg2png(bytestring=data,output_width=width,output_height=height)
    image=Image.open(io.BytesIO(data))
    if image.size!=(width,height):image=image.resize((width,height),Image.Resampling.LANCZOS)
    out=io.BytesIO();image.save(out,format='WEBP',lossless=True,method=6)
    return 'data:image/webp;base64,'+base64.b64encode(out.getvalue()).decode()
def optimize_svg(source):
    root=ET.fromstring(source)
    for parent in root.iter():
        for child in list(parent):
            if child.get('id') in ('watchful-eyes','watchful-eye-style','readme-performance'):parent.remove(child)
    for image in root.iter():
        if image.tag.split('}')[-1]!='image':continue
        url=image.get('href','')
        if url.startswith('data:image/'):
            image.set('href',image_cache(url,round(float(image.get('width'))),round(float(image.get('height')))))
    rules=['.sculpture-sway,.wing-left,.wing-right{animation-timing-function:steps(54,end)}',
           '.wing-right{animation-delay:-.5s}',
           '#terminal-kernel-cursor{animation-delay:-.5s}',
           '.matrix-easter-egg{animation-timing-function:steps(4,end)}']
    for image in root.iter():
        if image.get('class')!='rain-image':continue
        timing=image.get('style','')
        speed=float(re.search(r'--speed:([\d.]+)s',timing)[1]);delay=float(re.search(r'--delay:([-\d.]+)s',timing)[1])
        speed=round(speed/3)*3;delay=round(delay*RATE)/RATE
        rules.append('#'+image.get('id')+'{animation-duration:'+str(speed)+'s;animation-delay:'+f'{delay:.8f}'+'s;animation-timing-function:steps('+str(speed//3*RATE)+',end)}')
    ET.SubElement(root,'{'+SVG+'}style',{'id':'readme-performance'}).text='\n'.join(rules)
    desc=next(e for e in root if e.tag.split('}')[-1]=='desc')
    desc.text='POHL ANGEL banner. AI & Full-Stack Developer, ~/construct and momokoboi. Carbon grain, soft green portal and terminals, four foreground fingers around the G and thumb behind. Eyes removed. Detailed layers cached at banner resolution; wing and Matrix motion share a 12-update-per-second clock. Reduced motion stops animation. Native editable vector source retained separately.'
    return ET.tostring(root,encoding='unicode')
if __name__=='__main__':
    Path(sys.argv[2]).write_text(optimize_svg(Path(sys.argv[1]).read_text()))
