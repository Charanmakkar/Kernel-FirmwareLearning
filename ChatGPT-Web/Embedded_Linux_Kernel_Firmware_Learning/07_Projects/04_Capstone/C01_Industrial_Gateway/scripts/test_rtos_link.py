#!/usr/bin/env python3
import os,pathlib,subprocess,sys,tempfile,json
firmware=pathlib.Path(__file__).resolve().parents[3]/'02_Intermediate'/'I05_RTOS_Linux'/'firmware'
if not firmware.is_file():raise SystemExit('Build I05 firmware first')
with tempfile.TemporaryDirectory() as d:
    fifo=d+'/uart';os.mkfifo(fifo);fd=os.open(fifo,os.O_RDONLY|os.O_NONBLOCK)
    sink=subprocess.Popen([sys.executable,'src/gateway.py','--state',d+'/state'],stdin=fd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    os.close(fd)
    tx=subprocess.run([str(firmware),fifo],capture_output=True,timeout=5)
    stdout,stderr=sink.communicate(timeout=5)
    if tx.returncode or sink.returncode:raise SystemExit((tx.returncode,sink.returncode,tx.stderr,stderr))
    h=json.loads(stdout);assert h['accepted']==20 and h['rejected']==0,h
    print(json.dumps({'test':'actual FreeRTOS POSIX producer -> FIFO -> gateway','accepted':h['accepted'],'rejected':h['rejected'],'status':'PASS'}))
