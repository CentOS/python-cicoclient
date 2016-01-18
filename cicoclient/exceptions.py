#   Copyright Red Hat, Inc. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#


class ApiKeyRequired(Exception):
    """
    When running a command that requires an api key and the api key is not
    provided
    """
    def __str__(self):
        return "The requested operation requires an API key."


class NoInventory(Exception):
    """
    When requesting nodes from Duffy and no inventory is available
    """
    def __str__(self):
        return "The requested operation failed as no inventory is available."


class SsidRequired(Exception):
    """
    When running a command that requires an api key and the api key is not
    provided
    """
    def __str__(self):
        return "The requested operation requires a SSID."
