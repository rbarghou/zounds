#
# Command line use of 'ffprobe':
#
# ffprobe -loglevel quiet -print_format json \
#         -show_format    -show_streams \
#         video-file-name.mp4
#
# man ffprobe # for more information about ffprobe
#

import subprocess as sp
import json


def probe(media_file_path):
    ''' Give a json from ffprobe command line

    @media_file_path : The absolute (full) path of the video file, string.
    '''
    if type(media_file_path) != str:
        raise Exception('Gvie ffprobe a full file path of the video')
        return

    command = ("ffprobe -loglevel quiet -print_format json -show_format"
               " -show_streams".split()) + [media_file_path]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    return json.loads(str(out, 'utf8'))


def duration(media_file_path):
    """
    Video's duration in seconds, return a float number
    :param media_file_path:
    :return float duration:
    """
    if not media_file_path:
        return None
    try:
        _json = probe(media_file_path)
        if 'format' in _json:
            if 'duration' in _json['format']:
                return float(_json['format']['duration'])

        if 'streams' in _json:
            # commonly stream 0 is the video
            for s in _json['streams']:
                if 'duration' in s:
                    return float(s['duration'])
        return None
    except:
        return None

