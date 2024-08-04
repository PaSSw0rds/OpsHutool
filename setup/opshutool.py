# coding=utf-8
import re
import subprocess
import os
import time

import logging

from rich import print
from rich.logging import RichHandler
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.prompt import Confirm
from utils.utils import (insert_before_line as before,
                         insert_after_line as after,
                         replace_line as replace,
                         delete_line as delete)

os.system("clear")
console = Console(record=True)
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(console=console, omit_repeated_times=False, show_path=False, enable_link_path=False,
                    rich_tracebacks=False,
                    tracebacks_show_locals=True)],
)

log = logging.getLogger("rich")
thistime = str(time.strftime("%Y%m%d%H%M", time.localtime()))


def check_system_support():
    """
    Check if the current system is supported.
    """
    with open('/etc/os-release', 'r') as os:
        flag = False
        for line in os:
            if "ROCKY" in line.upper() or "CENTOS" in line.upper():
                global SYSTEM
                SYSTEM = "REDHAT"
                flag = True
                break
        if not flag:
            print("系统不支持")
            exit(0)
        os.close()


check_system_support()

"""
创建备份目录、审计日志目录
"""
console.rule("操作审计", align="left")
os.system("mkdir -p /var/log/.history")
os.system("clear")
try:
    subprocess.check_call(["rpm", "-q", "audit"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    log.info("[×] 系统不存在audit，尝试安装……")
    try:
        subprocess.check_call(["yum", "-y", "install", "audit"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        log.error("[×] 安装audit失败！")
    exit(0)
try:
    subprocess.check_call(["auditctl", "-D"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    comm = [
        'egrep -q "max_log_file[^_].*=" {RULES_CONF} && sed -ri "s/.*max_log_file[^_].*=*/max_log_file=999/" {RULES_CONF} || echo "max_log_file=999" >> {RULES_CONF}',
        'egrep -q "max_log_file[_].*=" {RULES_CONF} && sed -ri "s/.*max_log_file[_].*=*/max_log_file_action=keep_logs/" {RULES_CONF} || echo "max_log_file_action=keep_logs" >> {RULES_CONF}'
        'echo "-w /etc/shadow -p wa -k password_change" >> {RULES_FILE}',
        'echo "-w /etc/selinux/ -p wa -k selinux_change" >> {RULES_FILE}',
        'echo "-w /sbin/insmod -p x -k module_change" >> {RULES_FILE}',
        'echo "-w /sbin/rmmod -p x -k module_change" >> {RULES_FILE}',
        'echo "-w /sbin/modprobe -p x -k module_change" >> {RULES_FILE}',
        'echo "-w /var/log/wtmp -p wa -k logins" >> {RULES_FILE}',
        'echo "-w /var/run/utmp -p wa -k sessions" >> {RULES_FILE}',
        'echo "-w /var/log/btmp -p wa -k logouts" >> {RULES_FILE}',
        'echo "-a always,exit -F arch=b64 -S execve -k commands" >> {RULES_FILE} ']
    for e in comm:
        os.system(e.format(RULES_FILE="/etc/audit/rules.d/audit.rules", RULES_CONF="/etc/audit/auditd.conf"))
except subprocess.CalledProcessError:
    log.error("[×] 安装audit失败！")
    exit(0)

console.rule("用户安全", align="left")
try:
    subprocess.check_call(["rpm", "-q", "pam"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    log.error("[×] 系统不存在PAM！")
    exit(0)

log.info("[-] 用户口令复杂性策略设置")
console.print(Markdown("""- 密码过期周期0~90
- 到期前15天提示
- 密码长度至少8
- 复杂度设置至少有一个大小写、数字、特殊字符
- 密码三次不能一样
- 尝试次数为三次)
"""))

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
