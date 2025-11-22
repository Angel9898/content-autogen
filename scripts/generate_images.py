import os, sys, json, requests
from PIL import Image, ImageDraw, ImageFont
HF_KEY = os.getenv('HF_API_KEY')
MODEL = os.getenv('HF_IMAGE_MODEL','stabilityai/stable-diffusion-xl-base-1.0')
path = sys.argv[1] if len(sys.argv)>1 else 'assets/content.json'
with open(path,encoding='utf-8') as f: data=json.load(f)
os.makedirs('assets/images', exist_ok=True)
font = ImageFont.load_default()
for i, slide in enumerate(data.get('ig_carousel',[]), start=1):
    out = f'assets/images/slide{i:02d}.png'
    prompt = f"{data.get('title','')}: {slide}"
    try:
        if HF_KEY:
            url = f'https://api-inference.huggingface.co/models/{MODEL}'
            headers = {'Authorization':f'Bearer {HF_KEY}'}
            r = requests.post(url, headers=headers, json={'inputs':prompt}, timeout=120)
            r.raise_for_status()
            with open(out,'wb') as fh: fh.write(r.content)
            print('Wrote', out); continue
    except Exception as e:
        print('HF image failed', e)
    im = Image.new('RGB', (1080,1350), (240,240,240))
    d = ImageDraw.Draw(im)
    d.text((60,80), slide, fill=(10,10,10), font=font)
    im.save(out)
    print('Wrote fallback', out)
# thumbnail
thumb='assets/thumbnail.png'
Image.new('RGB',(1280,720),(20,20,20)).save(thumb)
print('Image generation complete')
