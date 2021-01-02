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

crystal_material_choices = [
    ('TiSa', 'Ti:Sa'),
    ('BBO', 'BBO'),
    ('KDP', 'KDP'),
    ('KTP', 'KTP')
]

# Pre-defined items organised by group of elements
# TODO :
# 'Optics':['Beamsplitters', 'Diffusers', 'Filters',
#              'Gratings', 'Lenses', 'Mirrors', 'Objective lenses',
#              'Polarizers', 'Prisms', 'Reticles', 'Windows'
#             ]
choices = {
    'choose a type':'choose a subtype',
    'Optics':['Crystals', 'Mirrors', 'Windows']           
        }

get_search_fields = {
    'base': {'manufacturer':'Manufacturer', 'part_number':'Part number', 'description':'Description'},
    'mirrors' : {'diameter':'Diameter', 'coating':'Coating', 'curvature':'Curvature'},
    'windows' : {'diameter':'Diameter', 'thickness':'Thickness', 'coating':'Coating'},
    'crystals': {'width':'Width', 'height':'Height', 'thickness':'Thickness', 'material':'Material',
                 'coating':'Coating'}
}

non_str_fields = {
    'float':['diameter', 'curvature', 'width', 'height', 'thickness']
}