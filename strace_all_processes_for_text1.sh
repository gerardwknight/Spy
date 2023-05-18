#!/bin/bash

# Cleanup
rm -f *strace_output*.txt

# Get the list of process IDs
pids=$(pgrep -f "")

# Start strace on all processes
for pid in $pids; do
  echo "Tracing PID: $pid"
  strace -e trace=open,read,write -s 500 -y -f -p "$pid" 2>&1 | grep '/dev/bus/usb' > "$pid-strace_output_$pid.txt" &
done

# Wait for a key press
read -n 1 -s -r -p "Press any key to stop strace..."

# Kill the strace processes
pkill -f "strace -e trace=open,read,write"

# Wait for all background strace processes to finish
wait

# List files size > 0 and put them into a list
file_list=()
while IFS= read -r -d '' file; do
  file_list+=("$file")
done < <(find . -type f -size +0c -name "*strace_output*" -print0)

# Cat each file in the list
for file in "${file_list[@]}"; do
  echo "Contents of $file:"
  cat "$file"
  echo "----------------------------------------"
done

# Exit the script
exit

