class scripts:
    clear_data = '''cd pi-zero-tracker
sudo rm -f beacon_data.txt archive.txt'''

    clear_running = '''readarray -t proc_array < <(ps aux | grep python | grep sudo | grep tracker.py)
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
echo "killed $killed processes."'''

    run_detach = '''cd pi-zero-tracker
if [ -f "beacon_data.txt" ]; then
    echo '' >> "archive.txt"
    cat "beacon_data.txt" >> "archive.txt"
    rm -f "beacon_data.txt"
fi
sudo python3 tracker.py -d 0 -w 'iNode_Bacon' -s ',' -dt -m -do &'''

    run_test = '''cd pi-zero-tracker
if [ -f "beacon_data.txt" ]; then
    echo "" >> "archive.txt"
    cat "beacon_data.txt" >> "archive.txt"
    rm -f "beacon_data.txt"
fi
sudo python3 tracker.py -d 10 -w "iNode_Bacon" -m -s "," -dt -m'''

    show_archive = '''cd pi-zero-tracker
cat archive.txt'''

    show_output = '''cd pi-zero-tracker
cat beacon_data.txt'''

    show_help = '''cd pi-zero-tracker
sudo python3 tracker.py -h'''

    show_running = '''readarray -t proc_array < <(ps aux | grep python | grep sudo | grep tracker.py)
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
echo "found $active active processes."'''

    update_git = '''cd pi-zero-tracker
git reset --hard HEAD
git fetch
git pull'''

    update_pip = '''sudo pip install bluepy'''

print(scripts.clear_running)