import os, json
from helpers.model_clients import gen_text
from helpers.utils import save_json
os.makedirs('assets', exist_ok=True)
PROMPT = open('templates/prompt_templates.md').read()
production_prompt = PROMPT + '\nTopic: AI productivity hacks. Return a JSON object.'
raw = gen_text(production_prompt)
try:
    data = json.loads(raw)
except Exception:
    data = {'title': raw.split('\n')[0][:60], 'linkedin_post': raw[:1000], 'x_post': raw[:280], 'ig_carousel': [raw[i:i+120] for i in range(0,600,120)][:5], 'yt_script': raw[:800], 'hashtags': ['#AI']}
save_json(data,'assets/content.json')
print('Wrote assets/content.json')
