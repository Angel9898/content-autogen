"""Publish to X (Twitter) with media upload support (OAuth1.0a flow) and v2 fallback.
"""
import os, sys, json, requests
from requests_oauthlib import OAuth1
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
BEARER = os.getenv('X_BEARER_TOKEN')
content_file = sys.argv[1] if len(sys.argv)>1 else 'assets/content.json'
with open(content_file,encoding='utf-8') as f: data=json.load(f)
text = data.get('x_post','')
media_paths = []
imgdir = os.path.join('assets','images')
if os.path.exists(imgdir):
    for fn in sorted(os.listdir(imgdir)):
        if fn.endswith('.png') or fn.endswith('.jpg'):
            media_paths.append(os.path.join(imgdir,fn)); break
if os.getenv('SELF_TEST','false').lower()=='true' or os.getenv('DRY_RUN','true').lower()=='true':
    print('[DRY] X publish simulated'); print('text=',text); print('media=',media_paths); sys.exit(0)
# Try OAuth1 with media upload
if API_KEY and API_SECRET and ACCESS and ACCESS_SECRET:
    auth = OAuth1(API_KEY, API_SECRET, ACCESS, ACCESS_SECRET)
    # chunked media upload
    upload_url = 'https://upload.twitter.com/1.1/media/upload.json'
    try:
        if media_paths:
            # INIT
            p = media_paths[0]
            total_bytes = os.path.getsize(p)
            init = requests.post(upload_url, auth=auth, data={'command':'INIT','total_bytes':total_bytes,'media_type':'image/png'})
            init.raise_for_status(); media_id = init.json()['media_id_string']
            # APPEND
            segment_id = 0
            with open(p,'rb') as fh:
                while True:
                    chunk = fh.read(4*1024*1024)
                    if not chunk: break
                    append = requests.post(upload_url, auth=auth, data={'command':'APPEND','media_id':media_id,'segment_index':segment_id}, files={'media':chunk})
                    append.raise_for_status(); segment_id += 1
            finalize = requests.post(upload_url, auth=auth, data={'command':'FINALIZE','media_id':media_id})
            finalize.raise_for_status()
            payload = {'status':text,'media_ids':media_id}
        else:
            payload = {'status':text}
        post = requests.post('https://api.twitter.com/1.1/statuses/update.json', auth=auth, data=payload)
        print('Post response', post.status_code, post.text); post.raise_for_status(); print('Posted via v1.1')
        sys.exit(0)
    except Exception as e:
        print('OAuth1 media/post failed', e)
# Fallback v2 text-only
if BEARER:
    resp = requests.post('https://api.twitter.com/2/tweets', headers={'Authorization':f'Bearer {BEARER}','Content-Type':'application/json'}, json={'text':text})
    print('v2 response', resp.status_code, resp.text)
    resp.raise_for_status(); print('Posted via v2'); sys.exit(0)
print('No credentials for X available')
