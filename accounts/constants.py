COUNTRY_CHOICES = [
    ('', 'Select Country'),
    ('Zimbabwe', 'Zimbabwe'),
    ('South Africa', 'South Africa'),
    ('Botswana', 'Botswana'),
    ('Namibia', 'Namibia'),
    ('Zambia', 'Zambia'),
    ('Malawi', 'Malawi'),
    ('Mozambique', 'Mozambique'),
    ('Lesotho', 'Lesotho'),
    ('Swaziland', 'Swaziland'),
    ('Kenya', 'Kenya'),
    ('Uganda', 'Uganda'),
    ('Tanzania', 'Tanzania'),
    ('Burundi', 'Burundi'),
    ('Rwanda', 'Rwanda'),
    ('Other', 'Other'),
]

# Structured data for logical pairing
GEOGRAPHIC_DATA = {
    'Zimbabwe': {
        'demonym': 'Zimbabwean',
        'cities': [
            'Harare', 'Bulawayo', 'Chitungwiza', 'Mutare', 'Gweru', 
            'Kwekwe', 'Kadoma', 'Masvingo', 'Chinhoyi', 'Victoria Falls',
            'Chegutu'
        ],
        'ethnicities': [
            ('Shona', 'Shona'),
            ('Ndebele', 'Ndebele'),
            ('Tonga', 'Tonga'),
            ('Shangani', 'Shangani'),
            ('Venda', 'Venda'),
            ('Kalanga', 'Kalanga'),
            ('Sotho', 'Sotho'),
        ]
    },
    'South Africa': {
        'demonym': 'South African',
        'cities': [
            'Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 
            'Port Elizabeth', 'Bloemfontein', 'Nelspruit', 'Polokwane', 
            'Sandton', 'Midrand', 'Umtata', 'Tshwane', 'East London'
        ],
        'ethnicities': [
            ('Zulu', 'Zulu'),
            ('Xhosa', 'Xhosa'),
            ('Pedi', 'Pedi'),
            ('Tswana', 'Tswana'),
            ('Sotho', 'Sotho'),
            ('Tsonga', 'Tsonga'),
            ('Swati', 'Swati'),
            ('Venda', 'Venda'),
            ('Ndebele', 'Ndebele'),
        ]
    },
    'Botswana': {
        'demonym': 'Botswanan',
        'cities': ['Gaborone', 'Francistown', 'Molepolole'],
        'ethnicities': 
        [('Tswana', 'Tswana'), 
        ('Kalanga', 'Kalanga')]
    },
    'Zambia': {
        'demonym': 'Zambian',
        'cities': ['Lusaka', 'Kitwe', 'Ndola'],
        'ethnicities': [
            ('Bemba', 'Bemba'),
            ('Lozi', 'Lozi'),
            ('Chewa', 'Chewa')
            ]
    },
    
    'Lesotho': {
        'demonym': 'Lesothan',
        'cities': ['Maseru', 'Mafikeng', 'Maseru'],
        'ethnicities': [('Basotho', 'Basotho')]
    },
    'Swaziland': {
        'demonym': 'Swati',
        'cities': ['Maseru', 'Mafikeng', 'Maseru'],
        'ethnicities': [('Basotho', 'Basotho')]
    },
    'Malawi': {
        'demonym': 'Malawian',
        'cities': ['Lilongwe', 'Blantyre', 'Chikwawa'],
        'ethnicities': [
            ('Chewa', 'Chewa'), 
            ('Ngoni', 'Ngoni'), 
            ('Chichewa', 'Chichewa'), 
            ('Ngoni', 'Ngoni'), 
            ('Chichewa', 'Chichewa')
        ]
    },
    'Kenya': {
        'demonym': 'Kenyan',
        'cities': ['Nairobi', 'Mombasa', 'Maseru'],
        'ethnicities': [
            ('Kikuyu', 'Kikuyu'), 
            ('Luhya', 'Luhya'), 
            ('Kikuyu', 'Kikuyu'), 
            ('Luhya', 'Luhya'), 
            ('Kikuyu', 'Kikuyu')
        ]
    },
    'Uganda': {
        'demonym': 'Ugandan',
        'cities': ['Kampala', 'Entebbe', 'Jinja', 'Mbarara', 'Gulu'],
        'ethnicities': [
            ('Baganda', 'Baganda'),
            ('Banyankole', 'Banyankole'),
            ('Basoga', 'Basoga'),
            ('Iteso', 'Iteso'),
            ('Bakiga', 'Bakiga')
        ]
    },
    'Tanzania': {
        'demonym': 'Tanzanian',
        'cities': ['Dar es Salaam', 'Dodoma', 'Mwanza', 'Arusha', 'Mbeya'],
        'ethnicities': [
            ('Sukuma', 'Sukuma'),
            ('Nyamwezi', 'Nyamwezi'),
            ('Chagga', 'Chagga'),
            ('Haya', 'Haya'),
            ('Ha', 'Ha')
        ]
    },
    'Burundi': {
        'demonym': 'Burundian',
        'cities': ['Gitega', 'Bujumbura', 'Ngozi', 'Rumonge'],
        'ethnicities': [
            ('Hutu', 'Hutu'),
            ('Tutsi', 'Tutsi'),
            ('Twa', 'Twa')
        ]
    },
    'Rwanda': {
        'demonym': 'Rwandan',
        'cities': ['Kigali', 'Butare', 'Gisenyi'],
        'ethnicities': [
            ('Hutu', 'Hutu'), 
            ('Tutsi', 'Tutsi'), 
            ('Twa', 'Twa')
        ]
    },
    'Namibia': {
        'demonym': 'Namibian',
        'cities': ['Windhoek', 'Walvis Bay', 'Swakopmund', 'Oshakati'],
        'ethnicities': [
            ('Ovambo', 'Ovambo'),
            ('Kavango', 'Kavango'),
            ('Herero', 'Herero'),
            ('Damara', 'Damara'),
            ('Nama', 'Nama'),
        ]
    },
    'Mozambique': {
        'demonym': 'Mozambican',
        'cities': ['Maputo', 'Matola', 'Beira', 'Nampula','Tete'],
        'ethnicities': [
            ('Makua', 'Makua'),
            ('Tsonga', 'Tsonga'),
            ('Lomwe', 'Lomwe'),
            ('Sena', 'Sena'),
        ]
    },
}

# General Fallback Choices for the Database
CITY_CHOICES = [('', 'Select City')]
for country, data in GEOGRAPHIC_DATA.items():
    for city in data['cities']:
        CITY_CHOICES.append((city, f"{city}, {country}"))

ETHNICITY_CHOICES = [
    ('', 'Select Ethnicity'),
    ('white', 'White / Caucasian'),
    ('black', 'Black'),
    ('colored', 'Colored'),
    ('indian', 'Indian'),
    ('asian', 'Asian'),
]

# Flatten all specific ethnicities into a unique list for model choices
all_specific_ethnicities = set()
for data in GEOGRAPHIC_DATA.values():
    for val, label in data['ethnicities']:
        all_specific_ethnicities.add((val, label))

ETHNICITY_CHOICES.extend(sorted(list(all_specific_ethnicities)))
