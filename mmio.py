from mmio_regs import *

def mmio_is_in_range(addr):
	for start, data in MMIO_RANGES.items():
		(length, name, ignore) = data
		if addr >= start and addr < (start + length):
			return (start, length, name, ignore)
	return ()

def parse_region_write(line):
	args = line.split('(')[1]
	hwaddr, data, size = args.split(',')
	hwaddr = hwaddr.replace('0000:00:02.0:region', '')
	bar, addr = hwaddr.split('+')
	addr = int(addr, 16)
	size = size.split(')')[0].strip()
	data = int(data.strip(), 16)
	if size == '8' and data == '0x7d131001':
		pass
	elif (size == '1' or size == '4') and data == '0x0':
		pass
	else:
		info = parse_region_regs(addr, data, True)
		if(addr in MMIO_REGS):
			print("MMIO write: {} (0x{:x}) = 0x{:X}{}".format(MMIO_REGS[addr], addr, data, info))
		elif bar == '0':
			mmio_range = mmio_is_in_range(addr)
			if not mmio_range:
				print("MMIO unknown write: 0x{:X} = 0x{:X} ({})".format(addr, data, size))
			else:
				if not mmio_range[3]:
					print("MMIO write: region {}+0x{:X} (0x{:X}+0x{:X}) = 0x{:X}{}".format(mmio_range[2], addr - mmio_range[0], mmio_range[0], addr - mmio_range[0], data, info))

def parse_region_read(line):
	args = line.split('(')[1]
	hwaddr, size = args.split(',')
	hwaddr = hwaddr.replace('0000:00:02.0:region', '')
	bar, addr = hwaddr.split('+')
	addr = int(addr, 16)
	size = size.split(')')[0].strip()
	data = int(args.split('=')[1].strip(), 16)
	info = parse_region_regs(addr, data, False)
	if(addr in MMIO_REGS):
		print("MMIO read: {} (0x{:x}) = 0x{:X}{}".format(MMIO_REGS[addr], addr, data, info))
	elif bar == '0':
		mmio_range = mmio_is_in_range(addr)
		if not mmio_range:
			print("MMIO unknown read: 0x{:X} = 0x{:X} ({})".format(addr, data, size))
		else:
			if not mmio_range[3]:
				print("MMIO read: region {}+0x{:X} (0x{:X}+0x{:X}) = 0x{:X}{}".format(mmio_range[2], addr - mmio_range[0], mmio_range[0], addr - mmio_range[0], data, info))

def dp_pack_aux(data, size):
    v = 0;
    if size > 4:
        size = 4

    for i in range(0, size):
        v |= (data[i]) << ((3 - i) * 8)

    return v

def dp_unpack_aux(src, data, size):
    if size > 4:
        size = 4

    for i in range(0, size):
        data[i] = (src >> ((3 - i) * 8));

ddi_aux_data = []

def parse_region_regs(addr, data, write):
	ret = []
	if addr in [0x64014, 0x64018, 0x6401C, 0x64020, 0x64024, 0x64028]:
		ddi_aux_data.append(data & 0xFF)
		ddi_aux_data.append((data >> 8) & 0xFF)
		ddi_aux_data.append((data >> 16) & 0xFF)
		ddi_aux_data.append((data >> 24) & 0xFF)
	elif addr == 0x64010:
		ret.append("Sync Pulse Count {}".format((data & 0x1F) + 1))
		ret.append("Fast Wake Sync Pulse Count {}".format(((data >> 5) & 0x1F) + 1))
		ret.append("Message size {}".format((data >> 20) & 0x1F))
		timeout_val = (data >> 26) & 0x3
		if timeout_val == 1:
			ret.append("Timeout value 600")
		elif timeout_val == 2:
			ret.append("Timeout value 800")
		elif timeout_val == 3:
			ret.append("Timeout value 1600")
		if data & 0x80000000:
			ret.append('Send Busy')
		if data & 0x40000000:
			ret.append('Done')
		if data & 0x20000000:
			ret.append('Interrupt on Done')
		if data & 0x10000000:
			ret.append('Timeout error')
		if data & 0x02000000:
			ret.append('Receive error')
		if write and ddi_aux_data:
			ret.append('\n')
			ret.append('request: {}'.format(ddi_aux_data[0] & 0xF))
		ddi_aux_data.clear()
		if ret:
			ret = ', '.join(ret)
	if ret:
		return ' ({})'.format(ret)
	else:
		return ''
