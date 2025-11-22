import os, sys, subprocess
assets = sys.argv[1] if len(sys.argv)>1 else 'assets'
out = sys.argv[2] if len(sys.argv)>2 else os.path.join(assets,'video_post.mp4')
imgdir = os.path.join(assets,'images')
if not os.path.exists(imgdir): print('No images'); raise SystemExit(1)
slides = sorted([os.path.join(imgdir,f) for f in os.listdir(imgdir) if f.endswith('.png')])
with open(os.path.join(assets,'inputs.txt'),'w') as f:
    for s in slides:
        f.write(f"file '{s}'\nduration 3\n")
    f.write(f"file '{slides[-1]}'\n")
tmp = os.path.join(assets,'temp_slideshow.mp4')
subprocess.check_call(['ffmpeg','-y','-f','concat','-safe','0','-i',os.path.join(assets,'inputs.txt'),'-vf','scale=1080:1920,format=yuv420p','-r','30',tmp])
audio = os.path.join(assets,'audio.mp3')
if os.path.exists(audio) and os.path.getsize(audio)>0:
    subprocess.check_call(['ffmpeg','-y','-i',tmp,'-i',audio,'-c:v','libx264','-c:a','aac','-shortest',out])
else:
    subprocess.check_call(['ffmpeg','-y','-i',tmp,'-c:v','libx264','-an',out])
print('Video assembled', out)
