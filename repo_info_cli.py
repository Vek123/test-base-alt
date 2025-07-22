#!/usr/bin/env python3
__all__ = ()

import json

import fire

import alt_repos_stat as stat


class RepoInfo:
    """
    A CLI tool for getting information about ALT Linux repository.
    """

    async def compare(self, branch1: str, branch2: str):
        """Get difference between two binary branches."""
        branch1_archs = await stat.get_branch_archs(branch1)
        branch2_archs = await stat.get_branch_archs(branch2)
        common_archs = list(
            set(branch1_archs).intersection(set(branch2_archs)),
        )
        compare_data = {}

        for arch in common_archs:
            branch1_packages = await stat.get_branch_packages(branch1, arch)
            branch2_packages = await stat.get_branch_packages(branch2, arch)
            compared = stat.compare_packages(
                branch1_packages,
                branch2_packages,
            )
            compare_data[arch] = {
                f'{branch1}_not_in_{branch2}': compared['a_not_in_b'],
                f'{branch2}_not_in_{branch1}': compared['b_not_in_a'],
                f'{branch1}_newer_than_{branch2}': compared['a_newer_than_b'],
            }

        return json.dumps(compare_data)


if __name__ == '__main__':
    obj = RepoInfo()
    fire.Fire(obj)
