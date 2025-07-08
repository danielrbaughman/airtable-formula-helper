from rich import print
from typer import Typer

from airtableformulahelpers import (
    AND,
    IF,
    TextField,
)

app = Typer(rich_markup_mode="markdown")


@app.command()
def main():
    # IF({Lab Code}="063", "Product " & {Deal Test Pckg} & "\n", "")
    # IF IsVolo && JobFlag == "Map Hard to See"         THEN "Warning: Hard to See - Scout!"

    job_flags = TextField(name="Job Flags")
    lab_code = TextField(name="Lab Code")
    formula = (
        IF(
            AND(
                lab_code.equals("063"),
                job_flags.contains("Map Hard to See", case_sensitive=False, no_trim=True),
            )
        )
        .THEN("Warning: Hard to See - Scout!", string=True)
        .ELSE("")
    )
    print(formula)


if __name__ == "__main__":
    app()
