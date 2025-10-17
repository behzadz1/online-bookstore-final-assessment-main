
# Phase 3 follow-ups

- Uses `.coveragerc` to omit `profiles/` and `tests/` from coverage so your app's real code is measured.
- `pytest.ini` enforces a stricter coverage gate (85%). Bump to 90% after adding a few more small tests.
- `Makefile` adds handy tasks: `make test`, `make profile-timeit`, `make profile-checkout`, `make lint`, `make security`.
