import datetime
from app.skills.skill_registry import register_skill

@register_skill(
    name="time",
    description="获取当前时间",
    parameters={
        "type": "object",
        "properties": {}
    }
)
class TimeSkill:

    def run(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")