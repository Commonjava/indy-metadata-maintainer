from ruamel.yaml import YAML
from getpass import getpass, getuser
import os

ENV_INDY_URL = 'indy-url'
ENV_PNC_URL = 'pnc-url'
ENV_CLEAR_STORES = 'clear-stores'
ENV_SSL_VERIFY = 'ssl-verify'
ENV_SSO_SECTION = 'sso'

SSO_ENABLE='enabled'
SSO_GRANT_TYPE = 'grant-type'
SSO_URL = 'url'
SSO_REALM = 'realm'
SSO_CLIENT_ID = 'client-id'
SSO_CLIENT_SECRET = 'client-secret'
SSO_USERNAME = 'username'
SSO_PASSWORD = 'password'

CLIENT_CREDENTIALS_GRANT_TYPE = 'client_credentials'
PASSWORD_GRANT_TYPE = 'password'

DEFAULT_SSO_GRANT_TYPE = CLIENT_CREDENTIALS_GRANT_TYPE

class Environment:
    def __init__(self, env_spec):
        self.indy_url = env_spec.get(ENV_INDY_URL)
        self.pnc_url = env_spec.get(ENV_PNC_URL)
        self.clear_stores = env_spec.get(ENV_CLEAR_STORES) or ['maven:group:builds-untested']
        self.headers = {}

        self.ssl_verify = env_spec.get(ENV_SSL_VERIFY)
        if self.ssl_verify is None:
            self.ssl_verify = True

    def set_sso_token(self, token):
        self.token = token
        self.headers = {
            'Authorization': f"Bearer {token}"
        }

class SingleSignOn:
    def __init__(self, sso_spec):
        if sso_spec is None or sso_spec.get(SSO_ENABLE) is False:
            self.enabled = False
        else:
            self.enabled = sso_spec[SSO_ENABLE]
            self.grant_type = sso_spec.get(SSO_GRANT_TYPE) or DEFAULT_SSO_GRANT_TYPE

            if self.grant_type == DEFAULT_SSO_GRANT_TYPE:
                self.form = {
                    'grant_type': self.grant_type, 
                    'client_id': sso_spec[SSO_CLIENT_ID],
                    'client_secret': sso_spec[SSO_CLIENT_SECRET]
                }

            elif self.grant_type == PASSWORD_GRANT_TYPE:
                username = input("Username: ") or getuser()
                password = getpass()
                self.form = {
                    'grant_type': self.grant_type, 
                    'client_id': sso_spec[SSO_CLIENT_ID],
                    'client_secret': sso_spec[SSO_CLIENT_SECRET],
                    'username': username,
                    'password': password
                }

            base_url = sso_spec[SSO_URL]
            if base_url.endswith('/'):
                base_url = base_url[:-1]

            self.url = f"{base_url}/auth/realms/{sso_spec[SSO_REALM]}/protocol/openid-connect/token"

def read_config(env_yml):
    """ Read the suite configuration that this worker should run, from a config.yml file 
    (specified on the command line and passed in as a parameter here). 

    Once we have a suite YAML file (from the suite_yml config), that file will be parsed
    and passed back with the rest of the config values, in a Config object.

    If any required configs are missing and don't have default values, error messages will
    be generated. If the list of errors is non-empty at the end of this method, an error
    message containing all of the problems will be logged to the console and an
    exception will be raised.
    """
    errors = []

    env_spec = {}
    if env_yml is None:
        errors.append(f"Missing environment config file")
    elif os.path.exists(env_yml):
        with open(env_yml) as f:
            yaml = YAML(typ='safe')
            env_spec = yaml.load(f)
    else:
        errors.append( f"Invalid environment config file")

    env = Environment(env_spec)

    errors = []
    if env.indy_url is None:
        errors.append(f"Missing Indy URL configuration: {ENV_INDY_URL}")

    if env.pnc_url is None:
        errors.append(f"Missing PNC URL configuration: {ENV_PNC_URL}")

    if len(errors) > 0:
        print("\n".join(errors))
        raise Exception("Invalid configuration")

    if env.indy_url.endswith('/'):
        env.indy_url = env.indy_url[:-1]

    if env.pnc_url.endswith('/'):
        env.pnc_url = env.pnc_url[:-1]

    sso = SingleSignOn(env_spec.pop(ENV_SSO_SECTION, None))

    return (env, sso)

