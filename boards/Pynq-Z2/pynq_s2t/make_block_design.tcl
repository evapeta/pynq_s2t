set overlay_name "block_design"
set design_name "pynq_s2t"
set iprepo_dir ./../../../PYNQ/boards/ip

# Create project
create_project ${overlay_name} ./${overlay_name} -part xc7z020clg400-1
set_property target_language VHDL [current_project]

# Set IP repository paths
set_property ip_repo_paths $iprepo_dir [current_project]
update_ip_catalog

# Add constraints
add_files -fileset constrs_1 -norecurse ./constraints.xdc

# Make block design
source ./${design_name}.tcl
