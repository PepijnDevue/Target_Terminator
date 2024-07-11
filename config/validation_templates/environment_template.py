ENVIRONMENT_TEMPLATE = {
    'window_dimensions' : {
        'required' : True,
        'type' : 'list',
        'minlength' : 2, 
        'maxlength' : 2,
        'items' : [
            {'type' : 'integer', 'min' : 1}, 
            {'type' : 'integer', 'min' : 1}
        ]
    },
    'plane_pos_scale' : {
        'required' : True,
        'min' : 0,
        'type' : 'number'
    },
    'ground' : {
        'required' : True,
        'type' : 'dict',
        'schema' : {
            'sprite' : {
                'required' : False,
                'type' : 'string'
            },
            'height' : {
                'required' : True,
                'type' : 'integer',
                'min' : 1
            },
            'collision_elevation' : {
                'required' : True,
                'type' : 'integer',
                'min' : 0
            }
        }
    }
}
