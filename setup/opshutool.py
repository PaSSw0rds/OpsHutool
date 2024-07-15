# coding=utf-8
import re
import subprocess
import os
import click
import logging
from rich.logging import RichHandler
from rich.console import Console

os.system("clear")
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True, tracebacks_suppress=[click])],
)

log = logging.getLogger("rich")
console = Console()


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
