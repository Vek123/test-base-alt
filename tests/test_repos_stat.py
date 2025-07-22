__all__ = ()

import pytest

from alt_repos_stat import BranchPackageFilters


class TestBranchPackagesFilters:
    filters = BranchPackageFilters

    @pytest.mark.parametrize(
        ['a', 'b', 'expected'],
        [
            (
                [
                    {'name': '1'},
                    {'name': '2'},
                    {'name': '3'},
                ],
                [
                    {'name': '1'},
                    {'name': '2'},
                ],
                [
                    {'name': '3'},
                ],
            ),
            (
                [
                    {'name': '1'},
                    {'name': '2'},
                    {'name': '3'},
                ],
                [
                    {'name': '1'},
                    {'name': '3'},
                ],
                [
                    {'name': '2'},
                ],
            ),
            (
                [
                    {'name': '1'},
                    {'name': '2'},
                    {'name': '3'},
                ],
                [
                    {'name': '2'},
                    {'name': '3'},
                ],
                [
                    {'name': '1'},
                ],
            ),
        ],
    )
    def test_a_not_in_b(self, a, b, expected):
        res = self.filters.a_not_in_b(a, b)
        assert res == expected

    @pytest.mark.parametrize(
        ['criteria', 'a', 'b', 'expected'],
        [
            (
                ['name'],
                [
                    {'name': '1'},
                    {'name': '2'},
                    {'name': '3'},
                ],
                [
                    {'name': '1'},
                    {'name': '2'},
                    {'name': '3'},
                ],
                [
                    ({'name': '1'}, {'name': '1'}),
                    ({'name': '2'}, {'name': '2'}),
                    ({'name': '3'}, {'name': '3'}),
                ],
            ),
            (
                ['name', 'sub_name'],
                [
                    {'name': '1', 'sub_name': '11'},
                    {'name': '1', 'sub_name': '12'},
                    {'name': '1', 'sub_name': '13'},
                ],
                [
                    {'name': '1', 'sub_name': '11'},
                    {'name': '1', 'sub_name': '12'},
                    {'name': '1', 'sub_name': '13'},
                ],
                [
                    (
                        {'name': '1', 'sub_name': '11'},
                        {'name': '1', 'sub_name': '11'},
                    ),
                    (
                        {'name': '1', 'sub_name': '12'},
                        {'name': '1', 'sub_name': '12'},
                    ),
                    (
                        {'name': '1', 'sub_name': '13'},
                        {'name': '1', 'sub_name': '13'},
                    ),
                ],
            ),
        ],
    )
    def test_group_similar_packages_by_pair(self, criteria, a, b, expected):
        res = self.filters.group_similar_packages_by_pairs(a, b, criteria)
        assert res == expected

    @pytest.mark.parametrize(
        ['a', 'b', 'expected'],
        [
            (
                [
                    {'name': '1', 'version': '1.2.3', 'release': 'alt1'},
                    {'name': '2', 'version': '1.2.31', 'release': 'alt2'},
                    {'name': '3', 'version': '2.2.3', 'release': 'alt1_20201'},
                ],
                [
                    {'name': '1', 'version': '1.2.3', 'release': 'alt1'},
                    {'name': '2', 'version': '1.2.31', 'release': 'alt2'},
                    {'name': '3', 'version': '2.2.3', 'release': 'alt1_2020'},
                ],
                [
                    {'name': '3', 'version': '2.2.3', 'release': 'alt1_20201'},
                ],
            ),
            (
                [
                    {'name': '1', 'version': '1.2.3', 'release': 'alt1'},
                    {'name': '2', 'version': '1.2.31', 'release': 'alt2'},
                    {'name': '3', 'version': '2.2.3', 'release': 'alt1_2020'},
                ],
                [
                    {'name': '1', 'version': '1.2.3', 'release': 'alt1'},
                    {'name': '2', 'version': '1.2.30', 'release': 'alt2'},
                    {'name': '3', 'version': '2.2.3', 'release': 'alt1_2020'},
                ],
                [
                    {'name': '2', 'version': '1.2.31', 'release': 'alt2'},
                ],
            ),
            (
                [
                    {'name': '1', 'version': '1.2.1', 'release': 'alt1'},
                    {'name': '2', 'version': '1.2.31', 'release': 'alt2'},
                    {'name': '3', 'version': '200.2.3', 'release': 'alt1_202'},
                ],
                [
                    {'name': '1', 'version': '1.2.3', 'release': 'alt1'},
                    {'name': '2', 'version': '1.2.31', 'release': 'alt2'},
                    {'name': '3', 'version': '20.2.3', 'release': 'alt1_202'},
                ],
                [
                    {'name': '3', 'version': '200.2.3', 'release': 'alt1_202'},
                ],
            ),
        ],
    )
    def test_a_newer_version_release_than_b(self, a, b, expected):
        res = self.filters.a_newer_version_release_than_b(a, b)
        assert res == expected
