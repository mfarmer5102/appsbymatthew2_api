import datetime

from apis.globals.mongo_coll_names import traffic_logs_coll


# Modified and borrowed from https://stackoverflow.com/questions/25466904/print-raw-http-request-in-flask-or-wsgi
class RequestLogger(object):

    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        # error_log = env['wsgi.errors']

        def log_response(status, headers, *args):

            obj_to_save = {
                'timestamp': datetime.datetime.now(),
                'request': str(env),
                'response_status': status,
                'response': headers
            }

            for key in env:
                obj_to_save[f"request_{key}"] = str(env[key])

            try:
                traffic_logs_coll.ref.insert_one(obj_to_save)
            except Exception as e:
                print("Unable to save to traffic logs: ", e)
            return resp(status, headers, *args)

        return self._app(env, log_response)


