from ast import For
import subprocess
import json

def exec(cmd):
    cmd = subprocess.check_output(cmd, shell=True)
    cmd = json.loads(cmd)

    return cmd


def load_json():
    # Opening JSON file
    f = open('config.json',)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    return data

def generate_cmd(data):
    cmd = ""
    for dt in data:
        if isinstance(data[dt], str):
            cmd += " --" + dt + " " + data[dt]

        elif isinstance(data[dt], list):
            cmd += " --" + dt
            for dt_list in data[dt]:
                cmd += " " + dt_list + "\n"

        elif isinstance(data[dt], bool):
            cmd += " --" + dt
            if data[dt]:
                cmd += ' true'
            else:
                cmd += ' false'

        elif isinstance(data[dt], dict):
            for opt in data[dt].keys():
                print(data[dt][opt])
                if isinstance(data[dt][opt], str):
                    cmd += " --" + dt + " " + data[dt]

                elif isinstance(data[dt][opt], list):
                    print('test')
                    cmd += " --" + dt
                    for dt_list in data[dt]:
                        cmd += " " + dt_list + "\n"

                elif isinstance(data[dt][opt], bool):
                    cmd += " --" + dt
                    if data[dt]:
                        cmd += ' true'
                    else:
                        cmd += ' false'

test = load_json()

generate_cmd(test['group'][0])
