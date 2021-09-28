python stage_1_create_cad.py


rm *.jou *.json *.out *.xml *.exo *.h5m *.vtk *.log *.h5
rm -rf stage_1_output/
rm -rf stage_2_output/


python stage_1_create_cad.py

# needed to prevent hdf5 conflict
export HDF5_DISABLE_VERSION_CHECK=1

python stage_2_convert_cad_to_neutronics.py

mbconvert stage_2_output/unstructured_mesh.cub stage_2_output/unstructured_mesh.h5m

python stage_3_run_neutronics_simulation.py