readarray -t proc_array < <(ps aux | grep python | grep sudo | grep tracker.py)
active=0
for line in "${proc_array[@]}"
do
    owner=$(echo "$line" | awk '{print $1}')
    pid=$(echo "$line" | awk '{print $2}')
    if [[ "$owner" == "root" ]]; then
        echo "$line"
        let "active++"
    fi
done
echo "found $active active processes."