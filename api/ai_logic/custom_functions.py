from api.ai_logic.schemas.application import application_schema

func_create_upsert_statement = {
    'name': 'create_upsert_statement',
    'description': 'Create or update information about an application.',
    'parameters': {
        'type': 'object',
        'properties': {
            'find_clause': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string',
                        'description': 'Name of the application'
                    },
                }
            },
            'set_clause': {
                'type': 'object',
                'properties': application_schema
            }
        }
    }
}

func_extract_application_info = {
    'name': 'extract_application_info',
    'description': "Get the application information from the body of the input text",
    'parameters': {
        'type': 'object',
        # "required": [
        #     "title",
        #     "is_featured"
        # ],
        'properties': application_schema
    }
}

application_functions = [
    func_create_upsert_statement,
    func_extract_application_info
]