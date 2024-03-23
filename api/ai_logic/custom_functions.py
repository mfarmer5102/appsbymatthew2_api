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
                'properties': {
                    'title': {
                        'type': 'string',
                        'description': 'Name of the application'
                    },
                    'publish_date': {
                        'type': 'string',
                        'description': 'The date on which the application was published'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'A description for the application, or how the application is described.'
                    },
                    'image_url': {
                        'type': 'string',
                        'description': 'The image or thumbnail to show for the application.'
                    },
                    'deployed_link': {
                        'type': 'string',
                        'description': 'The URL or link at which the application is deployed.'
                    },
                    'is_featured': {
                        'type': 'boolean',
                        'description': 'Whether or not the application is featured.',
                        "default": False
                    },
                    'support_status': {
                        'type': 'string',
                        'description': 'The current support status of the application.',
                        'enum': [
                            'ACTIVE',
                            'DISCONTINUED',
                            'EXPERIMENTAL',
                            'INACTIVE'
                        ],
                        "default": "ACTIVE"
                    },
                    'associated_skills': {
                        'type': 'array',
                        'description': 'A list of technical skills demonstrated by, used by, or associated with the application.',
                        'items': {
                            'type': 'string',
                            'enum': [
                                'React',
                                'GraphQL',
                                'Python'
                            ]
                        }
                    }
                }
            }
        }
    }
}

func_extract_application_info = {
    'name': 'extract_application_info',
    'description': """
        Get the application information from the body of the input text.
    """,
    'parameters': {
        'type': 'object',
        # "required": [
        #     "title",
        #     "is_featured"
        # ],
        'properties': {
            'title': {
                'type': 'string',
                'description': 'Name of the application'
            },
            'publish_date': {
                'type': 'string',
                'description': 'The date on which the application was published'
            },
            'description': {
                'type': 'string',
                'description': 'A description for the application, or how the application is described.'
            },
            'image_url': {
                'type': 'string',
                'description': 'The image or thumbnail to show for the application.'
            },
            'deployed_link': {
                'type': 'string',
                'description': 'The URL or link at which the application is deployed.'
            },
            'is_featured': {
                'type': 'boolean',
                'description': 'Whether or not the application is featured.',
                "default": False
            },
            'support_status': {
                'type': 'string',
                'description': 'The current support status of the application.',
                'enum': [
                    'ACTIVE',
                    'DISCONTINUED',
                    'EXPERIMENTAL',
                    'INACTIVE'
                ],
                "default": "ACTIVE"
            },
            'associated_skills': {
                'type': 'array',
                'description': 'A list of technical skills demonstrated by, used by, or associated with the application.',
                'items': {
                    'type': 'string',
                    'enum': [
                        'React',
                        'GraphQL',
                        'Python'
                    ]
                }
            }
        }
    }
}

application_functions = [
    func_create_upsert_statement,
    func_extract_application_info
]