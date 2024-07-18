from apis.src.ai_logic.schemas.skill import skill_schema

func_find_one_skill_statement = {
    'name': 'find_one_skill_statement',
    'description': "Find information about one skill.",
    'parameters': {
        'type': 'object',
        'properties': {
            'find_clause': {
                'type': 'object',
                'required': [
                    'name'
                ],
                'properties': skill_schema
            }
        }
    }
}

func_find_many_skill_statement = {
    'name': 'find_many_skill_statement',
    'description': "Find information about multiple skills.",
    'parameters': {
        'type': 'object',
        'properties': {
            'find_clause': {
                'type': 'object',
                'properties': skill_schema
            }
        }
    }
}

skill_functions = [
    func_find_one_skill_statement,
    func_find_many_skill_statement
]