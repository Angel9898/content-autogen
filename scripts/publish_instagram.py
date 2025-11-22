"""Instagram publish via Graph API container flow. IMAGE_HOSTING_URL is required if files are not public.
"""
import os, sys, json, requests
IG_USER = os.getenv('IG_USER_ID'); TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN'); IMAGE_HOST = os.getenv('IMAGE_HOSTING_URL')
if os.getenv('SELF_TEST','false').lower()=='true' or os.getenv('DRY_RUN','true').lower()=='true':
    print('[DRY] Instagram publish simulated'); sys.exit(0)
if not (IG_USER and TOKEN): print('Missing IG credentials'); sys.exit(1)
assets_dir = sys.argv[1] if len(sys.argv)>1 else 'assets'
images = sorted([os.path.join(assets_dir,'images',f) for f in os.listdir(os.path.join(assets_dir,'images')) if f.endswith('.png') or f.endswith('.jpg')])
if not images: print('No images'); sys.exit(1)
container_ids = []
for img in images:
    if IMAGE_HOST:
        with open(img,'rb') as fh:
            r = requests.post(IMAGE_HOST, files={'file':fh}, timeout=60); r.raise_for_status(); image_url = r.json().get('url')
    else:
        print('Provide IMAGE_HOSTING_URL to upload images and get public URLs'); sys.exit(1)
    resp = requests.post(f'https://graph.facebook.com/v17.0/{IG_USER}/media', params={'image_url':image_url,'access_token':TOKEN}, timeout=30)
    resp.raise_for_status(); cid = resp.json().get('id'); container_ids.append(cid); print('Created container', cid)
pub = requests.post(f'https://graph.facebook.com/v17.0/{IG_USER}/media_publish', params={'children':','.join(container_ids),'access_token':TOKEN}, timeout=30)
pub.raise_for_status(); print('Published', pub.json())
