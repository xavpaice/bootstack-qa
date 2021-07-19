#! /bin/bash -x

# Shortcut to make a candidate branch charm
# usage: ./candidate.sh ~/charms/thruk-agent-charm thruk-agent 21.07

REPO_DIR=$1
CHARM_NAME=$2
REV=$3

OWNER=$(charm show cs:${CHARM_NAME} | awk '/Owner/ {print $NF}')

cd $REPO_DIR
git checkout master
git pull --rebase
git checkout -b candidate/$REV
git push origin candidate/$REV
make clean
make submodules
make submodules-update
build_dir=$(make release |awk '/Building charm to / {print $NF}')  # text changes between charms
charm_url=$(charm push $build_dir cs:~${OWNER}/${CHARM_NAME} |awk '/url:/ {print $NF}')

charm list-resources cs:$CHARM_NAME |tail -n +2

echo charm release --channel candidate $charm_url [--resource resource]
