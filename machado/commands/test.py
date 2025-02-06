import importlib
from urllib.parse import urlparse

from machado.parser import ConfigParser
from machado.utils.env_var import load_env, get_env_var


def create_dsn(params):
    if isinstance(params, str):
        return params

    cleaned_params = {
        k: v for k, v in params.items()
        if v is not None and k != 'driver'
    }

    return " ".join([
        f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}"
        for key, value in cleaned_params.items()
    ])


def connection_test():
    main_config = ConfigParser()
    project_configs = main_config.project_config()
    db_configs = main_config.database_config()

    env_path = project_configs.get("env_path")
    if env_path:
        load_env(env_path)

    DRIVER_MAPPING = {
        'postgresql': ['psycopg2'],
    }

    db_url = db_configs.get("url")

    if db_url:
        parsed = urlparse(db_url)

        if '+' in parsed.scheme:
            db_type, driver = parsed.scheme.split('+')
        else:
            db_type = parsed.scheme
            driver = DRIVER_MAPPING.get(db_type, [''])[0]
    else:
        driver = db_configs.get("driver")

    if not driver:
        raise ValueError("Driver must be specified in machado.conf.")

    try:
        lib_driver = importlib.import_module(driver)
    except ImportError:
        raise ImportError(f"Driver {driver} not installed.")

    raw_params = db_url if db_url else {
        "driver": driver,
        "host": get_env_var("DB_HOST") or db_configs.get("host"),
        "port": get_env_var("DB_PORT") or db_configs.get("port"),
        "dbname": get_env_var("DB_NAME") or db_configs.get("name"),
        "user": get_env_var("DB_USER") or db_configs.get("user"),
        "password": get_env_var("DB_PASSWORD") or db_configs.get("password")
    }

    connection_params = create_dsn(raw_params)

    lib_driver.connect(connection_params)

    # TODO: DCL commands.
    print("Connection established with database.")
