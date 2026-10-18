
def count_events(log_lines):
    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
    }

    error_lines = []
    unknown_lines = []

    for line in log_lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("[INFO]"):
            counts["INFO"] += 1

        elif line.startswith("[WARNING]"):
            counts["WARNING"] += 1

        elif line.startswith("[ERROR]"):
            counts["ERROR"] += 1
            error_lines.append(line)

        else:
            unknown_lines.append(line)

    return counts, error_lines, unknown_lines
