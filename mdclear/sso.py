import requests

def get_sso_token(sso_config, env):
    if sso_config.enabled is False:
        return None

    response = requests.post(sso_config.url, data=sso_config.form, verify=env.ssl_verify)
    response.raise_for_status()

    token = response.json()['access_token']
    print(f"Token: {token}")
    env.set_sso_token(token)

    return token
