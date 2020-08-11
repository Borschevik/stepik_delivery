"""
   Cli for custom commands for database
"""
import csv
import io
import os

import click
from flask.cli import with_appcontext
from flask_alembic.cli.click import cli as db_cli
from flask_migrate import cli
from sqlalchemy_utils import create_database, drop_database

from config.config import config
from config.extenstions import db
from database.models import Category, Meal


@click.group()
@with_appcontext
def db_tasks():
    """Perform database relates commands"""
    # pylint: disable=W0107
    pass


@db_cli.command()
@click.option(
    "--drop-db", is_flag=True, expose_value=True, prompt="Drop DB tables?",
)
@with_appcontext
@click.pass_context
def init_db(ctx, drop_db: bool):
    """Set the database up from scratch."""
    click.echo("Init.")
    ctx.invoke(create, drop_db=drop_db)
    click.echo("Migrate.")
    ctx.invoke(cli.upgrade)
    click.echo("Done")
    ctx.invoke(seed)
    click.echo("Done")


@db_cli.command()
@click.option("--drop-db/--no-drop-db", expose_value=True, prompt="Drop DB?")
@with_appcontext
def create(drop_db: bool):
    """Create the database."""
    if drop_db:
        click.echo("Dropping database.")
        drop_database(config.SQLALCHEMY_DATABASE_URI)
        click.echo("Done dropping database.")
    create_database(config.SQLALCHEMY_DATABASE_URI)
    click.echo("Database created.")


@click.command("seed")
@with_appcontext
def seed():
    """Seed databse from json files"""
    click.echo("Seeding")

    seeds_dir: str = os.path.join(config.ROOT_DIR, "fixtures")
    categories: list = csv.DictReader(
        io.open(os.path.join(seeds_dir, "delivery_categories.csv"), encoding="utf-8")
    )
    for category in categories:
        Category(**category).add()
        click.echo(f"Added category with id {category.get('id')} to Categories.")

    meals: list = csv.DictReader(
        io.open(os.path.join(seeds_dir, "delivery_items.csv"), encoding="utf-8")
    )
    for meal in meals:
        Meal(**meal).add()
        click.echo(f"Added meal with id {meal.get('id')} to Meal.")
    click.echo("Done seeding.")
    db.session.commit()


db_tasks.add_command(init_db)
db_tasks.add_command(seed)
db_tasks.add_command(create)
