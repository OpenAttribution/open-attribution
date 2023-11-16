#!/bin/bash

export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
export PATH="$JAVA_HOME/bin:$PATH"


app_dir=$(pwd)
echo "setting app_dir to ${app_dir}"
my_link="/etc/systemd/system/open-attribution-druid.service"


if [ -L ${my_link} ] ; then
   if [ -e ${my_link} ] ; then
      echo "Good link"
   else
      echo "Broken link"
	sudo rm ${my_link}
	sudo ln -s ${app_dir}/scripts/open-attribution-druid.service ${my_link}
   	echo "Druid service added ${my_link}"
   fi
elif [ -e ${my_link} ] ; then
   echo "Not a link"
   sudo ln -s ${app_dir}/scripts/open-attribution-druid.service ${my_link}
   echo "Druid service added ${my_link}"
else
   echo "Missing"
   sudo ln -s ${app_dir}/scripts/open-attribution-druid.service ${my_link}
   echo "Druid service added ${my_link}"
fi

sudo systemctl daemon-reload


sudo systemctl start open-attribution-druid.service

