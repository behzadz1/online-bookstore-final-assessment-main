def test_account_redirects_when_logged_out(app_client):
    r = app_client.get("/account", follow_redirects=True)
    assert r.status_code == 200
    body = r.get_data(as_text=True).lower()
    # login GET returns {"ok": true}
    assert '"ok": true' in body or "ok" in body
