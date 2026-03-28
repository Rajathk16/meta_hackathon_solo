# grader.py

def grade(state):
    total = len(state["emails"])
    correct = state.get("correct_resolutions", 0)
    steps = state["steps"]

    if total == 0:
        return 0.0

    accuracy = correct / total
    efficiency = max(0, 1 - steps / 10)

    score = (0.7 * accuracy) + (0.3 * efficiency)

    return round(score, 2)