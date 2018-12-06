import subprocess

from utils import RPC
import subprocess


ps = subprocess.Popen(["/sbin/ip",  "route"], stdout=subprocess.PIPE)
output = subprocess.check_output(['awk', '/default/ { print $3 }'], stdin=ps.stdout, stderr=ps.stderr)
ps.wait()
output = output.decode("utf-8").strip()
print(output)


zcash_url = 'http://{}:8232'.format(output)
print(zcash_url)

zcash = RPC(zcash_url, 'user', 'pass')

print(zcash.getbestblockhash())
