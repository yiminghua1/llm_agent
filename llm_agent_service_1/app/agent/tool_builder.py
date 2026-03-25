from app.skills.skill_registry import SKILL_REGISTRY

def build_tools():

    tools = []

    for name, skill in SKILL_REGISTRY.items():

        tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": skill["description"],
                "parameters": skill["parameters"]
            }
        })

    return tools