import importlib
from urllib.parse import urlparse

from machado.config.parser import ConfigParser
from machado.utils.env_var import load_env, get_env_var


class Connection:
    def __init__(self):
        main_config = ConfigParser()
        self.project_configs = main_config.project_config()

        env_path = self.project_configs.get("env_path")
        if env_path:
            load_env(env_path)

        self.DRIVER_MAPPING = {
            'postgresql': ['psycopg2'],
        }

        self.db_configs = main_config.database_config()
        self.db_url = self.db_configs.get("url")
        self.db_type, self.driver = self._db_type_()

        self._connection_ = None


    def connection(self):
        try:
            lib_driver = importlib.import_module(self.driver)
        except ImportError:
            raise ImportError(f"[Machado]: Driver {self.driver} not installed.")

        raw_params = self.db_url if self.db_url else {
            "driver": self.driver,
            "host": get_env_var("DB_HOST") or self.db_configs.get("host"),
            "port": get_env_var("DB_PORT") or self.db_configs.get("port"),
            "dbname": get_env_var("DB_NAME") or self.db_configs.get("name"),
            "user": get_env_var("DB_USER") or self.db_configs.get("user"),
            "password": get_env_var("DB_PASSWORD") or self.db_configs.get("password")
        }

        connection_params = self._create_dsn_(raw_params)

        return lib_driver.connect(connection_params)


    def __enter__(self):
        self._connection_ = self.connection()
        return self._connection_


    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._connection_.close()


    def _create_dsn_(self, params: dict | str):
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


    def _db_type_(self) -> tuple[str, str]:
        DB_TYPE_MAPPING = {"psycopg2": "postgresql"}

        if self.db_url:
            parsed = urlparse(self.db_url)

            if '+' in parsed.scheme:
                db_type = parsed.scheme.split('+')[0]
            else:
                db_type = parsed.scheme

            return db_type, self.DRIVER_MAPPING.get(db_type)

        else:
            driver = self.db_configs.get("driver")

            if not driver:
                raise ValueError("[Machado]: Driver must be specified in machado.conf.")

            return DB_TYPE_MAPPING.get(driver), driver


    def _parse_params_(self):
        driver = self.db_type
        db_url = self.db_configs.get("url")

        raw_params = db_url if db_url else {
            "driver": driver,
            "host": get_env_var("DB_HOST") or self.db_configs.get("host"),
            "port": get_env_var("DB_PORT") or self.db_configs.get("port"),
            "dbname": get_env_var("DB_NAME") or self.db_configs.get("name"),
            "user": get_env_var("DB_USER") or self.db_configs.get("user"),
            "password": get_env_var("DB_PASSWORD") or self.db_configs.get("password")
        }

        return raw_params
