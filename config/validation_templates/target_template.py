"""
Target yaml template.

This template can be used to validate the composition of any custom
target yaml file. This is also already done when creating an actual
environment.

Minimal viable yaml file looks like (_'s are placeholders for data):

```yaml
size : [_, _]
position : [_, _]
max_spawn_position_deviation : _
coll_radius : _
```
"""

# {
#     "type": "object",
#     "patternProperties": {
#         "^target\\d+$": {
#             "type": "object",
#             "properties": {
#                 "sprite": { "type": "string" },
#                 "size": {
#                     "type": "array",
#                     "minItems": 2,
#                     "maxItems": 2,
#                     "items": { "type": "integer", "minimum": 1 }
#                 },
#                 "position": {
#                     "type": "array",
#                     "minItems": 2,
#                     "maxItems": 2,
#                     "items": { "type": "integer", "minimum": 0 }
#                 },
#                 "max_spawn_position_deviation": { "type": "integer", "minimum": 0 },
#                 "coll_radius": { "type": "integer", "minimum": 0 }
#             },
#             "required": ["size", "position", "coll_radius"],
#             "additionalProperties": false
#         }
#     },
#     "additionalProperties": false
# }

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
