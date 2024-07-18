# coding=utf-8
import re
import subprocess
import os
import time

import click
import logging

import rich
from rich.logging import RichHandler
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from utils.utils import insert_before_line as before, insert_after_line as after, replace_line as replace

os.system("clear")
console = Console(record=True)
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(console=console, omit_repeated_times=False, show_path=False, enable_link_path=False, rich_tracebacks=False,
                    tracebacks_show_locals=True,
                    tracebacks_suppress=[click])],
)

log = logging.getLogger("rich")
thistime = str(time.strftime("%Y%m%d%H%M", time.localtime()))


def check_system_support():
    """
    Check if the current system is supported.
    """
    with open('/etc/os-release', 'r') as f:
        flag = False
        for line in f:
            if "ROCKY" in line.upper() or "CENTOS" in line.upper():
                flag = True
                break
        if not flag:
            print("系统不支持")
            exit(0)


check_system_support()

# try:
#     subprocess.check_call(["ansible", "--version"])
# except OSError:
#     """
#     安装 ansible、setuptools
#     """
#     subprocess.call(["tar", "-xzvf", "Docker/rpm/ansible_rpm.tar.gz", "-C", "Docker/rpm/"])
#     os.system("rpm -Uvh Docker/rpm/ansible_rpm/*.rpm --force")
#     subprocess.check_call(["ansible", "--version"])

"""
安装密钥免密
"""
# try:
#     os.system("rm -f /root/.ssh/baseline*")
#     subprocess.call("ssh-keygen -b 2048 -t rsa -f /root/.ssh/baseline -q -N ''", shell=True)
#     os.system("cat /root/.ssh/baseline.pub >> /root/.ssh/authorized_keys")
#     os.system("cat /root/.ssh/baseline.pub >> /TRS/baseline/venv/env/ssh_key")
#     content = """
#     Host localhost
#         StrictHostKeyChecking no
#         UserKnownHostsFile=/dev/null
#         PubkeyAuthentication yes
#     """
#     with open("/root/.ssh/config", "w") as f:
#         f.write(content)
# except OSError:
#     pass

"""
创建备份目录、审计日志目录
"""
os.system("mkdir -p /TRS/baseline/backup")
os.system("mkdir -p /var/log/.history")

console.rule("用户安全", align="left")
try:
    pam = subprocess.check_call(["rpm", "--quiet", "-q", "pam"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    log.info("[*] 不允许用户重复使用最近的密码")
    f = open('/etc/pam.d/system-auth', 'r+')
    with open('/etc/pam.d/system-auth', 'r') as systemauth:
        start, end, incorrect, index, presence, correct = 0, 0, 0, 0, False, False
        pattern_presence = re.compile(r"^\s*password\s+(?:(?:requisite)|(?:required))\s+pam_pwhistory\.so.*$")
        pattern_correct = re.compile(r"^\s*password\b.*\bpam_pwhistory\.so\b.*\bremember=([0-9]*).*$")
        for line in systemauth:
            if presence is True and correct is True:
                break
            index += 1
            # find first line
            if line.startswith("password") and start == 0:
                start = index
            # find end line
            if line.startswith("password") and "pam_deny.so" in line and end == 0:
                end = index
            if pattern_presence.match(line):
                presence = True
            if pattern_correct.match(line):
                correct = True
        pass
        if presence is False:
            log.warning("[-] 未找到 pam_pwhistory.so！")
        if presence is True and correct is False:
            log.warning("[-] 找到 pam_pwhistory.so，但是配置不正确")
            pass
        else:
            log.info("[-] pam_unix2.so 已经设置了 remember 参数")

except subprocess.CalledProcessError:
    pass

"""
供应商安全
"""
console.rule("软件供应链安全", align="left")
ssh = subprocess.run("ssh -V", shell=True, capture_output=True, text=True)
print(ssh.stderr)
"""
用户安全
"""
console.rule("用户安全", align="left")
log.info("[-] 锁定或者删除多余的系统账户以及创建低权限用户")
try:
    defaultuser = ["root", "bin", "daemon", "adm", "lp", "sync", "shutdown", "halt", "mail", "operator", "games", "ftp",
                   "nobody",
                   "systemd-network", "dbus", "polkitd", "sshd", "postfix", "chrony", "ntp", "rpc", "rpcuser",
                   "nfsnobody"]
    with open('/etc/passwd', 'r') as passwd:
        for line in passwd:
            parts = line.split(":")
            if len(parts) < 1:
                continue
            uu = parts[0]
            if uu not in defaultuser:
                log.info("%s 非默认用户" % uu)
                try:
                    subprocess.run(["usermod", "-L", uu], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.run(["usermod", "-s", "/sbin/nologin", uu], stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError as e:
                    log.error("Failed to execute usermod command: %s" % e)
except FileNotFoundError as e:
    log.error("Failed to open /etc/passwd: %s" % e)
except PermissionError as e:
    log.error("Failed to read /etc/passwd: %s" % e)

log.info("[-] 配置满足策略的root管理员密码")


console.save_html('opslogs.html')
