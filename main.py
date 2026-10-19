
from pathlib import Path
from analyzer import count_events, find_repeated_failed_logins, calculate_risk

# Find files next to this script
project_dir = Path(__file__).parent
log_file = project_dir / "security.log"
report_file = project_dir / "report.txt"

# Read and analyze the log
try:
    with log_file.open("r", encoding="utf-8") as file:
        log_lines = file.readlines()

        counts, error_lines, unknown_lines = count_events(log_lines)
        repeated_logins = find_repeated_failed_logins(log_lines)

except OSError as error:
    print(f"Could not read log file: {error}")
    raise SystemExit(1)

# Prepare the report
total_events = sum(counts.values())

report_lines = [
    "=== Security Log Analyzer ===",
    f"Total recognized events: {total_events}",
    f"Unknown lines: {len(unknown_lines)}",
    "",
]

for event_type, total in counts.items():
    report_lines.append(f"{event_type}: {total}")


report_lines.extend(["", "=== Event risk levels ==="])

for line in log_lines:
    line = line.strip()

    if not line:
        continue

    if line.startswith("[INFO]"):
        event_type = "INFO"
    elif line.startswith("[WARNING]"):
        event_type = "WARNING"
    elif line.startswith("[ERROR]"):
        event_type = "ERROR"
    else:
        event_type = "UNKNOWN"

    message = line.split("]", 1)[1].strip() if "]" in line else line
    risk = calculate_risk(event_type, message)

    report_lines.append(f"{risk}: {line}")


report_lines.extend(["", "=== Errors found ==="])

if error_lines:
    report_lines.extend(error_lines)
else:
    report_lines.append("No errors found.")

if unknown_lines:
    report_lines.extend(["", "=== Unknown events ==="])
    report_lines.extend(unknown_lines)

if total_events == 0 and not unknown_lines:
    report_lines.extend(["", "The log file is empty."])

report_lines.extend(["","=== Repeated failed logins ==="])

if repeated_logins:
    for username,attempts in repeated_logins.items():
        report_lines.append(
            f"Repeated failed logins detected for user {username}"
        )
        report_lines.append(f"Failed attempts: {attempts}")
else:
    report_lines.append("No repeated failed logins detected.")


# Display the report
print("\n".join(report_lines))

# Save the report
try:
    report_file.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8"
    )
    print(f"\nReport saved to: {report_file.name}")

except OSError as error:
    print(f"Could not save report: {error}")
    raise SystemExit(1)
