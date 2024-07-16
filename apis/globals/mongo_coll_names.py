from apis.utils.common import myclient as mongo_client


class MongoColl:

    def __init__(self, db, name):
        self.db = db
        # Standard config
        self.name = name
        self.ref = mongo_client[self.db][self.name]
        # Temp config
        self.temp_name = f"{self.name}_temp"
        self.temp_ref = mongo_client[self.db][self.temp_name]
        # Backup config
        self.backup_name = f"{self.name}_backup"
        # Broken config
        self.broken_name = f"{self.name}_broken"

    def convert_primary_to_backup(self):
        try:
            self.ref.rename(self.backup_name, dropTarget=True)
        except Exception as e:
            print("No primary collection to rename.")

    def convert_temp_to_broken(self):
        self.temp_ref.rename(self.broken_name, dropTarget=True)

    def convert_temp_to_primary(self):
        self.temp_ref.rename(self.name, dropTarget=True)


# logs DB
logger_coll = MongoColl("logs", 'jobs')

# verdantime DB
verdantime_db = "verdantime"
entries_coll = MongoColl(verdantime_db, 'entries')
sources_coll = MongoColl(verdantime_db, 'sources')
source_types_coll = MongoColl(verdantime_db, 'source_types')
monthly_reports_coll = MongoColl(verdantime_db, 'monthly_reports')
users_coll = MongoColl(verdantime_db, 'users')

# apps_by_matthew DB
apps_by_matthew_db = "apps_by_matthew"
applications_coll = MongoColl(apps_by_matthew_db, 'applications')
skills_coll = MongoColl(apps_by_matthew_db, 'skills')
skill_types_coll = MongoColl(apps_by_matthew_db, 'skill_types')
support_statuses_coll = MongoColl(apps_by_matthew_db, 'support_statuses')