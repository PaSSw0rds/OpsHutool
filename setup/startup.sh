#!/bin/bash

function err() {
    local message="${@:-$(</dev/stdin)}"
    if [[ -n "$message" ]]; then
      printf "[%s]: \033[41;97mERROR  : %s \033[0m\n" "$(date +'%Y-%m-%dT%H:%M:%S')" "$message"
    fi
}
function info() {
    local message="${@:-$(</dev/stdin)}"
    if [[ -n "$message" ]]; then
      printf "[%s]: \033[40;38;5;82mINFO   : %s \033[0m\n" "$(date +'%Y-%m-%dT%H:%M:%S')" "$message"
    fi
}

function warn() {
    local message="${@:-$(</dev/stdin)}"
    if [[ -n "$message" ]]; then
        printf "[%s]: \033[43;30mWARNING: %s \033[0m\n" "$(date +'%Y-%m-%dT%H:%M:%S')" "$message"
    fi
}

clear
echo -e '\e[47;30m                                                                                                    \e[0m'
echo -e '\e[47;30m                                                                                  █                 \e[0m'
echo -e '\e[47;30m                                                                                  ██                \e[0m'
echo -e '\e[47;30m                                                                                  ██                \e[0m'
echo -e '\e[47;30m                                                                                  ██                \e[0m'
echo -e '\e[47;30m                                                                                 ███                \e[0m'
echo -e '\e[47;30m                                                                                 ████               \e[0m'
echo -e '\e[47;30m                                                         █                       ████               \e[0m'
echo -e '\e[47;30m          ██                                             █                      ██████              \e[0m'
echo -e '\e[47;30m         ████                                           ███                    ████████             \e[0m'
echo -e '\e[47;30m       ████████                                      █████████               ███████████            \e[0m'
echo -e '\e[47;30m     ███████████████████████████████████████████████████████████           ████████████████         \e[0m'
echo -e '\e[47;30m       ████████              ████                      █████                    ██████              \e[0m'
echo -e '\e[47;30m        ███████             ██████                      ███  ███                 ████        █      \e[0m'
echo -e '\e[47;30m        ███████  ███████████████████████████     ████████████████   ██████████████████████████████  \e[0m'
echo -e '\e[47;30m        ███████  ███████              ████████        █████████████ ████████     ███      █████████ \e[0m'
echo -e '\e[47;30m        ███████  ███████              ███████    ████  ████████████ ███████      ████     ████████  \e[0m'
echo -e '\e[47;30m        ███████  ███████              ███████    ████  █████        ███████    ████████   ████████  \e[0m'
echo -e '\e[47;30m        ███████  ███████████████████  ███████    ████  █████  ████  ██████████████████████████████  \e[0m'
echo -e '\e[47;30m        ███████  ███████              ███████    ████  █████  ████  ████████ ████████████ ████████  \e[0m'
echo -e '\e[47;30m        ███████  ███████              ███████    ████  █████  ████  ███████     ██████    ████████  \e[0m'
echo -e '\e[47;30m        ██████   ████████████████████████████    ████  █████  ████  ███████      ████     ████████  \e[0m'
echo -e '\e[47;30m       ███████   ████       ██████    ████       ████  █████  ████  ██████████████████████████████  \e[0m'
echo -e '\e[47;30m       ██████               ██████              █████  █████  ███   ███████       ██       ███████  \e[0m'
echo -e '\e[47;30m      ██████     ███████    ██████    ███████   █████  █████  █     █████        ████        █████  \e[0m'
echo -e '\e[47;30m     ██████  █████████████ ███████  ████████████████   █████                   ████████             \e[0m'
echo -e '\e[47;30m    █████   ████████        ██████        █████████    █████               ████████████████         \e[0m'
echo -e '\e[47;30m   ████      ███            ██████            ███      █████                 ████████████           \e[0m'
echo -e '\e[47;30m  █              ██         ██████         ██          █████                   ████████             \e[0m'
echo -e '\e[47;30m                            ████                       ████                     ██████              \e[0m'
echo -e '\e[47;30m                            ██                         ██                       █████               \e[0m'
echo -e '\e[47;30m                                                                                 ████               \e[0m'
echo -e '\e[47;30m                                                                                 ████               \e[0m'
echo -e '\e[47;30m                                                                                 ███                \e[0m'
echo -e '\e[47;30m                                                                                  ██                \e[0m'
echo -e '\e[47;30m                                                                                  ██                \e[0m'
echo -e '\e[47;30m                                                                                  ██                \e[0m'
echo -e '\e[47;30m                                                                                  ██                \e[0m'
echo -e '\e[47;30m                                                                                  █                 \e[0m'
echo -e '\e[47;30m                                                                                  █                 \e[0m'
echo -e '\e[47;30m                                                                                                    \e[0m'
echo -e '\e[47;30m                                                                                                    \e[0m'
cd /TRS/baseline || exit

###
### 安装基础环境
###
info "正在安装基础环境，此步骤需要YUM源支持"
yum install -y gcc perl perl-devel 2>&1 >/dev/null
yum install -y gcc openssl-devel bzip2-devel libffi-devel 2>&1 >/dev/null || exit
###
### 安装OPENSSL>=1.1
###
if [ $(openssl version | awk '{print $2}' | grep "1.1.1" | wc -l) -ne 1 ]; then
    cd /TRS/baseline/setup || exit
    info "openssl 不满足版本 >=1.1.1，开始编译安装" && sleep 2
    tar -xzf rpm/openssl-1.1.1w.tar.gz -C ./rpm && cd ./rpm/openssl-1.1.1w || exit
    ./config --prefix=/usr/local/openssl-1.1.1w --openssldir=/usr/local/openssl-1.1.1w/ssl enable-shared 2>&1 >/dev/null | warn
    make -j4 2>&1 >/dev/null | warn
    make install -j4 2>&1 >/dev/null | warn
    echo '/usr/local/openssl-1.1.1w/lib' >> /etc/ld.so.conf
    ldconfig
    mv /usr/bin/openssl{,.origin}
    cp /usr/local/openssl-1.1.1w/bin/openssl /usr/bin/openssl -af
fi
info "$(openssl version)" && sleep 1
###
### 安装PYTHON3
###
python3 -V 2>&1 >/dev/null | warn
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    cd /TRS/baseline/setup  || exit
    info "python 不满足版本 > 3.8，开始编译安装" && sleep 2
    tar -xzf rpm/Python-3.12.4.tgz -C ./rpm && cd ./rpm/Python-3.12.4 || exit
    ./configure --with-openssl=/usr/local/openssl-1.1.1w 2>&1 >/dev/null | warn
    make -j4 2>&1 >/dev/null | warn
    make install -j4 2>&1 >/dev/null | warn
    echo 'PATH=$PATH:/root/.local/bin' >> $(getent passwd root | cut -d: -f6)/.bashrc && source $(getent passwd root | cut -d: -f6)/.bashrc
    cd /TRS/baseline || exit
    pip3 config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
    cd rpm || exit
    pip3 install --no-index *.whl
    #pipx install --no-index rpm/ansible-10.1.0-py3-none-any.whl
fi
info "$(python3 -V)" && sleep 1
python3 opshutool.py
