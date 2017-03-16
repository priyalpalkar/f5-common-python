# coding=utf-8
#
# Copyright 2015-2017 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""BIG-IP® Advanced Firewall Manager™ (AFM®) module.

REST URI
    ``http://localhost/mgmt/tm/security/firewall``

GUI Path
    ``Security --> Network Firewall``

REST Kind
    ``tm:security:firewall:*``
"""
from f5.bigip.resource import _minimum_one_is_missing
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource

from distutils.version import LooseVersion


class Firewall(OrganizingCollection):
    """BIG-IP® AFM® Firewall organizing collection."""

    def __init__(self, security):
        super(Firewall, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [Address_Lists]


class Address_Lists(Collection):
    """BIG-IP® AFM® Address List collection"""
    def __init__(self, firewall):
        super(Address_Lists, self).__init__(firewall)
        self._meta_data['allowed_lazy_attributes'] = [Address_List]
        self._meta_data['attribute_registry'] = \
            {'tm:security:firewall:address-list:address-liststate':
                Address_List}


class Address_List(Resource):
    """BIG-IP® Address List resource"""
    def __init__(self, address_lists):
        super(Address_List, self).__init__(address_lists)
        self._meta_data['required_json_kind'] = \
            'tm:security:firewall:address-list:address-liststate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self.tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']

    def create(self, **kwargs):
        """Custom create method to accommodate different endpoint behavior."""
        self._check_create_parameters(**kwargs)
        if LooseVersion(self.tmos_ver) < LooseVersion('12.0.0'):
            req_set = {'addressLists', 'addresses', 'geo'}
        else:
            req_set = {'addressLists', 'addresses', 'geo', 'fqdns'}
        _minimum_one_is_missing(req_set, **kwargs)
        return self._create(**kwargs)
