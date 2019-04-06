import os
import pathlib

vars = {}

with open(".env", "r") as env_file:
    for line in env_file.readlines():
        line = line.split('#')[0]
        if '=' in line:
            var, val = line.split('=')
            vars[var.strip()] = val.strip()

for service in ('zcash', 'mongo', 'postgres', 'task_results'):
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

with open(".env", "w") as env_file:
    env_file.write("".join(["{}={}\n".format(k, v) for k, v in vars.items()]))
    env_file.write('\n')
