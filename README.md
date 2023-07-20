## Offline Speech-to-Text Generator
Project was a guide through embedded system design utilising PYNQ framework within the processing system of PYNQ-Z2 and implementing hardware designs upon ZYNQ-7020 programmable logic fabric. Along with student’s educational benefit, it was desired to create something novel through extending the capabilities of the video pipeline and utilising the PYNQ-framework, in a new way. Through the recent prevalence of offline communication, it was chosen to create a widening access feature of offline speech-to-text transcription. This would enable communication worldwide, while also providing security and privacy. Transcribed videos increase the viewer’s concentration and aids comprehension, further improving education. 

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
