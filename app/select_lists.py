type_choices = [
    ('None', 'Choose a type'),
    ('optics', 'Optics')
]

optics_choices = [
    ('beamsplitters', 'Beamsplitters'),
    ('diffusers', 'Diffusers'),
    ('filters', 'Filters'),
    ('gratings', 'Gratings'),
    ('lenses', 'Lenses'),
    ('mirrors', 'Mirrors'),
    ('objective_lenses', 'Objective lenses'),
    ('polarizers', 'Polarizers'),
    ('prisms', 'Prisms'),
    ('reticles', 'Reticles'),
    ('windows', 'Windows')
]

coating_choices = [
    ('dielectric', 'Dielectric'),
    ('al', 'Aluminium'),
    ('ag', 'Silver'),
    ('uncoated', 'Uncoated')
]

choices = {
    'choose a type':'choose a subtype',
    'optics':['Beamsplitters', 'Diffusers', 'Filters',
              'Gratings', 'Lenses', 'Mirrors', 'Objective lenses',
              'Polarizers', 'Prisms', 'Reticles', 'Windows'
             ]           
        }

search_fields = {
    'base': {'manufacturer':'Manufacturer', 'part_number':'Part number', 'description':'Description'},
    'mirrors' : {'diameter':'Diameter', 'coating':'Coating', 'curvature':'Curvature'}
}