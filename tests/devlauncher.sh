#!/bin/bash

session="openattribution"

sudo ./launcher.sh

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
	# First Window
	## Initial: Top Left
	tmux send-keys -t $session "cd apps/dash && npm run dev" Enter
	## Top Right
	tmux split-window -h -t $session
	tmux send-keys -t $session "sudo tail -f /var/log/clickhouse-server/clickhouse-server.log" Enter
	## Bottom Right
	tmux split-window -v -p 50 -t $session
	tmux send-keys -t $session "sudo tail -f /var/log/clickhouse-server/clickhouse-server.err.log" Enter
	## Bottom Left
	tmux select-pane -t $session:0.0
	tmux split-window -v -p 50 -t $session
	tmux send-keys -t $session "source ~/venv/open-attribution-env/bin/activate && python run_data_generation.py" Enter
	# Second Window
	## Initial: Top
	tmux new-window -t $session
	tmux send-keys -t $session "source ~/venv/open-attribution-env/bin/activate && python run_data_generation.py -i" Enter
	## Bottom
	#tmux split-window -v -t $session
	# Put cursor back on first pane
	#tmux select-pane -t $session:0.0
else
	echo "Attach existing new session"
fi

tmux att -t $session
