from api.ai_logic.schemas.skill import skill_schema

func_extract_skill_info = {
    'name': 'extract_skill_info',
    'description': "Get the skill information from the body of the input text",
    'parameters': {
        'type': 'object',
        # "required": [
        #     "title",
        #     "is_featured"
        # ],
        'properties': skill_schema
    }
}

skill_functions = [
    func_extract_skill_info
]