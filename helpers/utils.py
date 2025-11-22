import os, json

def load_content(path='assets/content.json'):
    if not os.path.exists(path):
        return {}
    with open(path,encoding='utf-8') as f:
        return json.load(f)

def save_json(obj, path):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(obj,f,indent=2)
