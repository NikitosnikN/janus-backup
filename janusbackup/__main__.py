import click

from janusbackup.config import CONFIG_TYPE_CHOICES, MODE_CHOICES, initialize_config
from janusbackup.worker import run_worker

CLICK_MODE_CHOICES = click.Choice(MODE_CHOICES)
CLICK_CONFIG_TYPE_CHOICES = click.Choice(CONFIG_TYPE_CHOICES)


@click.command()
@click.argument(
    "mode",
    type=CLICK_MODE_CHOICES,
)
@click.option(
    "--config-type",
    type=CLICK_CONFIG_TYPE_CHOICES,
    default="env",
    help="Config type",
    show_default=True,
)
@click.option(
    "--config-path",
    type=click.Path(exists=True),
    default=None,
    help="Path to config file",
    show_default=True,
)
def run(
    mode: str,
    config_type: str,
    config_path: str,
):
    config = initialize_config(config_type, config_path)

    if mode == "worker":
        run_worker(config)

    elif mode == "api":
        # uvicorn.run(
        #     get_app(config),
        #     host=config.API_HOST,
        #     port=config.API_PORT,
        # )
        raise NotImplementedError("API section is not implemented yet")

    else:
        raise ValueError("invalid mode")

    return


if __name__ == "__main__":
    run()
