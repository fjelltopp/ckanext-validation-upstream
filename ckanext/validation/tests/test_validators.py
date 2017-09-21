import json

from nose.tools import assert_raises, assert_equals

from ckantoolkit import Invalid

from ckanext.validation.validators import resource_schema_validator


class TestValidators(object):

    def test_resource_schema_none(self):

        schema = ''

        assert resource_schema_validator(schema, {}) is None

    def test_resource_schema_invalid_json_string(self):

        schema = '{a,b}'

        assert_raises(Invalid, resource_schema_validator, schema, {})

    def test_resource_schema_invalid_schema_string(self):

        schema = '{"a": 1}'

        assert_raises(Invalid, resource_schema_validator, schema, {})

    def test_resource_schema_invalid_schema_object(self):

        schema = {'a': 1}

        with assert_raises(Invalid) as e:
            resource_schema_validator(schema, {})

        assert_equals(
            e.exception.error,
            'Invalid Table Schema: u\'fields\' is a required property')

    def test_resource_schema_valid_schema_object(self):

        schema = {'fields': [{'name': 'longitude'}]}

        value = resource_schema_validator(schema, {})

        assert_equals(value, json.dumps(schema))

    def test_resource_schema_valid_schema_string(self):

        schema = '{"fields": [{"name": "longitude"}]}'

        value = resource_schema_validator(schema, {})

        assert_equals(value, schema)
