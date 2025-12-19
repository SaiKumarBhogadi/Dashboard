ROLE_PERMISSIONS = {
    'super_admin': {
        'dashboard': {'view': True},
        'users': {'view': True, 'create': True, 'edit': True, 'delete': True, 'export': True},
        'biodata': {'view': True, 'create': True, 'edit': True, 'delete': True, 'export': True},
        'training': {'view': True, 'create': True, 'edit': True, 'delete': True, 'export': True},
        'projects': {'view': True, 'create': True, 'edit': True, 'delete': True, 'export': True},
    },

    'admin': {
         'dashboard': {'view': True},
        'users': {'view': True, 'create': False, 'edit': False, 'delete': False, 'export': True},
        'biodata': {'view': True, 'create': True, 'edit': True, 'delete': True, 'export': True},
        'training': {'view': True, 'create': True, 'edit': True, 'delete': True, 'export': True},
        'projects': {'view': True, 'create': True, 'edit': True, 'delete': True, 'export': True},
    },

    'scrum_master': {
         'dashboard': {'view': True},
        'users': {'view': True, 'create': False, 'edit': False, 'delete': False, 'export': True},
        'biodata': {'view': True, 'create': False, 'edit': False, 'delete': False, 'export': True},
        'training': {'view': True, 'create': False, 'edit': False, 'delete': False, 'export': True},
        'projects': {'view': True, 'create': False, 'edit': False, 'delete': False, 'export': True},
    },

    'trainer': {
         'dashboard': {'view': True},
        'users': {'view': True, 'create': True, 'edit': False, 'delete': True, 'export': True},
        'biodata': {'view': True, 'create': False, 'edit': False, 'delete': False, 'export': True},
        'training': {'view': True, 'create': False, 'edit': False, 'delete': False, 'export': True},
        'projects': {'view': True, 'create': False, 'edit': False, 'delete': False, 'export': True},
    },

   
}
