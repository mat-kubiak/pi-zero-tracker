cd pi-zero-tracker
if [ -f "beacon_data.txt" ]; then
    echo '' >> "archive.txt"
    cat "beacon_data.txt" >> "archive.txt"
    rm -f "beacon_data.txt"
fi
sudo python3 tracker.py -d 120 -w 'iNode_Bacon' -m -s ','