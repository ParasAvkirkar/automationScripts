import re
import numpy as np
import matplotlib.pyplot as plt


def get_min_max(scores):
    min = float("inf")
    max = 0
    for score in scores:
        if min >= score[1]:
            min = score[1]
        if max <= score[1]:
            max = score[1]

    return min, max


def smooth_scores(scores, window_size=5):
    new_scores = []
    curr_sum = 0.0
    for i in range(window_size):
        curr_sum += scores[i][1]
        new_scores.append((i+1, curr_sum/(i+1)))

    for i in range(window_size, len(scores)):
        curr_sum -= scores[i-window_size][1]
        curr_sum += scores[i][1]
        new_scores.append((i+1, curr_sum/window_size))

    return new_scores


text = ""
with open("scoreinput.txt", "r") as f:
    for line in f:
        text = text + " " + line

# [0-9]\s*(\r\n|\r|\n)[0-9]+\swpm
matches = re.findall("[0-9]+\s+[0-9]+\s+wpm", text)
print(str(matches[-10:]))
scores = {}
for m in matches:
    m = m.strip("wpm")
    m = m.strip()
    m = re.split("\s+", m)
    scores[int(m[0])] = float(m[1])

scores = scores.items()
scores = sorted(scores, key=lambda tuple: tuple[0])

print(str(scores[-10:]))
min, max = get_min_max(scores)
scores = smooth_scores(scores, 20)

plt.plot([score[0] for score in scores], [score[1] for score in scores])

plt.yticks(np.arange(min, max, 5))

plt.show()

