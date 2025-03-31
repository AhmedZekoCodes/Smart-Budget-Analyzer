# budget_reporting.py
class ReportGenerator:
    def generate_report(self, report_data):
        report_lines = []
        report_lines.append("="*40)
        report_lines.append("            Budget Analysis Report")
        report_lines.append("="*40)
        for key, value in report_data.items():
            # Format lists nicely if necessary.
            if isinstance(value, list):
                value = "\n    - " + "\n    - ".join(str(item) for item in value)
            report_lines.append(f"{key:<20}: {value}")
        report_lines.append("="*40)
        return "\n".join(report_lines)

class Visualizer:
    def plot_report(self, report_data):
        # Aesthetic text-based visualization with headers.
        print("\n" + "*" * 50)
        print("***** BUDGET ANALYSIS SUMMARY *****")
        print("*" * 50)
        for key, value in report_data.items():
            if isinstance(value, list):
                print(f"{key:<20}:")
                for item in value:
                    print(f"   - {item}")
            else:
                print(f"{key:<20}: {value}")
        print("*" * 50 + "\n")
