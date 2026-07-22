from rich.console import Console

console = Console()

def print_banner():
    banner_text = """
    ██████╗ ███████╗██████╗ ███████╗███╗   ██╗██████╗ ███████╗ ██████╗████████╗
    ██╔══██╗██╔════╝██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝
    ██║  ██║█████╗  ██████╔╝█████╗  ██╔██╗ ██║██║  ██║█████╗  ██║      ╚══██║   
    ██║  ██║██╔══╝  ██╔═══╝ ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██║         ██║   
    ██████╔╝███████╗██║     ███████╗██║ ╚████║██████╔╝███████╗╚██████╗    ██║   
    ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   
    """
    console.print(f"[bold cyan]{banner_text}[/bold cyan]")
    console.print("[bold yellow]        Software Supply Chain CVE Auditor[/bold yellow]")
    console.print("[dim]        Created by: USMAN ALI[/dim]")
    console.print("[dim]        Developed for DevSecOps & Security Assessment[/dim]\n")

if __name__ == "__main__":
    print_banner()
