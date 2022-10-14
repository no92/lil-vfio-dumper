#!/bin/bash
# Usage: ./qemu-launch.sh <path-to-vbios> <bootable linux iso>

qemu-system-x86_64 -enable-kvm -serial file:/dev/stdout \
-device vfio-pci,host=00:02.0,romfile=$1 -vga none -nographic \
-m 2048 -M pc -cpu host -global PIIX4_PM.disable_s3=1 -global PIIX4_PM.disable_s4=1 -machine kernel_irqchip=on \
-cdrom $2 \
--trace "vfio*"
