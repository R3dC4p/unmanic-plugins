#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from unmanic.libs.unplugins.settings import PluginSettings


class Settings(PluginSettings):
    settings = {
        "Patterns": "",
    }

    form_settings = {
        "patterns": {
            "input_type": "textarea",
        }
    }


def on_library_management_file_test(data):
    """
    Runner function - enables additional actions during the library management file tests.

    The 'data' object argument includes:
        path                            - String containing the full path to the file being tested.
        issues                          - List of currently found issues for not processing the file.
        add_file_to_pending_tasks       - Boolean, is the file currently marked to be added to the queue for processing.

    :param data:
    :return:

    """
    settings = Settings()

    regex_patterns = settings.get_setting('patterns')

    file_path = data.get('path')
    for regex_pattern in regex_patterns.splitlines():
        if not regex_pattern:
            continue

        pattern = re.compile(regex_pattern)
        if pattern.search(file_path):
            # Found a match
            data['add_file_to_pending_tasks'] = False
            data['issues'].append({
                'id':      'Path Ignore',
                'message': "File should be ignored because path '{}' matches the configured regex '{}'".format(
                    file_path, regex_pattern),
            })

    return data
