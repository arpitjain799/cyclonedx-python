# encoding: utf-8

# This file is part of CycloneDX Python Lib
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

import os
from unittest import TestCase

from cyclonedx_py.parser.pipenv import PipEnvFileParser


class TestPipEnvParser(TestCase):

    def test_simple(self) -> None:
        tests_pipfile_lock = os.path.join(os.path.dirname(__file__), 'fixtures/pipfile-lock-simple.txt')

        parser = PipEnvFileParser(pipenv_lock_filename=tests_pipfile_lock)
        self.assertEqual(2, parser.component_count())

        c_toml = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(c_toml)
        self.assertEqual('toml', c_toml.name)
        self.assertNotEqual(c_toml.purl.to_string(), c_toml.bom_ref.value)
        self.assertEqual('0.10.2', c_toml.version)
        self.assertEqual(2, len(c_toml.external_references), f'{c_toml.external_references}')
        self.assertEqual(1, len(c_toml.external_references.pop().hashes))
        c_property = next(filter(lambda p: p.name == 'cdx:pipenv:package:category', c_toml.properties), None)
        self.assertIsNotNone(c_property)
        self.assertEqual('default', c_property.value)

        c_flake8 = next(filter(lambda c: c.name == 'flake8', parser.get_components()), None)
        self.assertIsNotNone(c_flake8)
        self.assertEqual('flake8', c_flake8.name)
        self.assertNotEqual(c_flake8.purl.to_string(), c_flake8.bom_ref.value)
        self.assertEqual('3.7.9', c_flake8.version)
        self.assertEqual(2, len(c_flake8.external_references), f'{c_flake8.external_references}')
        self.assertEqual(1, len(c_flake8.external_references.pop().hashes))
        c_property = next(filter(lambda p: p.name == 'cdx:pipenv:package:category', c_flake8.properties), None)
        self.assertIsNotNone(c_property)
        self.assertEqual('develop', c_property.value)

    def test_simple_use_purl_bom_ref(self) -> None:
        tests_pipfile_lock = os.path.join(os.path.dirname(__file__), 'fixtures/pipfile-lock-simple.txt')

        parser = PipEnvFileParser(pipenv_lock_filename=tests_pipfile_lock,
                                  use_purl_bom_ref=True)
        self.assertEqual(2, parser.component_count())

        c_toml = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(c_toml)
        self.assertEqual('toml', c_toml.name)
        self.assertEqual(c_toml.purl.to_string(), c_toml.bom_ref.value)
        self.assertEqual('0.10.2', c_toml.version)
        self.assertEqual(2, len(c_toml.external_references), f'{c_toml.external_references}')
        self.assertEqual(1, len(c_toml.external_references.pop().hashes))
        c_property = next(filter(lambda p: p.name == 'cdx:pipenv:package:category', c_toml.properties), None)
        self.assertIsNotNone(c_property)
        self.assertEqual('default', c_property.value)

        c_flake8 = next(filter(lambda c: c.name == 'flake8', parser.get_components()), None)
        self.assertIsNotNone(c_flake8)
        self.assertEqual('flake8', c_flake8.name)
        self.assertEqual(c_flake8.purl.to_string(), c_flake8.bom_ref.value)
        self.assertEqual('3.7.9', c_flake8.version)
        self.assertEqual(2, len(c_flake8.external_references), f'{c_flake8.external_references}')
        self.assertEqual(1, len(c_flake8.external_references.pop().hashes))
        c_property = next(filter(lambda p: p.name == 'cdx:pipenv:package:category', c_flake8.properties), None)
        self.assertIsNotNone(c_property)
        self.assertEqual('develop', c_property.value)

    def test_with_multiple_and_no_index(self) -> None:
        tests_pipfile_lock = os.path.join(os.path.dirname(__file__), 'fixtures/pipfile-lock-no-index-example.txt')

        parser = PipEnvFileParser(pipenv_lock_filename=tests_pipfile_lock)
        self.assertEqual(3, parser.component_count())

        c_anyio = next(filter(lambda c: c.name == 'anyio', parser.get_components()), None)
        self.assertIsNotNone(c_anyio)
        self.assertEqual('anyio', c_anyio.name)
        self.assertEqual('3.3.3', c_anyio.version)
        self.assertEqual(2, len(c_anyio.external_references), f'{c_anyio.external_references}')
        self.assertEqual(1, len(c_anyio.external_references.pop().hashes))
        c_property = next(filter(lambda p: p.name == 'cdx:pipenv:package:category', c_anyio.properties), None)
        self.assertIsNotNone(c_property)
        self.assertEqual('default', c_property.value)

        c_toml = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(c_toml)
        self.assertEqual('toml', c_toml.name)
        self.assertEqual('0.10.2', c_toml.version)
        self.assertEqual(2, len(c_toml.external_references), f'{c_toml.external_references}')
        self.assertEqual(1, len(c_toml.external_references.pop().hashes))
        c_property = next(filter(lambda p: p.name == 'cdx:pipenv:package:category', c_toml.properties), None)
        self.assertIsNotNone(c_property)
        self.assertEqual('default', c_property.value)

        c_flake8 = next(filter(lambda c: c.name == 'flake8', parser.get_components()), None)
        self.assertIsNotNone(c_flake8)
        self.assertEqual('flake8', c_flake8.name)
        self.assertNotEqual(c_flake8.purl.to_string(), c_flake8.bom_ref.value)
        self.assertEqual('3.7.9', c_flake8.version)
        self.assertEqual(2, len(c_flake8.external_references), f'{c_flake8.external_references}')
        self.assertEqual(1, len(c_flake8.external_references.pop().hashes))
        c_property = next(filter(lambda p: p.name == 'cdx:pipenv:package:category', c_flake8.properties), None)
        self.assertIsNotNone(c_property)
        self.assertEqual('develop', c_property.value)
