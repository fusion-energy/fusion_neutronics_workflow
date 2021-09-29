# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
# defines a simple point source
# my_source = openmc.Source()
# my_source.space = openmc.stats.Point((300, 0, 0))
# my_source.angle = openmc.stats.Isotropic()
# my_source.energy = openmc.stats.Discrete([14e6], [1])


# initialises a new source object
coverage = 10

# my_source = ops.FusionRingSource(
#     radius=900,
#     start_angle=0,
#     stop_angle=coverage*3.14159265359/180,
# )


my_source = ops.TokamakSource(
    elongation=1.557,
    ion_density_centre=1.09e20,
    ion_density_peaking_factor=1,
    ion_density_pedestal=1.09e20,
    ion_density_separatrix=3e19,
    ion_temperature_centre=45.9,
    ion_temperature_peaking_factor=8.06,
    ion_temperature_pedestal=6.09,
    ion_temperature_separatrix=0.1,
    major_radius=9.06*100,
    minor_radius=2.1*100,
    pedestal_radius=0.8 * 2.1*100,
    mode="H",
    shafranov_factor=0.44789,
    triangularity=0.270,
    ion_temperature_beta=6,
    angles=(0, coverage*3.14159265359/180)
  )

settings = openmc.Settings()
settings.source = my_source.sources
settings.batches = 60
settings.particles = int(1e4)
settings.run_mode = "fixed source"
settings.inactive = 0

h5m_filename = 'stage_2_output/dagmc.h5m'
materials = odw.Materials(
    h5m_filename=h5m_filename,
    correspondence_dict={
        'divertor_mat': 'tungsten',
        'blanket_mat': 'tungsten'
    }
)

geometry = odw.Geometry(
    h5m_filename=h5m_filename,
    reflective_angles=[0, coverage*3.14159265359/180]
)


# tally = odw.TetMeshTally('(n,Xa)', filename='stage_2_output/unstructured_mesh.h5m')
# parts/s = 312
# tally = odw.CellTally('(n,Xa)')
# parts/s = 3200
# tally = odw.TetMeshTally('(n,Xa)', filename='stage_2_output/mesh_custom.h5m')
# parts/s = 71
tally = odw.MeshTally2D(
    '(n,Xa)', plane="xz",
    bounding_box=[(800-700, -1, -700), (800+700, 1, 700)])
# parts/s = 3k

neutronics_model = openmc.Model(
    geometry=geometry,
    settings=settings,
    materials=materials,
    tallies=[tally],
)

statepoint_file = neutronics_model.run(
    # restart_file='statepoint.60.h5'
)

odw.process_results(statepoint_file, fusion_power=1e9)
