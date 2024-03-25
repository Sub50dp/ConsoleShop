import os


def get_database_configuration(env):
    """
    This function returns the configuration for the database
    """

    # Localhost postgres
    database_local = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("POSTGRES_DB", default=""),
            "USER": env.str("POSTGRES_USER", default=""),
            "PASSWORD": env.str("POSTGRES_PASSWORD", default=""),
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

    # Docker postgres
    database_docker = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("POSTGRES_DB", default=""),
            "USER": env.str("POSTGRES_USER", default=""),
            "PASSWORD": env.str("POSTGRES_PASSWORD", default=""),
            "HOST": "postgres_container_console",
            "PORT": "5432",
        }
    }

    if os.getenv("ENVIRONMENT") == "docker":
        return database_docker
    else:
        return database_local
