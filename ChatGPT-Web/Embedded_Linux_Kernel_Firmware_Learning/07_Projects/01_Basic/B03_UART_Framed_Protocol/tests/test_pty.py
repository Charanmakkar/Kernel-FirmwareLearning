import os, pty, select, signal, struct, subprocess, threading, time, termios, pathlib
EXE=str(pathlib.Path('build/uart_frame').resolve())
def crc(data):
    c=0xffff
    for x in data:
        c^=x<<8
        for _ in range(8):c=((c<<1)^0x1021 if c&0x8000 else c<<1)&0xffff
    return c
def frame(payload,typ=2,seq=1):
    body=struct.pack('>BBHH',1,typ,len(payload),seq)+payload
    return b'\xa5\x5a'+body+struct.pack('>H',crc(body))
def trial(mode,payload=b'hello'):
    master,slave=pty.openpty();name=os.ttyname(slave);before=termios.tcgetattr(slave);errors=[]
    proc=subprocess.Popen([EXE,name,payload.decode(), '300'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    def peer():
        try:
            received=b'';end=time.monotonic()+2
            while time.monotonic()<end:
                if select.select([master],[],[],0.1)[0]: received+=os.read(master,4096)
                if len(received)>=10:
                    total=10+int.from_bytes(received[4:6],'big')
                    if len(received)>=total:break
            assert received==frame(payload,1,1),(mode,received)
            if mode in ('sigterm','sigint'):
                proc.send_signal(signal.SIGTERM if mode=='sigterm' else signal.SIGINT)
                return
            if mode=='timeout':return
            response=frame(payload.upper())
            if mode=='corrupt': response=response[:-1]+bytes([response[-1]^1])
            elif mode=='resync': response=b'garbage'+frame(b'old',2,99)+frame(b'bad')[:-1]+b'\x00'+response
            # Deliberate fragmentation exercises accumulated stream parsing.
            for byte in response: os.write(master,bytes([byte]));time.sleep(0.0003)
        except Exception as exc:errors.append(exc)
    thread=threading.Thread(target=peer);thread.start()
    out,err=proc.communicate(timeout=3);thread.join(timeout=3)
    assert not thread.is_alive() and not errors,errors
    assert termios.tcgetattr(slave)==before,'terminal state not restored'
    os.close(master);os.close(slave)
    if mode in ('sigterm','sigint'):
        assert proc.returncode==128+(signal.SIGTERM if mode=='sigterm' else signal.SIGINT),err
    elif mode in ('timeout','corrupt'):assert proc.returncode==1 and b'timed out' in err,err
    else:assert proc.returncode==0 and out==payload.upper()+b'\n',(out,err)
for m in ['normal','resync','timeout','corrupt','sigterm','sigint']:trial(m)
trial('normal',b'x'*128);trial('normal',b'')
assert subprocess.run([EXE,'/dev/null','x'*129,'1'],capture_output=True).returncode==2
# Broken output pipe must also take the cleanup path instead of default SIGPIPE.
master,slave=pty.openpty();before=termios.tcgetattr(slave)
read_end,write_end=os.pipe();os.close(read_end)
p=subprocess.Popen([EXE,os.ttyname(slave),'pipe','500'],stdout=write_end,stderr=subprocess.PIPE)
os.close(write_end)
request=b'';end=time.monotonic()+2
while time.monotonic()<end and len(request)<14:
    if select.select([master],[],[],.1)[0]:request+=os.read(master,100)
assert request==frame(b'pipe',1,1)
os.write(master,frame(b'PIPE'));_,err=p.communicate(timeout=2)
assert p.returncode==1 and termios.tcgetattr(slave)==before,err
os.close(master);os.close(slave)
print('PASS fragmented PTY; noise/stale/corrupt resynchronization; bounded timeout; 0/128-byte payload; oversize rejection; terminal restore on success/error/SIGINT/SIGTERM/broken stdout pipe')
