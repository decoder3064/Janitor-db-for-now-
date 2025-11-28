"""CLI interface for DB Agent"""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.db.sqlite_adapter import SQLiteAdapter

console = Console()

@click.group()
def cli():
    """DB Agent - AI Database Health Agent"""
    pass

@cli.command()
@click.argument('database')
def schema(database):
    """Display database schema"""
    
    if not Path(database).exists():
        console.print(f"[red]✗ Database not found: {database}[/red]")
        return
    
    with console.status("[bold green]Loading schema..."):
        with SQLiteAdapter(database) as db:
            schema_data = db.get_full_schema()
    
    # Display each table
    for table_name, table_info in schema_data.items():
        # Create table for columns
        table_display = Table(title=f"Table: {table_name} ({table_info['row_count']} rows)")
        table_display.add_column("Column", style="cyan")
        table_display.add_column("Type", style="magenta")
        table_display.add_column("Nullable", style="yellow")
        table_display.add_column("Primary Key", style="green")
        
        for col in table_info['columns']:
            table_display.add_row(
                col['name'],
                col['type'],
                "✓" if col['nullable'] else "✗",
                "✓" if col['primary_key'] else ""
            )
        
        console.print(table_display)
        
        # Display foreign keys if any
        if table_info['foreign_keys']:
            fk_text = "\n".join([
                f"  • {fk['column']} → {fk['references_table']}.{fk['references_column']}"
                for fk in table_info['foreign_keys']
            ])
            console.print(Panel(fk_text, title="Foreign Keys", border_style="blue"))
        
        console.print()  # Empty line between tables

@cli.command()
@click.argument('database')
def info(database):
    """Display database summary"""
    
    if not Path(database).exists():
        console.print(f"[red]✗ Database not found: {database}[/red]")
        return
    
    with SQLiteAdapter(database) as db:
        schema_data = db.get_full_schema()
    
    # Summary table
    summary = Table(title=f"Database: {database}")
    summary.add_column("Table", style="cyan")
    summary.add_column("Rows", style="magenta", justify="right")
    summary.add_column("Columns", style="yellow", justify="right")
    
    total_rows = 0
    for table_name, table_info in schema_data.items():
        summary.add_row(
            table_name,
            str(table_info['row_count']),
            str(len(table_info['columns']))
        )
        total_rows += table_info['row_count']
    
    console.print(summary)
    console.print(f"\n[bold]Total Records:[/bold] {total_rows:,}")
    console.print(f"[bold]Total Tables:[/bold] {len(schema_data)}")

if __name__ == '__main__':
    cli()