"""Test responses."""
import pytest

from boilerplateapp.responses import (
    ok,
    created,
    accepted,
    no_content,
    bad_request,
    unauthorized,
    forbidden,
    not_found,
    method_not_allowed,
    conflict,
    unprocessable_entity,
)


class TestResponses:
    """Tests for boilerplateapp.responses."""

    @pytest.mark.parametrize('response', [ok, created, accepted, no_content, bad_request,
                                          unauthorized, forbidden, not_found,
                                          method_not_allowed, conflict, unprocessable_entity])
    def test_response_working_with_defaults(self, app, client, response):
        """All responses are working with default values."""
        json_response = response()
        assert json_response[1] >= 200

    @pytest.mark.parametrize('response', [bad_request, unauthorized, forbidden, not_found,
                                          method_not_allowed, conflict, unprocessable_entity])
    def test_response_with_custom_message(self, app, client, response):
        """Error respones can take custom messages."""
        arbitrary_message = 'important message'
        json_response = response(message=arbitrary_message)
        assert json_response[0].json['message'] == arbitrary_message
        assert json_response[1] >= 200

    @pytest.mark.parametrize('response', [ok, created, accepted])
    def test_response_with_data(self, app, client, response):
        """Some responses can take data."""
        arbitrary_data = 'my data'
        json_response = response(data=arbitrary_data)
        assert json_response[0].json == arbitrary_data
        assert json_response[1] >= 200
