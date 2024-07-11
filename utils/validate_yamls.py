def validate_plane_data(plane_data: dict)-> bool:
    """
    Validate minimal viable config for plane.
    """
    for topic_key, sub_keys in (
        (
            "properties", [
                "mass", 
                "engine_force",
                "agility",
                "drag_constant",
                "lift_constant",
                "critical_aoa_lower_bound",
                "critical_aoa_higher_bound",
                "lift_coeficient_aoa_0",
                "drag_coeficient_aoa_0"
            ]
        ), 
        (
            "starting_config", [
                "initial_throttle",
                "initial_pitch",
                "initial_velocity",
                "initial_position",
                "size"
            ]
        )
    ):
        if topic_key in plane_data:
            for sub_key in sub_keys:
                if sub_key not in plane_data[topic_key]:
                    raise KeyError(
                        f"Missing sub key `{sub_key}` under "
                        f"key `{topic_key}` in plane configutation."
                    )
        else:
            raise KeyError(
                f"Missing key `{topic_key}` in plane configutation."
            )
    return True

def validate_env_data(env_data: dict)-> bool:
    """
    Validate minimal viable config for environment.
    """
    for topic_key in ["window_dimensions", "plane_pos_scale"]:
        if topic_key not in env_data:
            raise KeyError(
                f"Missing key `{topic_key}` in environment configutation."
            )    
    return True
