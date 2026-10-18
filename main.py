
from pathlib import Path
from analyzer import count_events

# Find files next to this script
project_dir = Path(__file__).parent
log_file = project_dir / "security.log"
report_file = project_dir / "report.txt"

# Read and analyze the log
try:
    with log_file.open("r", encoding="utf-8") as file:
        counts, error_lines, unknown_lines = count_events(file)

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
