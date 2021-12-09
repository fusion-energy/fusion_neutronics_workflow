


rm *.jou *.json *.out *.xml *.exo *.h5m *.vtk *.log *.h5
rm -rf stage_1_output/
rm -rf stage_2_output/

python 1_create_cad_and_convert_to_dagmc.py

# needed to prevent hdf5 conflict if using cad-to-h5m
# export HDF5_DISABLE_VERSION_CHECK=1

python 2_run_neutronics_simulation.py

python 3_post_process_and_plot.py
