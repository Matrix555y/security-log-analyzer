
from pathlib import Path

log_file = Path(__file__).parent / "security.log"

counts = {
    "INFO": 0,
    "WARNING": 0,
    "ERROR": 0
}

error_lines = []
unknown_lines = []

try:
    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
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

except OSError as error:
    print(f"Could not read log file: {error}")
    raise SystemExit(1)

total_events = sum(counts.values())

print("=== Security Log Analyzer ===")
print(f"Total recognized events: {total_events}")
print(f"Unknown lines: {len(unknown_lines)}")
print()

for event_type, total in counts.items():
    print(f"{event_type}: {total}")

print("\n=== Errors found ===")

if error_lines:
    for error in error_lines:
        print(error)
else:
    print("No errors found.")

if unknown_lines:
    print("\n=== Unknown events ===")
    for line in unknown_lines:
        print(line)

if total_events == 0 and not unknown_lines:
    print("\nThe log file is empty.")



report_file = Path(__file__).parent /"report.txt"

with report_file.open("w", encoding="utf-8") as file: 
    file.write("=== Security Log Analyzer ===\n")
    file.write(f"Total recognized events: {total_events}\n")
    file.write(f"Unknown lines: {len(unknown_lines)}\n\n")

    for event_type, total in counts.items():
        file.write(f"{event_type}: {total}\n")

    file.write("\n=== Errors found ===\n")

    for error in error_lines:
        file.write(error + "\n")


    if unknown_lines:
        file.write("\n === Unknown events ===\n")
        for line in unknown_lines:
            file.write(line + "\n")

print(f"\nReport saved to: {report_file.name}")