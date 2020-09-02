#!/bin/python3
import json
import subprocess


print('fetching data from cmc...')
subprocess.call("./call.sh")
with open('temp.json', 'r') as f:
    temp_list = json.load(f)['data']

print('writing formatted data...')
D = {}
for asset in temp_list:
    D[asset['symbol']] = asset
with open('cmc_by_symbol.json', 'w') as f:
    json.dump(D, f)


subprocess.call("rm temp.json", shell=True)
print('done')
