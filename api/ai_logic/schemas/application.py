from common import database

skills_collection = database["skills"]
support_status_collection = database["support_statuses"]

application_schema = {
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
        'description': 'Whether or not the application is featured.'
    },
    'support_status_code': {
        'type': 'string',
        'description': 'The current support status of the application.',
        'enum': support_status_collection.distinct('code')
    },
    'associated_skill_codes': {
        'type': 'array',
        'description': 'A list of technical skills demonstrated by, used by, or associated with the application.',
        'items': {
            'type': 'string',
            'enum': skills_collection.distinct('code')
        }
    }
}