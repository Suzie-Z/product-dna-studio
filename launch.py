"""Initialize a mounted disk, then run the app without root privileges."""
import os,pwd,runpy
from pathlib import Path
if os.getuid()==0:
    user=pwd.getpwnam('studio')
    disk=Path(os.environ.get('DNA_DATA_DIR','/data'))
    disk.mkdir(parents=True,exist_ok=True)
    os.chown(disk,user.pw_uid,user.pw_gid)
    os.setgroups([])
    os.setgid(user.pw_gid)
    os.setuid(user.pw_uid)
runpy.run_path('/app/server.py',run_name='__main__')
