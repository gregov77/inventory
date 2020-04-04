type_choices = [
    ('None', 'Choose a type'),
    ('Optics', 'Optics')
]

coating_choices = [
    ('dielectric', 'Dielectric'),
    ('al', 'Aluminium'),
    ('ag', 'Silver'),
    ('uncoated', 'Uncoated')
]

choices = {
    'choose a type':'choose a subtype',
    'Optics':['Beamsplitters', 'Diffusers', 'Filters',
              'Gratings', 'Lenses', 'Mirrors', 'Objective lenses',
              'Polarizers', 'Prisms', 'Reticles', 'Windows'
             ]           
        }

get_search_fields = {
    'base': {'manufacturer':'Manufacturer', 'part_number':'Part number', 'description':'Description'},
    'mirrors' : {'diameter':'Diameter', 'coating':'Coating', 'curvature':'Curvature'}
}

non_str_fields = {
    'float':['diameter', 'curvature']
}