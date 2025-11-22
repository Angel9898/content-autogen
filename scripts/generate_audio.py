import os, sys, json, requests
HF_KEY = os.getenv('HF_API_KEY')
path = sys.argv[1] if len(sys.argv)>1 else 'assets/content.json'
out = sys.argv[2] if len(sys.argv)>2 else 'assets/audio.mp3'
with open(path,encoding='utf-8') as f: data=json.load(f)
scr = data.get('yt_script','') or data.get('linkedin_post','')
if not scr:
    open(out,'wb').write(b''); print('No script; silent audio'); raise SystemExit(0)
if HF_KEY:
    url = 'https://api-inference.huggingface.co/models/facebook/tts_transformer'
    headers={'Authorization':f'Bearer {HF_KEY}'}
    r = requests.post(url, headers=headers, json={'inputs':scr}, timeout=120)
    if r.status_code==200:
        open(out,'wb').write(r.content); print('Wrote audio', out); raise SystemExit(0)
print('TTS not available or failed; writing silent audio')
open(out,'wb').write(b'')
