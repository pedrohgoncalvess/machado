from machado.config.parser import ConfigParser


def generate_conf_example():
    config = ConfigParser().config
    output_file = "machado.example.conf"

    descriptions = {
        "name": "The name of the project",
        "migration_path": "The path where migration files are stored",

        "url": "The full database connection URL (e.g., 'postgresql://user:password@host:port/dbname')",
        "env_file": "Path to the environment file containing database credentials",
        "driver": "The database driver used to connect to PostgreSQL",
        "db_host": "The hostname or IP address of the database server",
        "db_port": "The port on which the database is running",
        "db_name": "The name of the database",
        "db_user": "The username used for database authentication",
        "db_password": "The password for database authentication (avoid storing passwords in plain text)",
        "table_name": "The default table name used in the application",
        "timeout": "Timeout in seconds for database connections",
        "retry_attempts": "Number of retry attempts in case of connection failure",

        "py_example": "Indicates whether to use Python-based migration scripts (true/false)",
        "user": "The user responsible for executing migrations"
    }

    with open(output_file, "w") as example_file:
        for section in config.sections():
            example_file.write(f"[{section}]\n")
            for key in config[section]:
                if key in descriptions and descriptions[key] is None:
                    value = config[section][key]
                    example_file.write(f"{key} = {value}\n")
                else:
                    desc = descriptions.get(key, None)
                    example_file.write(f"{key} = # {desc}\n" if desc else f"{key} = \n")
            example_file.write("\n")

    print(f"[Machado] machado.example.conf generated with success!")
