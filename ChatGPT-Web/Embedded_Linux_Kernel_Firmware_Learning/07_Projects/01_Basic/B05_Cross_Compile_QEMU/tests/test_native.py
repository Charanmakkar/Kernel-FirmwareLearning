import subprocess
for n in [0,1,10,1000000]:
    p=subprocess.run(['./build/target_sum_native',str(n)],check=True,capture_output=True,text=True)
    assert f'sum={n*(n+1)//2}\n' in p.stdout,p.stdout
for n in ['-1','1000001','abc','99999999999999999999999999']:
    assert subprocess.run(['./build/target_sum_native',n],capture_output=True).returncode==2
print('PASS native reference: zero/max sum and malformed/overflow arguments; no cross/QEMU claim')
