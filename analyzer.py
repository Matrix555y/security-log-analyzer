
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


def find_repeated_failed_logins(log_lines, threshold=3):
    failed_logins ={}

    for line in log_lines:
        line =line.strip()

        marker = "Failed login for user "


        if marker in line:
            username = line.split(marker,1)[1].strip()

            if username:
                failed_logins[username] = failed_logins.get(username,0)+1

    repeated_logins = {}

    for username, attempts in failed_logins.items():
        if attempts >= threshold:
            repeated_logins[username]= attempts

    return repeated_logins 




def calculate_risk(event_type, message=""):
    if event_type == "INFO":
        return "LOW"

    elif event_type == "WARNING":
        return "MEDIUM"

    elif event_type == "ERROR":
        if "Failed login" in message:
            return "HIGH"
        else:
            return "MEDIUM"

    else:
        return "UNKNOWN"



