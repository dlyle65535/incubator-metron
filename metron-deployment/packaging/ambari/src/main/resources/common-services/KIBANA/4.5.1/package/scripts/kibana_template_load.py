#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl
from resource_management.libraries.functions import format
from dashboard.dashboardindex import DashboardIndex
import errno
import os

@OsFamilyFuncImpl(os_family=OsFamilyImpl.DEFAULT)
def loadkibanatemplate(env):

    hostname = format("{es_host}")
    port = int(format("{es_port}"))

    print("Connecting to Elasticsearch on host: %s, port: %s" % (hostname,port))
    di = DashboardIndex(host=hostname,port=port)

    #Loads Kibana Dashboard definition from disk and replaces .kibana on index
    templateFile = './cache/common-services/KIBANA/4.5.1/package/scripts/dashboard/dashboard.p'
    if not os.path.isfile(templateFile):
        raise IOError(
            errno.ENOENT, os.strerror(errno.ENOENT), templateFile)

    print("Deleting .kibana index from Elasticsearch")
    di.es.indices.delete(index='.kibana', ignore=[400, 404])

    print("Loading .kibana index from %s" % templateFile)
    di.put(data=di.load(filespec=templateFile))
