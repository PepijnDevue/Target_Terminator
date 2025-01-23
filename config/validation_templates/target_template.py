"""
Target yaml template.

This template can be used to validate the composition of any custom
target yaml file. This is also already done when creating an actual
environment.

Minimal viable yaml file looks like (_'s are placeholders for data):

```yaml
target0:
    size : [_, _]
    position : [_, _]
    max_spawn_position_deviation : _
    coll_radius : _
```

Add more by repeating this patter, replacing the number after the target
each time.
"""

TARGET_TEMPLATE = {
    'type': 'object',
    'patternProperties': {
        '^target\\d+$': {
            'type': 'object',
            'properties': {
                'sprite' : {
                    'type' : 'string'
                },
                'size' : {
                    'type' : 'array',
                    'minlength' : 2, 
                    'maxlength' : 2,
                    'items' : {'type': 'integer', 'min' : 1}
                },
                'position' : {
                    'type' : 'array',
                    'minlength' : 2, 
                    'maxlength' : 2,
                    'items' : {'type': 'integer', 'min' : 0}
                },
                'max_spawn_position_deviation' : {
                    'type' : 'number',
                    'min' : 0
                },
                'coll_radius' : {
                    'type' : 'number',
                    'min' : 0
                }
            },
            'required' : [
                'size', 
                'position', 
                'coll_radius', 
                'max_spawn_position_deviation'
            ],
            'additionalProperties' : False
        }
    },
    'additionalProperties' : False
}
