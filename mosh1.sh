#sh mosh1.sh ssh_ip ssh_port
host=$1
port=$2
remote_ip=`host $host | awk '/has address/ { print $4 ; exit }'` #remote ip
info=`ssh -p $port zdb@$host -t "mosh-server" | grep 'MOSH CONNECT' | sed  's/MOSH CONNECT//g' | tr -d '\r\n'`
read -a port_key <<< "${info}"
port=${port_key[0]}
key=${port_key[1]}

echo "///$port///"
echo "///$key///"
MOSH_KEY=$key ./mosh-client $remote_ip $port
