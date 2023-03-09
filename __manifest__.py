{
    'name': 'Travel Management',
    'sequence': 1,
    'version': '16.0.1.0.0',
    'depends': ['base', 'mail', 'account', 'sale','website'],

    'data':  ['security/group.xml',
              'security/ir.model.access.csv',
              'view/travel_views.xml',
              'data/facilities.xml',
              'data/website_menu.xml',
              'view/vehicle_page.xml',
              'view/estimation.xml',
              'view/facilities.xml',
              'view/estimation_amount.xml',
              'reporting/reporting.xml',
              'reporting/reporting.xml',
              'wizard/travel_reporting_wizard.xml',
              'view/website_template.xml',
              'view/travel_view_home.xml',
              'view/snippet.xml',
              # 'view/snippet_template.xml',
              'view/qweb_snippet.xml',
              'view/travel_management_menu.xml',
              ],
    # 'web.assets_qweb': [
    #     'static/src/xml/snippet_template.xml'
    #   ],

    'assets': {
        'web.assets_backend': [
            'travel_management/static/src/js/travels_management.js',
        ],
        'web.assets_frontend': [
            'travel_management/static/src/xml/snippet_template.xml',
            'travel_management/static/src/js/website.js',
            'travel_management/static/src/js/snippet.js',
            'travel_management/static/src/css/icon.scss',

        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,

}
