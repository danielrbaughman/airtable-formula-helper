import typer
from rich import print

app = typer.Typer(rich_markup_mode="markdown")


@app.command()
def main():
    print("Hello, World!")


if __name__ == "__main__":
    app()
