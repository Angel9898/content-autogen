"""Model client wrappers. Use env vars to configure real endpoints (Gemini/OpenAI/HF).
"""
import os, requests, json
HF_API_KEY = os.getenv('HF_API_KEY')

def gen_text(prompt: str):
    if HF_API_KEY:
        model = os.getenv('HF_TEXT_MODEL','gpt2')
        url = f'https://api-inference.huggingface.co/models/{model}'
        headers = {'Authorization':f'Bearer {HF_API_KEY}'}
        try:
            r = requests.post(url, headers=headers, json={'inputs':prompt}, timeout=60)
            r.raise_for_status()
            js = r.json()
            if isinstance(js, list) and len(js)>0:
                return js[0].get('generated_text','')
            if isinstance(js, dict):
                return js.get('generated_text', json.dumps(js))
        except Exception as e:
            print('HF text call failed', e)
    return json.dumps({
        'title':'AI Productivity Hacks',
        'linkedin_post':'Use AI to automate repetitive work...',
        'x_post':'AI + automation = productivity',
        'ig_carousel':['Slide 1','Slide 2','Slide 3','Slide 4','Slide 5'],
        'yt_script':'Short script about AI productivity...',
        'hashtags':['#AI','#productivity']
    })
