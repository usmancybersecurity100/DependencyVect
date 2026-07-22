import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel

from scanner.scanner import DependencyScanner
from reports.reporters import ReportGenerator
from utils.banner import print_banner
from utils.logger import setup_logger

logger = setup_logger(__name__)
console = Console()

def main():
    parser = argparse.ArgumentParser(description="DependencyVect - Software Supply Chain CVE Auditor")
    parser.add_argument("command", choices=["scan"], help="Action to perform")
    parser.add_argument("file", help="Path to dependency file (requirements.txt or package.json)")
    
    args = parser.parse_args()
    print_banner()

    target_file = Path(args.file)
    if not target_file.exists():
        console.print(f"[bold red][X] Error:[/bold red] File '{target_file}' not found.")
        sys.exit(1)

    scanner = DependencyScanner(str(target_file))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        scan_task = progress.add_task("[cyan]Scanning Dependencies...", total=100)
        
        try:
            # Run the scanner
            result = scanner.run_scan(progress, scan_task)
            
            progress.update(scan_task, description="[green]Generating Reports...", completed=100)
            
            # Generate Reports
            reporter = ReportGenerator(result)
            reporter.generate_all()

        except Exception as e:
            logger.exception("Fatal error during scan")
            console.print(f"\n[bold red][X] Fatal Error:[/bold red] {str(e)}")
            sys.exit(1)

    # UI Dashboard Output
    console.print("\n")
    
    # Risk Panel
    risk_color = "red" if result.risk_score >= 70 else "yellow" if result.risk_score >= 40 else "green"
    summary_text = f"Total Scanned: {result.total_dependencies} | Vulnerable: {result.vulnerable_dependencies} | Score: {result.risk_score}/100"
    console.print(Panel(summary_text, title=f"[{risk_color}]Risk Level: {result.risk_level}[/{risk_color}]", expand=False))

    # Vulnerability Table
    if result.vulnerable_dependencies > 0:
        table = Table(title="Detected Vulnerabilities", show_header=True, header_style="bold magenta")
        table.add_column("Package", style="cyan")
        table.add_column("Version", justify="right")
        table.add_column("CVE ID", style="red")
        table.add_column("Severity")

        for dep in result.dependencies:
            for v in dep.vulnerabilities:
                table.add_row(dep.name, dep.version, v.cve_id, v.severity)

        console.print(table)
    else:
        console.print("\n[bold green]✓ No known vulnerabilities detected in dependencies.[/bold green]")

    console.print(f"\n[bold blue]ⓘ Reports saved to output/ directory.[/bold blue]\n")

if __name__ == "__main__":
    main()
