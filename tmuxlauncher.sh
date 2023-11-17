#!/bin/bash
port=$1
app=$2

session="openattribution"

WAYDROID_LOG_FILE=/var/lib/waydroid/waydroid.log

sudo systemctl stop waydroid-container.service
sudo systemctl start waydroid-container.service

if [[ -n $(pgrep tmux) ]]; then
	tmuxrunning=true
else
	tmuxrunning=false
fi

if [ "$tmuxrunning" = true ]; then
	echo "tmux already up = $tmuxrunning"
	# Check if the session exists, discarding output
	# We can check $? for the exit status (zero for success, non-zero for failure)
	#tmux has-session -t $session 2>/dev/null
	# kill session, temp
	#if [[ $? == 0 ]]; then
	if tmux has-session -t $session == 0; then
		echo "Found running tmux $session"
		dolaunchsess=false
		#tmux kill-session -t $session
	else
		dolaunchsess=true
		echo "tmux up but can't find $session"
	fi
else
	echo "tmux not open, launch new"
	dolaunchsess=true
fi

if [ "$dolaunchsess" = true ]; then
	echo "Launching new session"
	# Set up your session
	tmux new-session -d -s $session
	# Initial: Top Left
	tmux send-keys -t $session "waydroid session start" Enter
	# Top Right
	tmux split-window -h -t $session
	tmux send-keys -t $session "proxysetup.sh $port -w " Enter
	# Bottom Right
	#tmux split-window -v -p 50 -t $session
	# Bottom Left
	tmux select-pane -t $session:0.0
	tmux split-window -v -p 50 -t $session
	tmux send-keys -t $session "sleep 1" Enter
	tmux send-keys -t $session "tail -f ${WAYDROID_LOG_FILE} | grep --line-buffered 'user 0 is ready' | while read ; do check_app.sh -s  && echo 'Launch Waydroid UI..'. && waydroid app launch $app ; done" Enter
	tmux send-keys -t $session "/app-spy/check_app.sh -s $app" Enter
	# Put cursor to proxy pane which will ask for sudo
	tmux select-pane -t $session:0.2
else
	echo "Attach existing new session"
fi

tmux att -t $session
