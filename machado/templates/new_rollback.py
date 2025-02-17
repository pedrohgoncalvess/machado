"""
Rollback's: $id_migration
"""
"$example sep$"
from machado.sql.instructions.drop import drop
from machado.sql.base import table, column
from machado.sql.types import numeric, varchar, integer

# usage example
example = table(  # can import the table from other migrations
    "example",
    column("id", integer(auto_increment=True), primary_key=True),
    column("name", varchar(length=80), unique=True),
    column("order_vl", numeric(10,2), not_null=True),
)

del_stmt = drop(example)
