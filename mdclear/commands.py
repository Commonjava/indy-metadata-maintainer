import click
import os
import sys
from time import sleep
from traceback import format_exc
import mdclear.config as config
import mdclear.sso as sso
import mdclear.pnc as pnc
import mdclear.indy as indy

@click.command()
@click.argument('env_yml') #, help='Target environment, including Indy/PNC URLs and SSO configuration')
@click.argument('build_ids', nargs=-1, required=True) #, help='The PNC build id')
def run(env_yml, build_ids):
    """ Clear the aggregated metadata for a given PNC build
    """
    env, sso_config = config.read_config(env_yml)

    sso.get_sso_token(sso_config, env)

    for build_id in build_ids:
        coords = pnc.get_coords(build_id, env)

        if coords is not None:
            indy.clear_metadata(coords, env)

