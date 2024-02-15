"""Docker superset config."""
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# This is an example "local" configuration file. In order to set/override config
# options that ONLY apply to your local environment, simply copy/rename this file
# to docker/pythonpath/superset_config_docker.py
# It ends up being imported by docker/superset_config.py which is loaded by
# superset/config.py
#

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED: bool = False
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST: list = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT: int = 60 * 60 * 24 * 365


FEATURE_FLAGS = {"EMBEDDED_SUPERSET": True}

# Not sure, but seems this is required?
GUEST_ROLE_NAME = "Admin"

GUEST_TOKEN_JWT_EXP_SECONDS = 300  # 5 minutes, or you could set it longer


CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["*"],
}


ENABLE_PROXY_FIX = True


ENABLE_CORS = True

PUBLIC_ROLE_LIKE_GAMMA = True

TALISMAN_ENABLED = False
