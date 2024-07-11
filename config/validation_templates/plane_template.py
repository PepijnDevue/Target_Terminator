PLANE_TEMPLATE = {
    'sprite' : {
        'required' : False,
        'type' : 'dict',
        'schema' : {
            'side_view_dir' : {
                'required' : False,
                'type' : 'string'
            },
            'top_view_dir' : {
                'required' : False,
                'type' : 'string'
            },
        }
    },
    'properties' : {
        'required' : True,
        'type' : 'dict',
        'schema' : {
            'mass' : {
                'type' : 'number',
                'min' : 0
            },
            'engine_force' : {
                'type' : 'number',
                'min' : 0
            },
            'agility' : {
                'type' : 'number',
                'min' : 0
            },
            'drag_constant' : {
                'type' : 'number',
                'min' : 0
            },
            'lift_constant' : {
                'type' : 'number',
                'min' : 0
            },
            'critical_aoa_lower_bound' : {
                'required' : True,
                'type' : 'list',
                'minlength' : 2, 
                'maxlength' : 2,
                'items' : [
                    {'type' : 'number'}, 
                    {'type': 'number'}
                ]
            },
            'critical_aoa_higher_bound' : {
                'required' : True,
                'type' : 'list',
                'minlength' : 2, 
                'maxlength' : 2,
                'items' : [
                    {'type' : 'number'}, 
                    {'type': 'number'}
                ]
            },
            'lift_coeficient_aoa_0' : {
                'type' : 'number',
                'min' : 0
            },
            'drag_coeficient_aoa_0' : {
                'type' : 'number',
                'min' : 0
            }
        }
    },
    'starting_config' : {
        'required' : True,
        'type' : 'dict',
        'schema' : {
            'initial_throttle' : {
                'type' : 'number',
                'min' : 0
            },
            'initial_pitch' : {
                'type' : 'number',
                'min' : 0
            },
            'initial_velocity' : {
                'required' : True,
                'type' : 'list',
                'minlength' : 2, 
                'maxlength' : 2,
                'items' : [
                    {'type' : 'number'}, 
                    {'type': 'number'}
                ]
            },
            'initial_position' : {
                'required' : True,
                'type' : 'list',
                'minlength' : 2, 
                'maxlength' : 2,
                'items' : [
                    {'type' : 'integer', 'min' : 0}, 
                    {'type': 'integer', 'min' : 0}
                ]
            },
            'size' : {
                'required' : True,
                'type' : 'list',
                'minlength' : 2, 
                'maxlength' : 2,
                'items' : [
                    {'type' : 'integer', 'min' : 0}, 
                    {'type': 'integer', 'min' : 0}
                ]
            },
        }
    }
}
