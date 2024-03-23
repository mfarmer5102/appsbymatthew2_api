from api.ai_logic.schemas.application import application_schema

func_find_application_statement = {
    'name': 'find_application_statement',
    'description': "Find information about an application.",
    'parameters': {
        'type': 'object',
        'properties': {
            'find_clause': {
                'type': 'object',
                'properties': application_schema
            }
        }
    }
}

func_create_upsert_application_statement = {
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
                        'description': 'Name of the application.'
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

func_delete_application_statement = {
    'name': 'delete_application_statement',
    'description': "Delete an application.",
}


application_functions = [
    func_find_application_statement,
    func_create_upsert_application_statement,
    func_delete_application_statement
]