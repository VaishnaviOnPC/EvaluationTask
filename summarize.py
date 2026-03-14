#!/usr/bin/env spack-python

import json
import argparse
from spack.spec import Spec
import spack.repo

TOKEN_LIMIT = 500


def collect_package(pkg_name):

    spec = Spec(pkg_name)
    pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
    pkg = pkg_cls(spec)

    versions = [
        str(v) for v in pkg.versions.keys()
        if str(v)[0].isdigit()
    ][:3]

    variants = [
        str(v) for v in pkg.variants.keys()
        if not str(v).startswith("@")
    ][:3]

    dependencies = []
    unbounded = []

    for _, dep_map in pkg.dependencies.items():

        for _, dep in dep_map.items():
            dep_name = dep.spec.name
            if (
                not dep_name
                or dep_name.startswith("+")
                or dep_name.startswith("@")
                or "=" in dep_name
            ):
                continue

            dependencies.append(dep_name)
            spec_str = str(dep.spec)

            if not dep.spec.versions or not dep.spec.versions.concrete:
                unbounded.append(dep_name)

    return {
        "pkg": pkg_name,
        "v": sorted(set(versions), reverse=True),
        "var": sorted(set(variants)),
        "deps": sorted(set(dependencies))[:12],
        "unbounded": sorted(set(unbounded))[:20]
    }

def summarize(packages):

    summaries = []
    token_usage = {}

    for pkg in packages:

        data = collect_package(pkg)
        summaries.append(data)

        pkg_tokens = int(len(json.dumps(data)) / 4)
        token_usage[pkg] = pkg_tokens

    output = {"packages": summaries}

    json_str = json.dumps(output, separators=(",", ":"))
    total_tokens = int(len(json_str) / 4)

    with open("summary.json", "w") as f:
        f.write(json_str)

    print(json_str)

    print("\nToken usage per package:")
    for p, t in token_usage.items():
        print(f"{p}: {t} tokens")

    print(f"\nTotal tokens: {total_tokens}")

    if total_tokens > TOKEN_LIMIT:
        print("WARNING: token limit exceeded")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="+")
    args = parser.parse_args()
    summarize(args.packages)


if __name__ == "__main__":
    main()