TARGET_TEMPLATE = {
    'sprite' : {
        'required' : False,
        'type' : 'string'
    },
    'size' : {
        'required' : True,
        'type' : 'list',
        'minlength' : 2, 
        'maxlength' : 2,
        'items' : [
            {'type' : 'integer', 'min' : 1}, 
            {'type': 'integer', 'min' : 1}
        ]
    },
    'position' : {
        'required' : True,
        'type' : 'list',
        'minlength' : 2, 
        'maxlength' : 2,
        'items' : [
            {'type' : 'integer', 'min' : 0}, 
            {'type' : 'integer', 'min' : 0}
        ]
    },
}
