from typing import Tuple
from flask.testing import FlaskClient


def try_post_route(
    client: FlaskClient, route_variants, data=None, follow_redirects=True
):
    for rt in route_variants:
        resp = client.post(rt, data=data or {}, follow_redirects=follow_redirects)
        if resp.status_code != 404:
            return rt, resp
    # If all 404, return the last one for visibility
    return route_variants[-1], resp


def try_get_route(client: FlaskClient, route_variants, follow_redirects=True):
    for rt in route_variants:
        resp = client.get(rt, follow_redirects=follow_redirects)
        if resp.status_code != 404:
            return rt, resp
    return route_variants[-1], resp
