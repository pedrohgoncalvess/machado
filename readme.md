Assistant's Response: Here's a README for your SQL migration tool "Machado":

```markdown
# Machado 🪓

A elegant and lightweight SQL migration tool designed for simplicity and efficiency.

## About

Machado is a Python-based SQL migration tool that emphasizes simplicity and ease of use. Built to manage database migrations across multiple projects without the overhead of complex configurations.

## Key Features

- **Simple Configuration**: Get started with minimal setup
- **Multi-Project Support**: Manage migrations for multiple projects effortlessly
- **Test-Friendly**: First-class support for testing migrations
- **Version Control**: Track and manage your database changes with confidence
- **Rollback Support**: Easily revert migrations when needed
- **Database Agnostic**: Works with various SQL databases

## Why Machado?

While there are many migration tools available, Machado stands out by:

- Providing a streamlined, no-frills approach to database migrations
- Making migration testing a core feature, not an afterthought
- Offering an intuitive CLI that feels natural to use
- Minimizing configuration overhead
- Supporting isolated test environments out of the box

## Quick Start

```bash
# Install Machado
pip install machado-sql

# Initialize a new migration project
machado init

# Create a new migration
machado create add_users_table

# Run migrations
machado migrate

# Run migration tests
machado test
```

## Migration Testing

Machado makes testing migrations straightforward:

```python
# test_migrations.py
from machado.testing import MigrationTest

def test_add_users_table():
    with MigrationTest() as mt:
        mt.run_migration('add_users_table')
        assert mt.table_exists('users')
```

## Configuration

Simple YAML configuration:

```yaml
# machado.yaml
database:
  type: postgresql
  name: my_app
migrations:
  path: ./migrations
  test_path: ./test_migrations
```

## Features Coming Soon

- [ ] Multiple database support
- [ ] Migration dependencies
- [ ] Automated rollback testing
- [ ] Migration dry-run mode
- [ ] Schema comparison tools
- [ ] Migration statistics and insights

## Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.


Made with 🪓 by [Pedro H.]
