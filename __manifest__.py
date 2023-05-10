{
    'name': 'Dairy',
    'depends':['base','contacts','mail','report_xlsx'],
    'author' : 'Satish Prajapati',
    'summary': 'Dairy Management',
    'sequence': -10,
    'description': """
Dairy Management
====================
Co-operative Dairy Management is a system to manage Milk Collections, Member Information, Cattle Information in a suitable way.

This system is useful to Milk Producers to check their daily collection. It can be helpful to them to monitor their collection at periodic time. They get alerts regarding collections.

At the end of the year, Milk Producers can check their yearly profits.
    """,
    'category': 'Dairy Management',
    'website': 'https://github.com/satishprajapati1/dairy',
    'data':[
        'security/ir.model.access.csv',
        'data/cattle_type_data.xml',
        'data/cattle_breed_data.xml',
        'report/report.xml',
        'views/dairy_member_views.xml',
        'views/dairy_cattle_views.xml',
        'views/dairy_collection_views.xml',
        'views/collection_rate_views.xml',
        'views/dairy_config_views.xml',
        'views/dairy_menus.xml'
    ],
    'application':True,
    'license': 'LGPL-3',
}