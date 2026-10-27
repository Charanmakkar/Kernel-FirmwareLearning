"""Run only in a disposable VM after loading the module; needs access to device."""
import errno,os,select,threading,time
device='/dev/learn_fifo'
fd=os.open(device,os.O_RDWR|os.O_NONBLOCK)
def drain():
    while True:
        try:os.read(fd,4096)
        except BlockingIOError:break
drain()
assert os.read(fd,0)==b'' and os.write(fd,b'')==0
try:os.read(fd,1);raise AssertionError('empty read did not return EAGAIN')
except BlockingIOError:pass
p=select.poll();p.register(fd,select.POLLIN|select.POLLOUT)
assert p.poll(0)[0][1]&select.POLLOUT
assert os.write(fd,b'x'*5000)==4096
assert p.poll(0)[0][1]&select.POLLIN and not p.poll(0)[0][1]&select.POLLOUT
try:os.write(fd,b'y');raise AssertionError('full write did not return EAGAIN')
except BlockingIOError:pass
assert os.read(fd,4096)==b'x'*4096
blocking=os.open(device,os.O_RDONLY);received=[]
t=threading.Thread(target=lambda:received.append(os.read(blocking,3)));t.start()
time.sleep(.05);assert t.is_alive();os.write(fd,b'abc');t.join(2)
assert not t.is_alive() and received==[b'abc'];os.close(blocking)
data=bytes(range(256))*4096;result=bytearray();failures=[]
def writer():
    try:
        w=os.open(device,os.O_WRONLY)
        try:
            pos=0
            while pos<len(data):pos+=os.write(w,data[pos:pos+10000])
        finally:os.close(w)
    except Exception as e:failures.append(e)
t=threading.Thread(target=writer);t.start();end=time.monotonic()+10
while len(result)<len(data) and time.monotonic()<end:
    try:result.extend(os.read(fd,997))
    except BlockingIOError:time.sleep(.001)
t.join(2);assert not t.is_alive() and not failures and bytes(result)==data
os.close(fd)
print('PASS zero-length; empty/full EAGAIN; partial write; poll; blocked read wake; 1 MiB ordered concurrent stream')
