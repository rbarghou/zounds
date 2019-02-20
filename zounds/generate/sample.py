import pandas as pd
import numpy as np
import librosa

feeds_df = pd.read_csv("./feeds.csv", index_col=0)


def get_random_sample(sample_duration):
    for _ in range(10):
        idx = np.random.choice(feeds_df[feeds_df.exists].index)
        entry_path = feeds_df["path"][idx]
        entry_duration = librosa.core.get_duration(filename=entry_path)
        if entry_duration > sample_duration + 1:
            offset = np.random.random() * (entry_duration - sample_duration)
            return librosa.load(entry_path,
                                offset=offset,
                                duration=sample_duration)
    raise ValueError("I tried to find audio that was long enough for your"
                     " specified sample_duration, but I couldn't.  Maybe"
                     " you specified too long a duration?"
                     " It was {}".format(sample_duration))

