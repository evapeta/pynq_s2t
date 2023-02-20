# pynq_s2t
 Setup instruction for rebuilding the project in Vivado.

Change directory in the tcl command console.
 ```sh
 cd C:/GitHub/pynq_s2t/boards/Pynq-Z2/pynq_s2t/
 ```

Make the HLS IP in the PYNQ sub-module repository.
 ```sh
 make hls_ip
 ```

Make the project's block design.
 ```sh
 make block_design
 ```

Open the project design.
 ```sh
 open_project ./block_design/block_design.xpr
 ```

Temporary: Make the wrapper and then generate bitstream in Vivado GUI.