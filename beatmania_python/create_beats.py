import librosa
import math

def beat_array(file_name, difficulty):
    wait = 5
    if difficulty == 'easy':
        wait = 20
    else:
        wait = 5

    y, sr = librosa.load(file_name, mono=True)
    o_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(o_env, sr=sr)
    peaks = librosa.util.peak_pick(o_env, pre_max=7, post_max=7, pre_avg=7, post_avg=7, delta=0.5, wait=wait)

    o = o_env.tolist()
    t = times.tolist()
    p = peaks.tolist()

    onsets = []
    beat_time = []

    for peak_index in p:
        onsets.append(o[peak_index])
        beat_time.append(t[peak_index])

    o_max = max(onsets)
    o_min = min(onsets)
    o_avg = (sum(onsets) / len(onsets)) - 0.5

    lower_section = (o_avg - o_min) / 12
    upper_section = (o_max - o_avg) / 24

    def low_section(size):
        return o_min + (lower_section * size)

    def high_section(size):
        return o_avg + (upper_section * size)

    beatmap = []

    total_a = 0
    total_b = 0
    total_c = 0
    total_d = 0
    total_e = 0
    total_f = 0

    time = 0

    for idx, o in enumerate(onsets):
        time = round(beat_time[idx] * 1000)

        if time <= 2500:
            continue

        if o < low_section(8):
            total_a += 1
            beatmap.append(
                {
                    'position': 1,
                    'time': time
                }
            )
        elif low_section(8) <= o < low_section(10):
            total_b += 1
            beatmap.append(
                {
                    'position': 2,
                    'time': time
                }
            )
        elif low_section(10) <= o < o_avg:
            total_c += 1
            beatmap.append(
                {
                    'position': 3,
                    'time': time
                }
            )
        elif o_avg <= o < high_section(1):
            total_d += 1
            beatmap.append(
                {
                    'position': 4,
                    'time': time
                }
            )
        elif high_section(1) <= o < high_section(3):
            total_e += 1
            beatmap.append(
                {
                    'position': 5,
                    'time': time
                }
            )
        elif o >= high_section(3):
            total_f += 1
            beatmap.append(
                {
                    'position': 6,
                    'time': time
                }
            )

    print(f"Total notes: {len(onsets)}")
    print(f"Total A: {total_a}")
    print(f"Total B: {total_b}")
    print(f"Total C: {total_c}")
    print(f"Total D: {total_d}")
    print(f"Total E: {total_e}")
    print(f"Total F: {total_f}")

    duration = librosa.get_duration(y=y, sr=sr)
    ending = (math.ceil(duration) * 1000) + 2500

    return beatmap, ending