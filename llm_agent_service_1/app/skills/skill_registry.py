SKILL_REGISTRY = {}

def register_skill(name, description, parameters):

    def decorator(cls):

        SKILL_REGISTRY[name] = {
            "instance": cls(),
            "description": description,
            "parameters": parameters
        }

        return cls

    return decorator


def get_skill(name):
    return SKILL_REGISTRY.get(name)