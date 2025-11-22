import os, sys, subprocess
if len(sys.argv)>1 and sys.argv[1]=='self_test': os.environ['SELF_TEST']='true'
subprocess.check_call(['python','scripts/publish_all.py'])
