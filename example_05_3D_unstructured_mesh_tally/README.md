#  WORK IN PROGRESS. NOT READY FOR USE AT THE MOMENT

This is a minimal example that creates a single volume CAD file in stp file
format, then converts the file to a DAGMC neutronics model and creates a tet
mesh of the volume, then runs an OpenMC simulation to get a unstrucuted mesh tally.

Run the files in this order

```bash
python 1_create_cad_and_convert_to_dagmc.py
mbconvert unstructured_mesh.cub unstructured_mesh.h5m
python 2_run_neutronics_simulation.py
```
