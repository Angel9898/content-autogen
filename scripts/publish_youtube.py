"""YouTube upload using googleapiclient; requires YT_CLIENT_ID/SECRET and YT_REFRESH_TOKEN.
"""
import os, sys, json
if os.getenv('SELF_TEST','false').lower()=='true' or os.getenv('DRY_RUN','true').lower()=='true':
    print('[DRY] YouTube upload simulated for', sys.argv[1] if len(sys.argv)>1 else 'video'); sys.exit(0)
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except Exception as e:
    print('Google client libraries needed:', e); sys.exit(1)
CLIENT_ID = os.getenv('YT_CLIENT_ID'); CLIENT_SECRET = os.getenv('YT_CLIENT_SECRET'); REFRESH = os.getenv('YT_REFRESH_TOKEN')
if not (CLIENT_ID and CLIENT_SECRET and REFRESH):
    print('Missing YouTube credentials'); sys.exit(1)
VIDEO = sys.argv[1] if len(sys.argv)>1 else 'assets/video_post.mp4'
creds = Credentials(token=None, refresh_token=REFRESH, token_uri='https://oauth2.googleapis.com/token', client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scopes=['https://www.googleapis.com/auth/youtube.upload'])
service = build('youtube','v3',credentials=creds)
meta = {}
try:
    with open('assets/content.json',encoding='utf-8') as f: meta=json.load(f)
except: pass
body = {'snippet':{'title':meta.get('title','Auto Video'),'description':meta.get('linkedin_post',''),'tags':meta.get('hashtags',[])}, 'status':{'privacyStatus':'public'}}
media = MediaFileUpload(VIDEO, chunksize=-1, resumable=True)
req = service.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
resp = None
while resp is None:
    status, resp = req.next_chunk()
    if status: print('Upload progress', int(status.progress()*100))
print('Uploaded video id', resp.get('id'))
thumb='assets/thumbnail.png'
if os.path.exists(thumb): service.thumbnails().set(videoId=resp.get('id'), media_body=MediaFileUpload(thumb)).execute(); print('Thumbnail uploaded')
