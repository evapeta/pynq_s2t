all: hls_ip block_design bitstream clean

hls_ip:
	vivado -mode batch -source make_hls_ip.tcl -notrace

block_design:
	vivado -mode batch -source make_block_design.tcl -notrace

bitstream:
	vivado -mode batch -source make_bitstream.tcl -notrace

clean:
	rm -rf block_design *.jou *.log NA .Xil
