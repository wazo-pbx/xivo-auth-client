# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from xivo_lib_rest_client import RESTCommand


class UsersCommand(RESTCommand):

    resource = 'users'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_policy(self, user_uuid, policy_uuid):
        url = '{}/{}/policies/{}'.format(self.base_url, user_uuid, policy_uuid)

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def change_password(self, user_uuid, **kwargs):
        url = '/'.join([self.base_url, user_uuid, 'password'])

        r = self.session.put(url, headers=self.headers, data=json.dumps(kwargs))

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, user_uuid, tenant_uuid=None):
        headers = dict(self.headers)
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        url = '{}/{}'.format(self.base_url, user_uuid)

        r = self.session.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, user_uuid, **kwargs):
        headers = dict(self.headers)
        tenant_uuid = kwargs.pop('tenant_uuid', None)
        if tenant_uuid is not None:
            headers['Wazo-Tenant'] = tenant_uuid

        url = '{}/{}'.format(self.base_url, user_uuid)

        r = self.session.put(url, headers=headers, data=json.dumps(kwargs))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, user_uuid, tenant_uuid=None):
        headers = dict(self.headers)
        if tenant_uuid is not None:
            headers['Wazo-Tenant'] = tenant_uuid

        url = '{}/{}'.format(self.base_url, user_uuid)

        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_groups(self, user_uuid, **kwargs):
        return self._get_relation('groups', user_uuid, **kwargs)

    def get_policies(self, user_uuid, **kwargs):
        return self._get_relation('policies', user_uuid, **kwargs)

    def get_tenants(self, user_uuid, **kwargs):
        return self._get_relation('tenants', user_uuid, **kwargs)

    def list(self, **kwargs):
        headers = dict(self.headers)
        tenant_uuid = kwargs.pop('tenant_uuid', None)
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.get(
            self.base_url,
            headers=headers,
            params=kwargs,
        )

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def new(self, **kwargs):
        headers = dict(self.headers)
        tenant_uuid = kwargs.pop('tenant_uuid', self._client.tenant())
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.post(self.base_url, headers=headers, data=json.dumps(kwargs))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def register(self, **kwargs):
        url = '{}/register'.format(self.base_url)

        r = self.session.post(url, headers=self.headers, data=json.dumps(kwargs))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def remove_policy(self, user_uuid, policy_uuid):
        url = '{}/{}/policies/{}'.format(self.base_url, user_uuid, policy_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def request_confirmation_email(self, user_uuid, email_uuid):
        url = '{}/{}/emails/{}/confirm'.format(self.base_url, user_uuid, email_uuid)

        r = self.session.get(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def reset_password(self, **kwargs):
        url = '{}/password/reset'.format(self.base_url)

        r = self.session.get(url, headers=self.headers, params=kwargs)

        if r.status_code != 204:
            self.raise_from_response(r)

    def set_password(self, user_uuid, password, token=None):
        url = '{}/password/reset'.format(self.base_url)
        query_string = {'user_uuid': user_uuid}
        body = {'password': password}
        if token:
            self.session.headers['X-Auth-Token'] = token

        r = self.session.post(url, headers=self.headers, params=query_string, data=json.dumps(body))

        if r.status_code != 204:
            self.raise_from_response(r)

    def update_emails(self, user_uuid, emails):
        url = '{}/{}/emails'.format(self.base_url, user_uuid)

        body = {'emails': emails}

        r = self.session.put(url, headers=self.headers, data=json.dumps(body))
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def _get_relation(self, resource, user_uuid, **kwargs):
        url = '{}/{}/{}'.format(self.base_url, user_uuid, resource)

        r = self.session.get(url, headers=self.headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
