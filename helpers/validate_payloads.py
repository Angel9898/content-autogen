import os,json

def validate_all_payloads():
    if not os.path.exists('assets/content.json'):
        raise AssertionError('assets/content.json missing')
    with open('assets/content.json',encoding='utf-8') as f:
        data=json.load(f)
    if 'x_post' not in data or len(data['x_post'])>280:
        raise AssertionError('x_post missing or too long')
    imgs = []
    img_dir = os.path.join('assets','images')
    if os.path.exists(img_dir):
        imgs = [p for p in os.listdir(img_dir) if p.endswith('.png') or p.endswith('.jpg')]
    if not imgs:
        raise AssertionError('No images generated in assets/images')
    if not os.path.exists(os.path.join('assets','video_post.mp4')):
        raise AssertionError('assets/video_post.mp4 missing')
    print('Payload validation OK')
