#   Copyright Red Hat, Inc. All Rights Reserved.
#   Copyright 2015 OpenStack Foundation
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

import six
import logging


def get_dict_properties(item, fields, mixed_case_fields=[], formatters={}):
    """Return a tuple containing the item properties.
    :param item: a single dict resource
    :param fields: tuple of strings with the desired field names
    :param mixed_case_fields: tuple of field names to preserve case
    :param formatters: dictionary mapping field names to callables
       to format the values
    """
    row = []

    for field in fields:
        if field in mixed_case_fields:
            field_name = field.replace(' ', '_')
        else:
            field_name = field.lower().replace(' ', '_')
        data = item[field_name] if field_name in item else ''
        if field in formatters:
            row.append(formatters[field](data))
        else:
            row.append(data)
    return tuple(row)


def log_method(log, level=logging.DEBUG):
    """Logs a method and its arguments when entered."""

    def decorator(func):
        func_name = func.__name__

        @six.wraps(func)
        def wrapper(self, *args, **kwargs):
            if log.isEnabledFor(level):
                pretty_args = []
                if args:
                    pretty_args.extend(str(a) for a in args)
                if kwargs:
                    pretty_args.extend(
                        "%s=%s" % (k, v) for k, v in six.iteritems(kwargs))
                log.log(level, "%s(%s)", func_name, ", ".join(pretty_args))
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
