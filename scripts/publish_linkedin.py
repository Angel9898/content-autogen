"""LinkedIn upload + UGC post implementation. Requires LI_OWNER_URN and LI_ACCESS_TOKEN.
"""
import os, sys, json, requests
TOKEN = os.getenv('LI_ACCESS_TOKEN'); OWNER = os.getenv('LI_OWNER_URN')
if os.getenv('SELF_TEST','false').lower()=='true' or os.getenv('DRY_RUN','true').lower()=='true':
    print('[DRY] LinkedIn publish simulated'); sys.exit(0)
if not (TOKEN and OWNER): print('Missing LinkedIn credentials'); sys.exit(1)
assets = sys.argv[1] if len(sys.argv)>1 else 'assets'
images = sorted([os.path.join(assets,f) for f in os.listdir(os.path.join(assets,'images')) if f.endswith('.png') or f.endswith('.jpg')])
if not images: print('No images'); sys.exit(1)
headers = {'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}
body = {"registerUploadRequest":{"owner": OWNER,"recipes":["urn:li:digitalmediaRecipe:feedshare-image"],"serviceRelationships":[{"identifier":"urn:li:userGeneratedContent","relationshipType":"OWNER"}],"supportedUploadMechanism":["SYNCHRONOUS_UPLOAD"]}}
r = requests.post('https://api.linkedin.com/v2/assets?action=registerUpload', headers=headers, json=body, timeout=30); r.raise_for_status()
val = r.json()['value']; upload_url = val['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']; asset = val['asset']
with open(images[0],'rb') as fh:
    put = requests.put(upload_url, headers={'Authorization':f'Bearer {TOKEN}','Content-Type':'application/octet-stream'}, data=fh, timeout=60); put.raise_for_status()
with open(os.path.join('assets','content.json'),encoding='utf-8') as f: content = json.load(f)
post = {"author": OWNER, "lifecycleState":"PUBLISHED", "specificContent":{"com.linkedin.ugc.ShareContent": {"shareCommentary":{"text": content.get('linkedin_post','')}, "shareMediaCategory":"IMAGE", "media":[{"status":"READY","description":{"text":""},"media":asset,"title":{"text":"Image"}}]}}, "visibility": {"com.linkedin.ugc.MemberNetworkVisibility":"PUBLIC"}}
r2 = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=post, timeout=30); r2.raise_for_status(); print('LinkedIn post created', r2.json())
