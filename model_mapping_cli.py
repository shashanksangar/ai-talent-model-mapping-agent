"""
AI Talent Operations - AI Model Mapping Agent CLI

Interactive command-line interface for mapping AI models to technical details and author profiles.
"""

import os
import sys
from typing import Dict, List, Optional
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from model_mapping_agent import ModelMappingAgent, ModelInfo, AuthorProfile
except ImportError:
    print("❌ Error: Could not import ModelMappingAgent. Make sure model_mapping_agent.py is in the same directory.")
    sys.exit(1)

console = Console()


class ModelMappingCLI:
    """Command-line interface for the Model Mapping Agent."""

    def __init__(self):
        """Initialize the CLI with the model mapping agent."""
        try:
            self.agent = ModelMappingAgent()
            self.current_menu = "main"
            console.print("[green]✅ Model Mapping Agent initialized successfully![/green]")
        except Exception as e:
            console.print(f"[red]❌ Failed to initialize Model Mapping Agent: {e}[/red]")
            sys.exit(1)

    def run(self):
        """Run the main CLI loop."""
        console.print(Panel.fit(
            "[bold blue]🧠 AI Model Mapping Agent[/bold blue]\n"
            "[dim]Map AI models to technical details and researcher profiles[/dim]\n"
            "[yellow]🔍 Discover: Technical summaries & Author online presence[/yellow]",
            title="Welcome"
        ))

        while True:
            try:
                if self.current_menu == "main":
                    self.show_main_menu()
                elif self.current_menu == "map":
                    self.show_mapping_interface()
                elif self.current_menu == "view":
                    self.show_view_menu()
                elif self.current_menu == "export":
                    self.show_export_menu()

            except KeyboardInterrupt:
                console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
                self.current_menu = "main"

    def show_main_menu(self):
        """Display the main menu."""
        console.print("\n[bold cyan]🧠 Main Menu[/bold cyan]")

        choices = [
            "🔍 Map AI Model",
            "👀 View Previous Mappings",
            "📤 Export Results",
            "ℹ️  About",
            "❌ Exit"
        ]

        choice = questionary.select(
            "Select an option:",
            choices=choices,
            pointer="▶"
        ).ask()

        if choice == "🔍 Map AI Model":
            self.current_menu = "map"
        elif choice == "👀 View Previous Mappings":
            self.current_menu = "view"
        elif choice == "📤 Export Results":
            self.current_menu = "export"
        elif choice == "ℹ️  About":
            self.show_about()
        elif choice == "❌ Exit":
            console.print("[yellow]👋 Goodbye![/yellow]")
            sys.exit(0)

    def show_mapping_interface(self):
        """Display the model mapping interface."""
        console.print("\n[bold cyan]🔍 Map AI Model[/bold cyan]")

        # Get model name
        model_name = questionary.text(
            "Enter AI model name (e.g., GPT-4, BERT, LLaMA-2):",
            validate=lambda x: len(x.strip()) > 0
        ).ask()

        if not model_name:
            self.current_menu = "main"
            return

        # Show progress
        console.print(f"\n[bold]🔍 Searching for model: {model_name}[/bold]")
        console.print("[dim]This may take a few moments...[/dim]")

        # Perform mapping
        result = self.agent.map_model(model_name.strip())

        if result:
            self.display_mapping_results(result)
        else:
            console.print(f"[red]❌ Could not find or map model: {model_name}[/red]")
            console.print("[dim]Try different variations or check spelling[/dim]")

        # Return to main menu
        input("\nPress Enter to continue...")
        self.current_menu = "main"

    def display_mapping_results(self, model_info: ModelInfo):
        """Display the mapping results in a formatted way."""
        console.print(f"\n[green]✅ Successfully mapped: {model_info.name}[/green]")

        # Technical Summary
        console.print("\n[bold cyan]📊 Technical Summary[/bold cyan]")
        console.print(Panel.fit(model_info.technical_summary))

        # Paper Information
        console.print("\n[bold cyan]📄 Paper Information[/bold cyan]")
        table = Table(show_header=False)
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        table.add_row("Title", model_info.paper_title)
        table.add_row("Published", model_info.publication_date)
        table.add_row("Categories", ", ".join(model_info.categories))
        table.add_row("arXiv URL", f"[link={model_info.paper_url}]{model_info.paper_url}[/link]")

        console.print(table)

        # Abstract (truncated)
        if model_info.abstract:
            abstract_preview = model_info.abstract[:300] + "..." if len(model_info.abstract) > 300 else model_info.abstract
            console.print("\n[bold cyan]📝 Abstract Preview[/bold cyan]")
            console.print(Panel.fit(abstract_preview))

        # Author Information
        console.print(f"\n[bold cyan]👥 Author Information ({len(model_info.authors)} authors)[/bold cyan]")

        for i, author in enumerate(model_info.authors, 1):
            if i == 1:
                console.print(f"\n[bold yellow]🥇 First Author: {author.name}[/bold yellow]")
                self.display_detailed_author_profile(author)
            else:
                console.print(f"\n[bold]#{i} {author.name}[/bold]")
                self.display_basic_author_profile(author)

    def display_detailed_author_profile(self, author: AuthorProfile):
        """Display detailed profile for the first author."""
        table = Table(show_header=False)
        table.add_column("Platform", style="cyan", no_wrap=True)
        table.add_column("Profile/Link", style="white")

        if author.homepage:
            table.add_row("🏠 Homepage", f"[link={author.homepage}]{author.homepage}[/link]")
        if author.scholar:
            citations = f" ({author.citations:,} citations)" if author.citations > 0 else ""
            table.add_row("🎓 Google Scholar", f"[link={author.scholar}]{author.scholar}{citations}[/link]")
        if author.github:
            table.add_row("💻 GitHub", f"[link={author.github}]{author.github}[/link]")
        if author.arxiv:
            table.add_row("📄 arXiv", f"[link={author.arxiv}]{author.arxiv}[/link]")
        if author.linkedin:
            table.add_row("💼 LinkedIn", f"[link={author.linkedin}]{author.linkedin}[/link]")
        if author.twitter:
            table.add_row("🐦 Twitter", f"[link={author.twitter}]{author.twitter}[/link]")
        if author.email:
            table.add_row("📧 Email", author.email)

        if table.rows:
            console.print(table)
        else:
            console.print("[dim]No online profiles found[/dim]")

    def display_basic_author_profile(self, author: AuthorProfile):
        """Display basic profile for other authors."""
        if author.arxiv:
            console.print(f"   📄 [link={author.arxiv}]arXiv publications[/link]")
        else:
            console.print("   [dim]No profile information available[/dim]")

    def show_view_menu(self):
        """Display the view menu."""
        console.print("\n[bold cyan]👀 View Previous Mappings[/bold cyan]")
        console.print("[dim]Previous mappings functionality coming soon...[/dim]")
        input("\nPress Enter to continue...")

    def show_export_menu(self):
        """Display the export menu."""
        console.print("\n[bold cyan]📤 Export Results[/bold cyan]")
        console.print("[dim]Export functionality coming soon...[/dim]")
        input("\nPress Enter to continue...")

    def show_about(self):
        """Show information about the agent."""
        console.print("\n[bold cyan]ℹ️  About AI Model Mapping Agent[/bold cyan]")
        console.print("""
This agent helps you discover and analyze AI models by:

🔍 [bold]Model Discovery:[/bold] Searches academic databases (arXiv) to find model papers
📊 [bold]Technical Analysis:[/bold] Generates summaries of model capabilities and architecture
👥 [bold]Author Profiling:[/bold] Maps researchers to their online presence
🔗 [bold]Profile Enrichment:[/bold] Links to GitHub, Google Scholar, personal websites

[bold]Supported Models:[/bold] GPT series, BERT, LLaMA, CLIP, ViT, T5, and more
[bold]Data Sources:[/bold] arXiv, Google Scholar, GitHub, academic homepages
        """)
        input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    try:
        cli = ModelMappingCLI()
        cli.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
