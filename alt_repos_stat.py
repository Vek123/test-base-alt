__all__ = ()

from collections import defaultdict
from typing import Iterable

import aiohttp


URL_BRANCH_ARCH_TEMPLATE = (
    'https://rdb.altlinux.org/api/site/all_pkgset_archs?branch={branch}'
)
URL_BRANCH_BINARY_PACKAGES_TEMPLATE = (
    'https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}'
)


class BranchPackageFilters:
    @classmethod
    def _is_first_version_newer(cls, version1: str, version2: str) -> bool:
        for val1, val2 in zip(version1.split('.'), version2.split('.')):
            if val1 > val2:
                return True

        return len(val1) > len(val2)

    @classmethod
    def _get_package_data(cls, package: dict, keys: tuple[str]) -> tuple[str]:
        return tuple([package.get(key) for key in keys])

    @classmethod
    def a_not_in_b(cls, a: Iterable, b: Iterable) -> list:
        return list(filter(lambda x: x not in b, a))

    @classmethod
    def group_similar_packages_by_pairs(
        cls,
        a: Iterable,
        b: Iterable,
        criteria: tuple[str] = ('name',),
    ) -> list[tuple[dict, dict]]:
        a_packages = defaultdict(list)
        for package in a:
            a_packages[cls._get_package_data(package, criteria)].append(
                package,
            )

        for package in b:
            package_unique_data = cls._get_package_data(package, criteria)
            if package_unique_data in a_packages:
                a_packages[package_unique_data].append(package)

        return [tuple(pair) for pair in a_packages.values() if len(pair) == 2]

    @classmethod
    def a_newer_version_release_than_b(
        cls,
        a: Iterable,
        b: Iterable,
    ) -> list[dict]:
        newer_packages = []
        similar_packages_pairs = cls.group_similar_packages_by_pairs(a, b)
        for pair in similar_packages_pairs:
            if cls._is_first_version_newer(
                pair[1]['version'],
                pair[0]['version'],
            ):
                continue

            if (
                pair[0]['version'] == pair[1]['version']
                and pair[0]['release'] <= pair[1]['release']
            ):
                continue

            newer_packages.append(pair[0])

        return newer_packages


async def get_branch_archs(branch: str) -> list[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            URL_BRANCH_ARCH_TEMPLATE.format(branch=branch),
        ) as response:
            data = await response.json()
            return [arch['arch'] for arch in data['archs']]


async def get_branch_packages(branch: str, arch: str = '') -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            URL_BRANCH_BINARY_PACKAGES_TEMPLATE.format(branch=branch),
            params={'arch': arch},
        ) as response:
            data = await response.json()
            return data.get('packages', [])


def compare_packages(packages1: list[dict], packages2: list[dict]) -> dict:
    first_not_in_second = BranchPackageFilters.a_not_in_b(packages1, packages2)
    second_not_in_first = BranchPackageFilters.a_not_in_b(
        packages2,
        packages1,
    )
    first_newer_than_in_second = (
        BranchPackageFilters.a_newer_version_release_than_b(
            packages1,
            packages2,
        )
    )
    return {
        'a_not_in_b': first_not_in_second,
        'b_not_in_a': second_not_in_first,
        'first_newer': first_newer_than_in_second,
    }
