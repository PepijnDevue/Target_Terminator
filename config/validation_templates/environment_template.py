"""
Environment yaml template.

This template can be used to validate the composition of any custom
environment yaml file. This is also already done when creating an actual
environment.

Minimal viable yaml file looks like (_'s are placeholders for data):

```yaml
window_dimensions : [_, _]
plane_pos_scale : _
ground:
    height : _
    collision_elevation : _
```
"""

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
    'background' : {
        'required' : False,
        'type' : 'dict',
        'schema' : {
            'sprite' : {
                'required' : False,
                'type' : 'string',
            }
        }
    }
}
