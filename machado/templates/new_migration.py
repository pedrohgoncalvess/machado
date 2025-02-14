"""
ID: $id
Created at: $datetime
Description: $description
After: $after
User: $user
"""
"$example sep$"
from machado.base import table, column
from machado.types import numeric, varchar, integer

# usage example
example = table(
    "example",
    column("id", integer(auto_increment=True), primary_key=True),
    column("name", varchar(length=80), unique=True),
    column("order_vl", numeric(10,2), not_null=True),
)
