# coding: utf-8

"""
    AIS

    AIStore is a scalable object-storage based caching system with Amazon and Google Cloud backends.  # noqa: E501

    OpenAPI spec version: 1.1.0
    Contact: dfcdev@exchange.nvidia.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from openapi_client.api_client import ApiClient


class SortApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def abort_sort(self, sort_uuid, **kwargs):  # noqa: E501
        """Abort distributed sort operation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.abort_sort(sort_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str sort_uuid: Sort uuid which is returned when starting dsort (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.abort_sort_with_http_info(sort_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.abort_sort_with_http_info(sort_uuid, **kwargs)  # noqa: E501
            return data

    def abort_sort_with_http_info(self, sort_uuid, **kwargs):  # noqa: E501
        """Abort distributed sort operation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.abort_sort_with_http_info(sort_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str sort_uuid: Sort uuid which is returned when starting dsort (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sort_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method abort_sort" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sort_uuid' is set
        if ('sort_uuid' not in local_var_params or
                local_var_params['sort_uuid'] is None):
            raise ValueError("Missing the required parameter `sort_uuid` when calling `abort_sort`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'sort_uuid' in local_var_params:
            path_params['sort-uuid'] = local_var_params['sort_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/sort/abort/{sort-uuid}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_sort_metrics(self, sort_uuid, **kwargs):  # noqa: E501
        """Get metrics of given sort operation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_sort_metrics(sort_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str sort_uuid: Sort uuid which is returned when starting dsort (required)
        :return: dict(str, object)
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_sort_metrics_with_http_info(sort_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_sort_metrics_with_http_info(sort_uuid, **kwargs)  # noqa: E501
            return data

    def get_sort_metrics_with_http_info(self, sort_uuid, **kwargs):  # noqa: E501
        """Get metrics of given sort operation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_sort_metrics_with_http_info(sort_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str sort_uuid: Sort uuid which is returned when starting dsort (required)
        :return: dict(str, object)
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sort_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_sort_metrics" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sort_uuid' is set
        if ('sort_uuid' not in local_var_params or
                local_var_params['sort_uuid'] is None):
            raise ValueError("Missing the required parameter `sort_uuid` when calling `get_sort_metrics`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'sort_uuid' in local_var_params:
            path_params['sort-uuid'] = local_var_params['sort_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/sort/metrics/{sort-uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='dict(str, object)',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def start_sort(self, sort_spec, **kwargs):  # noqa: E501
        """Starts distributed sort operation on cluster  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.start_sort(sort_spec, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SortSpec sort_spec: (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.start_sort_with_http_info(sort_spec, **kwargs)  # noqa: E501
        else:
            (data) = self.start_sort_with_http_info(sort_spec, **kwargs)  # noqa: E501
            return data

    def start_sort_with_http_info(self, sort_spec, **kwargs):  # noqa: E501
        """Starts distributed sort operation on cluster  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.start_sort_with_http_info(sort_spec, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SortSpec sort_spec: (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sort_spec']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method start_sort" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sort_spec' is set
        if ('sort_spec' not in local_var_params or
                local_var_params['sort_spec'] is None):
            raise ValueError("Missing the required parameter `sort_spec` when calling `start_sort`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'sort_spec' in local_var_params:
            body_params = local_var_params['sort_spec']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/sort/start', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
