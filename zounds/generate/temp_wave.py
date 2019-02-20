from contextlib import contextmanager
import subprocess
import os
import shutil
import tempfile

import numpy as np
import librosa


@contextmanager
def temp_wave(in_fp):
    outfile = in_fp + ".tmp.wav"
    try:
        subprocess.run([
            'ffmpeg', '-i', in_fp, outfile],
            check=True
        )
        yield outfile
    finally:
        os.remove(outfile)


def gen_wave_splits(in_fp, segment_duration, tqdm=None):
    tmp_dir = tempfile.mkdtemp()
    duration = librosa.get_duration(filename=in_fp)
    starts = np.arange(0, duration, segment_duration)
    if tqdm:
        starts = tqdm(starts)

    tmp_files = []
    try:
        for start in starts:
            tmp_file = os.path.join(tmp_dir, "segment_" + str(start) + ".wav")
            tmp_files.append(tmp_file)
            result = subprocess.run(["ffmpeg",
                                     "-ss", str(start),
                                     "-t", str(segment_duration),
                                     "-i", in_fp, tmp_file,
                                     ],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            yield tmp_file

    finally:
        print("Removing temp directory: " + tmp_dir)
        shutil.rmtree(tmp_dir)

