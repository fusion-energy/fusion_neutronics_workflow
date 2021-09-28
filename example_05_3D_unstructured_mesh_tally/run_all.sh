# needed to prevent hdf5 conflict
export HDF5_DISABLE_VERSION_CHECK=1

python 1_create_cad_and_convert_to_dagmc.py

mbconvert unstructured_mesh.cub unstructured_mesh.h5m

python 2_run_neutronics_simulation.py
