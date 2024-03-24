from api.ai_logic.schemas.application import application_schema

func_find_one_application_statement = {
    'name': 'find_one_application_statement',
    'description': "Find information about a single application.",
    'parameters': {
        'type': 'object',
        'properties': {
            'find_clause': {
                'type': 'object',
                'required': [
                    "title"
                ],
                'properties': application_schema
            }
        }
    }
}

func_find_many_application_statement = {
    'name': 'find_many_application_statement',
    'description': "Find information about multiple applications.",
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

func_create_application_statement = {
    'name': 'create_application_statement',
    'description': "Create a new record containing application information.",
    'parameters': {
        'type': 'object',
        'properties': {
            'insert_clause': {
                'type': 'object',
                'required': [
                    "title"
                ],
                'properties': application_schema
            }
        }
    }
}

func_update_application_statement = {
    'name': 'update_application_statement',
    'description': 'Update information about an application.',
    'parameters': {
        'type': 'object',
        'properties': {
            'find_clause': {
                'type': 'object',
                "required": [
                    "title"
                ],
                'properties': {
                    'title': {
                        'type': 'string',
                        'description': 'Name or title of the application.'
                    }
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
    func_find_one_application_statement,
    func_find_many_application_statement,
    func_create_application_statement,
    func_update_application_statement,
    func_delete_application_statement
]