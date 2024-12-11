from pathlib import Path

with Path("day-8/test.txt").open() as f:
    data = f.read()

with Path("day-8/test-answer.txt").open() as f:
    answer = f.read()

print(data == answer)
