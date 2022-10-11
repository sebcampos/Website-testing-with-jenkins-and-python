import os
import asyncio
import re

request_complete = False


async def get_pid():
    os.system("ps aux | grep openssl > processes.txt")
    with open("processes.txt", "r") as f:
        string = f.read()
    if "openssl" in string:
        print("heck")
        return True
    else:
        await asyncio.sleep(5)


async def ping_website():
    proc = await asyncio.create_subprocess_shell(
        "openssl s_client -connect thesensisociety.com:443",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    stdout = stdout.decode()
    if "Verify return code: 0 (ok)" in stdout:
        return True
    else:
        return False




asyncio.run(ping_website())
