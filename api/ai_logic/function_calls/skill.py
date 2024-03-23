from api.ai_logic.schemas.skill import skill_schema

func_find_skill_statement = {
    'name': 'find_skill_statement',
    'description': "Find information about a skill.",
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
    func_find_skill_statement
]