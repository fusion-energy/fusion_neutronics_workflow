This is a minimal example that creates a multi volume CAD file in stp file
format, then converts the file to a DAGMC neutronics model, then runs an OpenMC
simulation to get a cell tally.

Run the files in this order

```bash
python 1_create_cad_and_convert_to_dagmc.py
python 2_run_neutronics_simulation.py
```
