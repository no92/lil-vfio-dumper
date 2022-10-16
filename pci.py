PCI_CONFIG = {
	(0x00, 2): 'Vendor ID',
	(0x02, 2): 'Device ID',
	(0x00, 4): 'Vendor & Device ID',
	(0x04, 2): 'Command',
	(0x06, 2): 'Status',
	(0x08, 1): 'Revision',
	(0x08, 4): 'Class Code & Revision',
	(0x0A, 2): 'Class & Subclass',
	(0x0C, 1): 'Cache Line Size',
	(0x0E, 1): 'Header Type',
	(0x10, 4): 'BAR0',
	(0x14, 4): 'BAR1',
	(0x18, 4): 'BAR2',
	(0x1C, 4): 'BAR3',
	(0x20, 4): 'BAR4',
	(0x24, 4): 'BAR5',
	(0x2C, 2): 'Subsystem Vendor ID',
	(0x2E, 2): 'Subsystem ID',
	(0x30, 4): 'Expansion ROM base address',
	(0x34, 1): 'Capabilities Pointer',
	(0x3C, 1): 'Interrupt Line',
	(0x3D, 1): 'Interrupt Pin',
	(0x40, 2): 'Capability Identifier',
	(0x50, 2): 'Mirror of GMCH Graphics Control MGGC0 Register',
	(0x5C, 4): 'Base Data of Stolen Memory',
	(0x70, 2): 'PCI Express Capability Header',
	(0x72, 2): 'PCI Express Capability',
	(0x74, 4): 'PCI Express Device Capabilities',
	(0x78, 2): 'PCI Express Device Control',
	(0x94, 4): 'Message Address',
	(0xAC, 2): 'Message Signaled Interrupts Capability ID',
	(0xAE, 2): 'Message Signaled Interrupt control',
	(0xB0, 4): 'Base Data of Stolen Memory',
	(0xB4, 2): 'Base of GTT Stolen Memory',
	(0xD0, 2): 'Power Management Capabilities ID',
	(0xD2, 2): 'Power Management Capabilities',
	(0xD4, 2): 'Power Management Control/Status',
	(0xFC, 4): 'ASL Storage',
}

def parse_pci_read(line):
	args = line.split('(')[1]
	params = args.split(',')
	offset = int(params[1].replace('@', ''), 16)
	bytes_read = int(params[2].split('=')[1].split(')')[0], 16)
	data = int(args.split()[-1], 16)

	if (offset, bytes_read) in PCI_CONFIG:
		info = parse_config_regs(offset, data)
		print("PCI read: {} (0x{:X}, size {}) = 0x{:X}{}".format(PCI_CONFIG[(offset, bytes_read)], offset, bytes_read, data, info))
	else:
		print("PCI read: <unknown> (0x{:X}, size {}) = 0x{:X}".format(offset, bytes_read, data))

def parse_pci_write(line):
	args = line.split('(')[1]
	params = args.split(',')
	offset = int(params[1].replace('@', ''), 16)
	data = int(params[2], 16)
	bytes_read = int(params[3].split('=')[1].split(')')[0], 16)

	if (offset, bytes_read) in PCI_CONFIG:
		info = parse_config_regs(offset, data)
		print("PCI write: {} (0x{:X}, size {}) = 0x{:X}{}".format(PCI_CONFIG[(offset, bytes_read)], offset, bytes_read, data, info))
	else:
		print("PCI write: <unknown> (0x{:X}, size {}) = 0x{:X}".format(offset, bytes_read, data))

def parse_pci_reset(line):
	args = line.split('(')[1].split(')')[0].strip()
	assert(args == '0000:00:02.0')
	print("PCI reset: {}".format(args))

def parse_config_regs(offset, data):
	ret = []
	if offset == 0x04:
		if data & 0x1:
			ret.append('I/O Enable')
		if data & 0x2:
			ret.append('Memory Access Enable')
		if data & 0x4:
			ret.append('Bus Master Enable')
		if data & 0x400:
			ret.append('Interrupt Disable')
		if ret:
			ret = ', '.join(ret)
	if ret:
		return ' ({})'.format(ret)
	else:
		return ''
