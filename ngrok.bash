#!/bin/bash
# grabs the PID for the current running ngrok
ngrok_pid=$(pgrep ngrok)
echo $ngrok_pid

echo "Current ngrok PID = ${ngrok_pid}"
if [ "$ngrok_pid" == 1 ]; then
  # kills ngrok
  kill_ngrok_pid=$(kill -9 $ngrok_pid)
else
  echo "ngrok is running"
fi
# get exit status code for last command
check=$?
echo $check
# check if the exit status returned success
if [ $check -eq 0 ]; then
    # re-start ngrok

    # shellcheck disable=SC2034
    new_ngrok=$(ngrok http 8000 &)
    echo new_ngrok
    # do more checks below...
else
    echo "NO ngrok PID found"
fi

exit