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


class BucketApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete(self, bucket_name, input_parameters, **kwargs):  # noqa: E501
        """Delete operations on bucket and its contained objects  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete(bucket_name, input_parameters, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bucket_name: Bucket name (required)
        :param InputParameters input_parameters: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_with_http_info(bucket_name, input_parameters, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_with_http_info(bucket_name, input_parameters, **kwargs)  # noqa: E501
            return data

    def delete_with_http_info(self, bucket_name, input_parameters, **kwargs):  # noqa: E501
        """Delete operations on bucket and its contained objects  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_with_http_info(bucket_name, input_parameters, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bucket_name: Bucket name (required)
        :param InputParameters input_parameters: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['bucket_name', 'input_parameters']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'bucket_name' is set
        if ('bucket_name' not in local_var_params or
                local_var_params['bucket_name'] is None):
            raise ValueError("Missing the required parameter `bucket_name` when calling `delete`")  # noqa: E501
        # verify the required parameter 'input_parameters' is set
        if ('input_parameters' not in local_var_params or
                local_var_params['input_parameters'] is None):
            raise ValueError("Missing the required parameter `input_parameters` when calling `delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'bucket_name' in local_var_params:
            path_params['bucket-name'] = local_var_params['bucket_name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'input_parameters' in local_var_params:
            body_params = local_var_params['input_parameters']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/buckets/{bucket-name}', 'DELETE',
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

    def get_properties(self, bucket_name, **kwargs):  # noqa: E501
        """Query bucket properties  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_properties(bucket_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bucket_name: Bucket name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_properties_with_http_info(bucket_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_properties_with_http_info(bucket_name, **kwargs)  # noqa: E501
            return data

    def get_properties_with_http_info(self, bucket_name, **kwargs):  # noqa: E501
        """Query bucket properties  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_properties_with_http_info(bucket_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bucket_name: Bucket name (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['bucket_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_properties" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'bucket_name' is set
        if ('bucket_name' not in local_var_params or
                local_var_params['bucket_name'] is None):
            raise ValueError("Missing the required parameter `bucket_name` when calling `get_properties`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'bucket_name' in local_var_params:
            path_params['bucket-name'] = local_var_params['bucket_name']  # noqa: E501

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
            '/buckets/{bucket-name}', 'HEAD',
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

    def list_names(self, **kwargs):  # noqa: E501
        """Get bucket names  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_names(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool loc: Get only local bucket names
        :return: BucketNames
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_names_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_names_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_names_with_http_info(self, **kwargs):  # noqa: E501
        """Get bucket names  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_names_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool loc: Get only local bucket names
        :return: BucketNames
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['loc']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_names" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'loc' in local_var_params:
            query_params.append(('loc', local_var_params['loc']))  # noqa: E501

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
            '/buckets/*', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BucketNames',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def perform_operation(self, bucket_name, input_parameters, **kwargs):  # noqa: E501
        """Perform operations on bucket such as create  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.perform_operation(bucket_name, input_parameters, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bucket_name: Bucket name (required)
        :param InputParameters input_parameters: (required)
        :return: ObjectPropertyList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.perform_operation_with_http_info(bucket_name, input_parameters, **kwargs)  # noqa: E501
        else:
            (data) = self.perform_operation_with_http_info(bucket_name, input_parameters, **kwargs)  # noqa: E501
            return data

    def perform_operation_with_http_info(self, bucket_name, input_parameters, **kwargs):  # noqa: E501
        """Perform operations on bucket such as create  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.perform_operation_with_http_info(bucket_name, input_parameters, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bucket_name: Bucket name (required)
        :param InputParameters input_parameters: (required)
        :return: ObjectPropertyList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['bucket_name', 'input_parameters']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method perform_operation" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'bucket_name' is set
        if ('bucket_name' not in local_var_params or
                local_var_params['bucket_name'] is None):
            raise ValueError("Missing the required parameter `bucket_name` when calling `perform_operation`")  # noqa: E501
        # verify the required parameter 'input_parameters' is set
        if ('input_parameters' not in local_var_params or
                local_var_params['input_parameters'] is None):
            raise ValueError("Missing the required parameter `input_parameters` when calling `perform_operation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'bucket_name' in local_var_params:
            path_params['bucket-name'] = local_var_params['bucket_name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'input_parameters' in local_var_params:
            body_params = local_var_params['input_parameters']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/buckets/{bucket-name}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ObjectPropertyList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def set_properties(self, bucket_name, input_parameters, **kwargs):  # noqa: E501
        """Set bucket properties  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.set_properties(bucket_name, input_parameters, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bucket_name: Bucket name (required)
        :param InputParameters input_parameters: (required)
        :param str cloud_provider: Bucket's cloud provider
        :param str next_tier_url: URL for the next tier
        :param RWPolicy read_policy: Policy which defines how to perform reads in case of more tiers
        :param RWPolicy write_policy: Policy which defines how to perform writes in case of more tiers
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.set_properties_with_http_info(bucket_name, input_parameters, **kwargs)  # noqa: E501
        else:
            (data) = self.set_properties_with_http_info(bucket_name, input_parameters, **kwargs)  # noqa: E501
            return data

    def set_properties_with_http_info(self, bucket_name, input_parameters, **kwargs):  # noqa: E501
        """Set bucket properties  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.set_properties_with_http_info(bucket_name, input_parameters, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bucket_name: Bucket name (required)
        :param InputParameters input_parameters: (required)
        :param str cloud_provider: Bucket's cloud provider
        :param str next_tier_url: URL for the next tier
        :param RWPolicy read_policy: Policy which defines how to perform reads in case of more tiers
        :param RWPolicy write_policy: Policy which defines how to perform writes in case of more tiers
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['bucket_name', 'input_parameters', 'cloud_provider', 'next_tier_url', 'read_policy', 'write_policy']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method set_properties" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'bucket_name' is set
        if ('bucket_name' not in local_var_params or
                local_var_params['bucket_name'] is None):
            raise ValueError("Missing the required parameter `bucket_name` when calling `set_properties`")  # noqa: E501
        # verify the required parameter 'input_parameters' is set
        if ('input_parameters' not in local_var_params or
                local_var_params['input_parameters'] is None):
            raise ValueError("Missing the required parameter `input_parameters` when calling `set_properties`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'bucket_name' in local_var_params:
            path_params['bucket-name'] = local_var_params['bucket_name']  # noqa: E501

        query_params = []
        if 'cloud_provider' in local_var_params:
            query_params.append(('cloud_provider', local_var_params['cloud_provider']))  # noqa: E501
        if 'next_tier_url' in local_var_params:
            query_params.append(('next_tier_url', local_var_params['next_tier_url']))  # noqa: E501
        if 'read_policy' in local_var_params:
            query_params.append(('read_policy', local_var_params['read_policy']))  # noqa: E501
        if 'write_policy' in local_var_params:
            query_params.append(('write_policy', local_var_params['write_policy']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'input_parameters' in local_var_params:
            body_params = local_var_params['input_parameters']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/buckets/{bucket-name}', 'PUT',
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
