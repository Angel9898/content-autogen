import os, subprocess, sys
SELF_TEST = os.getenv('SELF_TEST','false').lower()=='true'
DRY = os.getenv('DRY_RUN','true').lower()=='true'
def run(cmd):
    print('Running:', ' '.join(cmd)); subprocess.check_call(cmd)
if __name__ == '__main__':
    run(['python','scripts/generate_text.py'])
    run(['python','scripts/generate_images.py','assets/content.json'])
    run(['python','scripts/generate_audio.py','assets/content.json','assets/audio.mp3'])
    run(['python','scripts/assemble_video.py','assets','assets/video_post.mp4'])
    if SELF_TEST:
        print('[SELF_TEST] Validating payloads')
        from helpers.validate_payloads import validate_all_payloads
        validate_all_payloads(); print('[SELF_TEST] OK'); sys.exit(0)
    if DRY:
        os.environ['DRY_RUN']='true'
    run(['python','scripts/publish_youtube.py','assets/video_post.mp4'])
    run(['python','scripts/publish_instagram.py','assets'])
    run(['python','scripts/publish_linkedin.py','assets'])
    run(['python','scripts/publish_x.py','assets/content.json'])
    print('Publish attempts complete')
