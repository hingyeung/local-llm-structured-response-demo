import click


@click.command()
def choose_model():
    model = click.prompt(
        "Please choose a LLM to use:",
        type=click.Choice(
            ["llama3:latest", "llama3:8b-instruct-q8_0"], case_sensitive=False
        ),
        default="llama3:latest",
    )
    click.echo(f"You chose: {model}\n")
    return model


class BaseConfig:
    def __init__(self):
        self.model_name = choose_model(standalone_mode=False)
