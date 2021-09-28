# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops

# defines a simple DT neutron point source
my_source = ops.FusionPointSource(
    coordinate = (0,0,0),
    temperature = 20000.,
    fuel='DT'
)

geometry = odw.Geometry(
    h5m_filename='dagmc.h5m',
)

materials = odw.Materials(
    h5m_filename='dagmc.h5m',
    correspondence_dict={"mat1": "eurofer"}
)

tally1 = odw.TetMeshTally(
    tally_type="neutron_fast_flux",
    filename='unstructured_mesh.h5m',
)


tallies = openmc.Tallies([tally1])

settings = odw.FusionSettings()
settings.batches = 5
settings.particles = 1000
# assigns a point source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionPointSource(fuel="DT")


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)
statepoint_file = my_model.run()

odw.process_results(statepoint_file, fusion_power=1e9)
