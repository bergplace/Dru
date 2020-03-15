import os
import pathlib

vars = {}

with open(".env", "r") as env_file:
    for line in env_file.readlines():
        line = line.split('#')[0]
        if '=' in line:
            var, *val = line.split('=')
            val = '='.join(val)
            vars[var.strip()] = val.strip()

for service in ('zcash', 'mongo', 'postgres', 'task_results', 'rabbit'):
    if service + '_dir' in vars:
        path = os.path.expanduser(vars[service + '_dir'])
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        vars[service + '_volume_source'] = path
        vars[service + '_volume_type'] = 'bind'
    else:
        vars[service + '_volume_source'] = 'tmp-vol-' + service
        vars[service + '_volume_type'] = 'volume'

if vars['use_docker_zcash_node'] == 'true':
    vars['cryptocurrency_host'] = 'zcashd'
else:
    vars['cryptocurrency_host'] = ''

vars['web_port'] = '8000' if vars['debug'] == 'true' else '80'

if 'web_ssl_key_path' not in vars:
    vars['web_ssl_key_path'] = './web/conf/placeholder.key'

if 'web_ssl_cert_path' not in vars:
    vars['web_ssl_cert_path'] = './web/conf/placeholder.cert'

with open(".env", "w") as env_file:
    env_file.write("".join(["{}={}\n".format(k, v) for k, v in vars.items()]))
    env_file.write('\n')
