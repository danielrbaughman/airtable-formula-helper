import typer
from rich import print

from airtableformulahelpers import AND, NOT, OR, BoolField, DateField, TextField, ListField

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
            ListField(name="field9").contains("value9"),
            BoolField(name="field10").is_true(),
            DateField(name="field11").is_on()._date("2023-10-01"),
            DateField(name="field12").is_on().days_ago(7),
            DateField(name="field13").is_on("2023-10-01T12:00:00Z"),
            DateField(name="field14").is_before().days_ago(30),
            DateField(name="field14").is_before("today"),
            OR(
                DateField(name="field15").is_on_or_after().days_ago(7),
                DateField(name="field16").is_on_or_after("2023-10-01"),
            ),
        ),
    )
    print(formula)


if __name__ == "__main__":
    app()
