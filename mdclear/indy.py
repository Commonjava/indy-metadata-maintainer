import requests
from mdclear.utils import MOD_HEADERS

def clear_metadata(build_id, coords, env):
    """
        For each coordinate path (Maven GA) in the given build, issue a HTTP DELETE command.
    """
    headers = {**MOD_HEADERS, **env.headers}
    print(f"HTTP headers: {headers}")
    for target in env.clear_stores:
        total=len(coords)
        index = 1
        for ga_path in coords:
            url = f"{env.indy_url}/api/content/{target.replace(':', '/')}/{ga_path}/maven-metadata.xml"

            print(f"DELETE {url}")
            resp = requests.delete(url=url, headers=headers)

            resp.raise_for_status()

            status = resp.status_code
            if status != 204:
                print(f"{build_id}: {index}/{total} Error deleting {target}/{ga_path} metadata: {status} {resp}")
            else:
                print(f"{build_id}: {index}/{total} {status} {target}/{ga_path} deleted.")

            index+=1
