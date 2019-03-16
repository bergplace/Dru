
vars = {}

with open(".env", "r") as env_file:
    for line in env_file.readlines():
        line = line.split('#')[0]
        if '=' in line:
            var, val = line.split('=')
            vars[var.strip()] = val.strip()

for service in ('zcashd', 'mongo', 'postgres', 'results'):
    # this option will be overwritten if data persistence is on

    vars[service + '_volume_source'] = 'vol-' + service
    vars[service + '_volume_type'] = 'volume'

    if vars['persist_data'] == 'true' and service + '_dir' in vars:
        vars[service + '_volume_source'] = vars[service + '_dir']
        vars[service + '_volume_type'] = 'bind'

with open(".env", "w") as env_file:
    env_file.write("".join(["{}={}\n".format(k, v) for k, v in vars.items()]))
    env_file.write('\n')
