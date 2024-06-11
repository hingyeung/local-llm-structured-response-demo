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

@click.command()
def read_question():
    question = click.prompt("Enter your question:", default="What is the name of Peter's brother? And how old is he?")
    click.echo(f"Your question: {question}\n")
    return question

@click.command()
def read_context():
    # context could be what the agent has scraped from the web
    # read context from data/context.txt
    with open("data/context.txt", "r") as f:
        context = f.read().strip()
        return context


class Config:
    def __init__(self):
        self.model_name = choose_model(standalone_mode=False)
        self.user_question = read_question(standalone_mode=False)
        self.context = read_context(standalone_mode=False)
    
    