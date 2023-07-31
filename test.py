import subprocess

# 外部コマンドを実行する関数
def execute_external_command(command):
    # パイプの処理
    if "|" in command:
        commands = command.split("|")
        processes = []

        for i, cmd in enumerate(commands):
            if not "awk" in cmd:
                cmd = cmd.split()
            if i == 0:
                pc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', timeout=3)
                processes.append(pc)
                print(pc.stdout)
                print(pc.stderr)
            else:
                pc = subprocess.run(cmd, stdin=processes[-1].stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', timeout=3)
                processes.append(pc)
                print(pc.stdout)
                print(pc.stderr)
    else:
        pc = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        print(pc.stdout)
        print(pc.stderr)

# execute_external_command("ls -")
# execute_external_command("ls static")
# execute_external_command("python3 test.py") TODO: checkをつけて途中でエラーが出たら終わらせる
# execute_external_command("ps | grep bash")
# execute_external_command("pwd   ")
# execute_external_command("   date")
# execute_external_command("cd ..") TODO: cdは内部コマンドだから別に処理する
# execute_external_command("ls ./*.py")
execute_external_command("ls -l | awk '{ x += $5 } END { print (x+1023) / 1024 'kB' }'")
