from multipledispatch import dispatch

@dispatch(dict, list)
def validate_yaml_data(
    data: dict, 
    keys: list[str]
)-> bool:
    """
    Validate minimal viable config for environment.
    """
    for topic_key in keys:
        if topic_key not in data:
            raise KeyError(
                f"Missing key `{topic_key}` in environment configutation."
            )    
    return True

@dispatch(dict, tuple)
def validate_yaml_data(
    data: dict, 
    keys: tuple[tuple[str, list[str]]]
)-> bool:
    """
    Validate minimal viable config for environment.
    """
    for topic_key, sub_keys in keys:
        if topic_key in data:
            for sub_key in sub_keys:
                if sub_key not in data[topic_key]:
                    raise KeyError(
                        f"Missing sub key `{sub_key}` under "
                        f"key `{topic_key}` in plane configutation."
                    )
        else:
            raise KeyError(
                f"Missing key `{topic_key}` in plane configutation."
            )
    return True
