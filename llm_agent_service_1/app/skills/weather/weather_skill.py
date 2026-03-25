import requests
from app.skills.skill_registry import register_skill

API_KEY = "SpzGHbauoMATjjwFq"

city_map = {
    "武汉": "wuhan",
    "北京": "beijing",
    "上海": "shanghai"
}

@register_skill(
    name="weather",
    description="查询城市实时天气，例如北京、上海、武汉",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名称"
            }
        },
        "required": ["city"]
    }
)
class WeatherSkill:

    def run(self, city):

        city = city_map.get(city, city)

        url = "https://api.seniverse.com/v3/weather/now.json"

        params = {
            "key": API_KEY,
            "location": city,
            "language": "zh-Hans",
            "unit": "c"
        }

        r = requests.get(url, params=params)

        data = r.json()

        result = data["results"][0]

        location = result["location"]["name"]
        weather = result["now"]["text"]
        temp = result["now"]["temperature"]

        # return f"{location}当前天气{weather}，温度{temp}°C"
        return result