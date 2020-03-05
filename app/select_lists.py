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
    ('MIRRORS', 'Mirrors'),
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
    'optics':['beamsplitters', 'diffusers', 'filters',
              'gratings', 'lenses', 'mirrors', 'objective lenses',
              'polarizers', 'prisms', 'reticles', 'windows'
             ]           
        }