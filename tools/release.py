#!/usr/bin/env python3
"""Release a charm from candidate to stable channel."""

import argparse
import json
import subprocess


def run_charm_command(command, charm, channel=None):
    """Run a charm show/etc command and return the parsed output."""
    data = None
    result = None
    cmdline = [
            "charm",
            command,
            charm,
            "--format",
            "json",
        ]
    if channel:
        cmdline.append("--channel")
        cmdline.append(channel)
    try:
        result = subprocess.check_output(cmdline)
        data = json.loads(result)
    except Exception as e:
        print("Unable to get output of {} for {} with {}".format(command, charm, e))

    return data


def charm_show(charm_name):
    """Get charm info and return a dict."""
    result = get_promulgated_charm_info(charm_name)
    owner_result = run_charm_command("show", "cs:~{}/{}".format(result['owner'],
                                                                charm_name),
                                     channel='candidate')
    result['owner_revision'] = owner_result['id-revision']['Revision']
    return result


def get_promulgated_charm_info(charm_name):
    """Get charm info from promulgated URL."""
    data = run_charm_command("show", "cs:{}".format(charm_name))
    resources = run_charm_command("list-resources", "cs:{}".format(charm_name))
    res_info = []

    for resource in resources:
        res_info.append("{}-{}".format(resource['Name'], resource['Revision']))
    result = {
        'owner': data['owner']['User'],
        'promulgated_revision': data['id-revision']['Revision'],
        'resources': res_info,
    }

    return result


def charm_release(charm_name, candidate_info):
    """Promote the candidate rev to stable."""
    charm_url = "cs:~{}/{}-{}".format(candidate_info['owner'],
                                      charm_name,
                                      candidate_info['owner_revision'])
    command = ["charm", "release", charm_url]

    for r in candidate_info['resources']:
        command.append("--resource")
        command.append(r)
    try:
        subprocess.check_output(command)
    except Exception as e:
        print("unable to promote charm with %s" % e)


def parse_args():
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Promote a charm from candidate to stable"
    )
    parser.add_argument("charm", help="Charm to promote")
    args = parser.parse_args()

    return args


def main():
    """Promote the given charm from candidate to stable."""
    args = parse_args()
    candidate_info = charm_show(args.charm)
    charm_release(args.charm, candidate_info)
    updated_info = charm_show(args.charm)
    if updated_info['promulgated_revision'] > candidate_info['promulgated_revision']:
        print("Update was successful")
    else:
        print("the promulgated charm revision has not incremented, please investigate")


if __name__ == "__main__":
    main()
