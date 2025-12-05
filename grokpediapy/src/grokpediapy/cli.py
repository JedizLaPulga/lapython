"""
Command Line Interface for grokpediapy.
Uses Typer for argument parsing and Rich for formatting.
"""
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from typing_extensions import Annotated

from grokpediapy.core import fetch_article, ContentRetrievalError

# Initialize Typer app and Rich console
app = typer.Typer(add_completion=False)
console = Console()

@app.command()
def get(
    topic: Annotated[str, typer.Argument(help="The topic to retrieve from Grokpedia.")]
):
    """
    Retrieve and display a summary of a topic from Grokpedia.
    """
    console.print(f"[bold cyan]Searching Grokpedia for:[/bold cyan] [yellow]{topic}[/yellow]...")

    try:
        content = fetch_article(topic)
        
        # UX: Use Rich Panel to make the output look like a proper documentation page
        # We assume the content might be plain text, but rendering as Markdown is safer/cleaner
        console.print(Panel(
            Markdown(content),
            title=f"Grokpedia: {topic.title()}",
            expand=False,
            border_style="green"
        ))

    except ContentRetrievalError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Unexpected System Error:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()