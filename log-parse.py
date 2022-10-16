#!/usr/bin/env python3

import argparse

from mmio import *
from pci import *

parser = argparse.ArgumentParser()

parser.add_argument('file', type=argparse.FileType('r'), help="input file")
parser.add_argument('-p', '--pci', action='store_true', default=False)
parser.add_argument('-m', '--mmio', action='store_true', default=False)
parser.add_argument('--startline', default=0, type=int)
parser.add_argument('--endline', default=-1, type=int)

args = parser.parse_args()

if not args.pci and not args.mmio:
	args.pci = True
	args.mmio = True

i = 0

for line in args.file:
	if i < args.startline:
		pass
	if args.endline > 0 and i > args.endline:
		break

	i += 1

	if line.startswith("vfio_realize"):
		pass
	elif line.startswith("vfio_mdev"):
		pass
	elif line.startswith("vfio_get_device"):
		pass
	elif line.startswith("vfio_check_pm_reset"):
		pass
	elif line.startswith("vfio_populate_device_config"):
		pass
	elif line.startswith("vfio_region_write"):
		if args.mmio:
			parse_region_write(line)
	elif line.startswith("vfio_region_read"):
		if args.mmio:
			parse_region_read(line)
	elif line.startswith("vfio_pci_read_config"):
		if args.pci:
			parse_pci_read(line)
	elif line.startswith("vfio_pci_write_config"):
		if args.pci:
			parse_pci_write(line)
	elif line.startswith("vfio_pci_reset_flr"):
		pass
	elif line.startswith("vfio_pci_reset"):
		parse_pci_reset(line)
	elif line.startswith("vfio_check_pcie_flr"):
		pass
	elif line.startswith("vfio_intx_enable_kvm"):
		pass
	elif line.startswith("vfio_intx_disable_kvm"):
		pass
	elif line.startswith("vfio_intx_enable"):
		pass
	elif line.startswith("vfio_intx_disable"):
		pass
	elif line.startswith("vfio_intx_update"):
		pass
	elif line.startswith("vfio_msi_setup"):
		pass
	elif line.startswith("vfio_msi_enable"):
		pass
	elif line.startswith("vfio_region_setup"):
		pass
	elif line.startswith("vfio_region_mmap"):
		pass
	elif line.startswith("vfio_region_mmaps_set_enabled"):
		pass
	elif line.startswith("vfio_listener_region_add_skip"):
		pass
	elif line.startswith("vfio_listener_region_del_skip"):
		pass
	elif line.startswith("vfio_listener_region_add_ram"):
		pass
	elif line.startswith("vfio_listener_region_del"):
		pass
	elif line.startswith("qemu-system-x86_64"):
		pass
	elif line.startswith(" "):
		pass
	else:
		# print("UNKNOWN LINE: {}".format(line.strip()))
		pass
