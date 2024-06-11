import click

from utils.base_config import BaseConfig


@click.command()
def read_question():
    question = click.prompt(
        "Enter your question:",
        default="What is the name of Peter's brother? And how old is he?",
    )
    click.echo(f"Your question: {question}\n")
    return question


@click.command()
def read_context():
    # context could be what the agent has scraped from the web
    # read context from data/context.txt
    with open("structured_responses/data/context.txt", "r") as f:
        context = f.read().strip()
        return context


class Config(BaseConfig):
    def __init__(self):
        super().__init__()
        self.user_question = read_question(standalone_mode=False)
        self.context = read_context(standalone_mode=False)
