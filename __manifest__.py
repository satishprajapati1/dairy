{
    'name': 'Dairy',
    'application':True,
    'sequence':-99,
    'depends':['contacts'],
    'data':[
        'security/ir.model.access.csv',
        'views/dairy_member_views.xml',
        'views/dairy_cattle_views.xml',
        'views/dairy_collection_views.xml',
        'views/dairy_config_views.xml',
        'views/dairy_menus.xml'
    ]
}