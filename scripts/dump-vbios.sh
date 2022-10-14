#!/bin/bash
# This script dumps an Intel iGPU's VBIOS

OUT="${1:-vbios.dump}"

echo 1 > /sys/devices/pci0000:00/0000:00:02.0/rom
cat /sys/devices/pci0000:00/0000:00:02.0/rom > "$OUT"
echo 0 > /sys/devices/pci0000:00/0000:00:02.0/rom
chmod 0777 $OUT
