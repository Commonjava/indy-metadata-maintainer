import requests
from mdclear.utils import MOD_HEADERS

def get_coords(build_id, env):
	""" Retrieve the list of artifact coordinates from the PNC build record, whose metadata should be cleared.
	"""

	# url_frag = f"{env.pnc_url}/pnc-web/apidocs/#!/build-records/{build_id}/built-artifacts?pageSize=200&pageIndex="
	url_frag= f"{env.pnc_url}/pnc-rest/rest/build-records/{build_id}/built-artifacts?pageSize=200&pageIndex="
	page = 0
	total_pgs = -1

	results = []
	while total_pgs < 0 or page < total_pgs:
		pg_url=url_frag + str(page)
		# print(pg_url)

		resp = requests.get(url=pg_url, headers=MOD_HEADERS)
		resp.raise_for_status()

		if resp.status_code == 200:
			data = resp.json()

			if total_pgs < 0:
				total_pgs = data['totalPages']

			for entry in data['content']:
				ga = entry['identifier'].split(':')[:2]
				gapath = f"{ga[0].replace('.', '/')}/{ga[1]}"
				if gapath not in results:
					results.append(gapath)

			page+=1
		elif resp.status_code == 204:
			print(f"No content found for build: {build_id}")
			return None

	return results
