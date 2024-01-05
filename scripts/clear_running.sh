readarray -t proc_array < <(ps aux | grep python | grep sudo | grep tracker.py)
killed=0
for line in "${proc_array[@]}"
do
    owner=$(echo "$line" | awk '{print $1}')
    pid=$(echo "$line" | awk '{print $2}')
    if [[ "$owner" == "root" ]]; then
        kill "$pid"
        let "killed++"
    fi
done
echo "killed $killed processes."