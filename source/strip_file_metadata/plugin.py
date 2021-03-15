#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unmanic.libs.unplugins.settings import PluginSettings


class Settings(PluginSettings):
    settings = {}


def on_worker_process(data):
    """
    Runner function - carries out additional processing during the worker stages of a task.

    The 'data' object argument includes:
        exec_ffmpeg             - Boolean, should Unmanic run FFMPEG with the data returned from this plugin.
        file_probe              - A dictionary object containing the current file probe state.
        ffmpeg_args             - A list of Unmanic's default FFMPEG args.
        file_in                 - The source file to be processed by the FFMPEG command.
        file_out                - The destination that the FFMPEG command will output.

    :param data:
    :return:
    """
    # Default to no FFMPEG command required. This prevents the FFMPEG command from running if it is not required
    data['exec_ffmpeg'] = False

    # Check file probe for title metadata in the video
    file_probe = data.get('file_probe')

    # First check the format
    probe_format = file_probe.get('format')
    if probe_format:
        # Check if tags exist in format with the key "title" or "language"
        format_tags = probe_format.get('tags')
        if format_tags and True in list(k.lower() in ['title', 'language'] for k in format_tags):
            data['exec_ffmpeg'] = True

    # Next check streams (if required)
    if not data['exec_ffmpeg']:
        probe_streams = file_probe.get('streams')
        for probe_stream in probe_streams:
            # Check if tags exist in streams with the key "title" or "language"
            stream_tags = probe_stream.get('tags')
            if stream_tags and True in list(k.lower() in ['title', 'language'] for k in stream_tags):
                data['exec_ffmpeg'] = True

    if data['exec_ffmpeg']:
        # Add FFMPEG args
        data['ffmpeg_args'] = [
            '-i',
            data.get('file_in'),
            '-hide_banner',
            '-loglevel',
            'info',
            '-map_metadata', '-1', '-map', '0', '-c', 'copy',
            '-y',
            data.get('file_out'),
        ]

    return data
