#!/bin/bash
source ~/.bashrc
echo "切换conda环境···"
source activate py10
conda info --envs
PWD=$(realpath .)
echo "pwd: ${PWD}"
echo "安装pip依赖···"
pip install -r $(dirname "$PWD")/requirements.txt

echo "check&stop gunicorn"
sh ${PWD}/stop.sh
cd ..
echo "start gunicorn"
gunicorn main:app -c gunicorn.py


applicationDomain="http://"$(ifconfig eth0| grep 'inet'| grep -v 'inet6'|awk '{print $2}')
PORT=8003

echo "******************** checkHealth start ********************"
for i in {1..60}
do
  http_code=`curl --request GET -sL \
        -l \
        -m 1 \
        -o /dev/null \
        -w %{http_code}\
        --url "${applicationDomain}:${PORT}/py/api/health"`
  echo -e "[健康检查]code:"${http_code}
  # httpcode 200 访问成功
  if [ 200 == ${http_code} ];then
    echo -e "\033[46;30m [健康检查] 外网访问成功！ \033[0m"
    exit 0
  # httpcode 失败，最后一次检查应用本地
  elif [ 60 == ${i} ]; then
    localApplication=`ps aux | grep ${PORT} | grep -v 'grep'`
    echo "ps:" ${localApplication}
    if [ ! ${localApplication} ]; then
        echo -e "\033[5;34m [健康检查] 应用本地启动失败，外网检查失败！ \033[0m"
        echo -e "\033[5;34m [健康检查] 应用本地启动失败，外网检查失败！ \033[0m"
        exit 1
    else
        echo -e "\033[5;34m [健康检查] 本地启动成功，但外网访问失败！请根据情况排查 \033[0m"
        # timeout 30 tail -f ${LOG_DIR}
        exit 1
    fi
  fi
  sleep 1
done
echo "******************** checkHealth end ********************"