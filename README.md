# Consolidated bundle tests for Bootstack managed charms

This repo contains a handful of bundles and tests to assist with charm releases
for a subset of the charms that are included in cs:~llama-charmers and
cs:~bootstack-charmers.  The bundle is deployed via Zaza, and a small subset of
tests run.

Included in the tests are deploys from the 'candidate' channel, as well as
deploys from stable and upgrade to 'candidate'.

## Running

To run all the tests, first ensure that each charm in
tests/modules/bootstackqa.py has a build from the candidate branch, uploaded and
released in the candidate channel.  Then:

```
make functional
```

To run just a subset of bundles, you may use:

```
tox -e smoke
```

## TODO

* keep output of tests
* cut down the side effect if some charms go wrong -> basic unit crashes -> affect the charms to test later

