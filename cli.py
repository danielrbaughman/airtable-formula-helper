import typer
from rich import print

from airtableformulahelpers import AND, NOT, BooleanField, DateField, TextField, TextListField

app = typer.Typer(rich_markup_mode="markdown")


@app.command()
def main():
    formula = AND(
        "field1",
        TextField(name="field2").contains("value2"),
        NOT(
            TextField(name="field3").starts_with("value3"),
            TextField(name="field4").not_starts_with("value4"),
            TextField(name="field5").not_equals("value5"),
            TextField(name="field6").is_empty(),
            TextField(name="field7").contains("value7"),
            TextField(name="field8").not_contains("value8"),
            TextListField(name="field9").contains("value9"),
            BooleanField(name="field10").is_true(),
            DateField(name="field11").is_on().value("2023-10-01"),
        ),
    )
    print(formula)


if __name__ == "__main__":
    app()
