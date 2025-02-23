"""
Plane yaml template.

This template can be used to validate the composition of any custom
plane yaml file. This is also already done when creating an actual
environment.

Minimal viable yaml file looks like (_'s are placeholders for data):

```yaml
properties:
    mass : _
    drag_constant : _
    lift_constant : _
    lift_coefficient_aoa_0 : _
    drag_coefficient_aoa_0 : _
    engine_force : _
    agility : _
    initial_throttle : _
    initial_pitch : _
    collision_radius : _
    critical_aoa_lower_bound : [_, _] 
    critical_aoa_higher_bound : [_, _] 
    initial_velocity : [_, _] 
    initial_position : [_, _] 
    max_spawn_position_deviation : _
    max_spawn_pitch_deviation : _
bullet_config:
    speed : _
    lifetime : _
    size : [_, _]
    coll_radius : _
```
"""

PLANE_TEMPLATE = PLANE_TEMPLATE = {
    'type': 'object',
    'properties': {
        'sprite': {
            'type': 'object',
            'properties': {
                'side_view_dir': {
                    'type': 'string'
                },
                'size': {
                    'type': 'array',
                    'minItems': 2,
                    'maxItems': 2,
                    'items': {'type': 'integer', 'minimum': 0}
                }
            },
            'required': ['size']
        },
        'properties': {
            'type': 'object',
            'properties': {
                'mass': {
                    'type': 'number', 
                    'minimum': 0
                },
                'drag_constant': {
                    'type': 'number', 
                    'minimum': 0
                },
                'lift_constant': {
                    'type': 'number', 
                    'minimum': 0
                },
                'lift_coefficient_aoa_0': {
                    'type': 'number', 
                    'minimum': 0
                },
                'drag_coefficient_aoa_0': {
                    'type': 'number', 
                    'minimum': 0
                },
                'engine_force': {
                    'type': 'number', 
                    'minimum': 0
                },
                'agility': {
                    'type': 'number', 
                    'minimum': 0
                },
                'initial_throttle': {
                    'type': 'number', 
                    'minimum': 0
                },
                'initial_pitch': {
                    'type': 'number', 
                    'minimum': 0
                },
                'collision_radius': {
                    'type': 'number', 
                    'minimum': 0
                },
                'critical_aoa_lower_bound': {
                    'type': 'array',
                    'minItems': 2,
                    'maxItems': 2,
                    'items': {'type': 'number'}
                },
                'critical_aoa_higher_bound': {
                    'type': 'array',
                    'minItems': 2,
                    'maxItems': 2,
                    'items': {'type': 'number'}
                },
                'initial_velocity': {
                    'type': 'array',
                    'minItems': 2,
                    'maxItems': 2,
                    'items': {'type': 'number'}
                },
                'initial_position': {
                    'type': 'array',
                    'minItems': 2,
                    'maxItems': 2,
                    'items': {'type': 'integer', 'minimum': 0}
                },
                'max_spawn_position_deviation': {
                    'type': 'number', 
                    'minimum': 0
                },
                'max_spawn_pitch_deviation': {
                    'type': 'number',
                    'minimum': 0,
                    'maximum': 360
                }
            },
            'required': [
                'critical_aoa_lower_bound', 
                'critical_aoa_higher_bound',
                'initial_velocity', 
                'initial_position',
                'max_spawn_position_deviation', 
                'max_spawn_pitch_deviation'
            ]
        },
        'bullet_config': {
            'type': 'object',
            'properties': {
                'sprite': {
                    'type': 'string'
                    },
                'speed': {
                    'type': 'number', 
                    'minimum': 0.1
                },
                'lifetime': {
                    'type': 'number', 
                    'minimum': 0
                },
                'size': {
                    'type': 'array',
                    'minItems': 2,
                    'maxItems': 2,
                    'items': {'type': 'integer', 'minimum': 1}
                },
                'coll_radius': {
                    'type': 'number', 
                    'minimum': 0
                }
            },
            'required': ['speed', 'lifetime', 'size', 'coll_radius']
        }
    },
    'required': ['properties', 'bullet_config']
}
