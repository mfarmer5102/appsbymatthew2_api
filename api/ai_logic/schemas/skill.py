from common import database

skill_types_collection = database['skill_types']

skill_schema = {
    'name': {
        'type': 'string',
        'description': 'Name of the skill.'
    },
    'code': {
        'type': 'string',
        'description': 'The name of the skill in uppercase with no spaces.'
    },
    'skill_type_code': {
        'type': 'string',
        'description': 'The type of skill in uppercase with no spaces.',
        'enum': skill_types_collection.distinct('code'),
    },
    'is_proficient': {
        'type': 'boolean',
        'description': 'Whether or not proficiency in the skill can be claimed.',
        'default': False
    },
    'is_visible_in_app_details': {
        'type': 'boolean',
        'description': 'Whether or not the skill should be visible in the details of an application.',
        'default': False
    }
}