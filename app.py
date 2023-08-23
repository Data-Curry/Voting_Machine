import os
import psycopg2
from psycopg2.errors import DivisionByZero
from dotenv import load_dotenv
from typing import List
import database


DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "
MENU_PROMPT = """-- Menu --

1) Create new election
2) List open elections
3) Vote in an election
4) Show election votes
5) Exit

Enter your choice: """
NEW_CANDIDATE_PROMPT = "Enter new candidate's name (or leave empty to stop adding candidates): "


def prompt_create_election(connection):
    election_title = input("Enter election title: ")
    election_creator = input("Enter election creator: ")
    candidates = []

    while (new_candidate := input(NEW_CANDIDATE_PROMPT)):
        candidates.append(new_candidate)

    database.create_election(connection, election_title, election_creator, candidates)


def list_open_elections(connection):
    elections = database.get_elections(connection)

    for _id, title, creator in elections:
        print(f"{_id}: {title} (created by {creator})")


def prompt_vote_election(connection):
    election_id = int(input("Enter election would you like to vote on: "))

    election_candidates = database.get_election_details(connection, election_id)
    _print_election_candidates(election_candidates)

    candidate_id = int(input("Enter candidate you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    database.add_election_vote(connection, username, candidate_id)


def _print_election_candidates(election_with_candidates: List[database.ElectionWithCandidate]):
    for candidate in election_with_candidates:
        print(f"{candidate[3]}: {candidate[4]}")


def show_election_votes(connection):
    election_id = int(input("Enter election you would like to see votes for: "))
    try:
        # This gives us count and percentage of votes for each candidate in an election
        election_and_votes = database.get_election_and_vote_results(connection, election_id)
    except DivisionByZero:
        print("No votes have been cast in this election.")
    else:
        for _id, candidate_text, count, percentage in election_and_votes:
            print(f"{candidate_text} got {count} votes ({percentage:.2f}% of total)")


MENU_OPTIONS = {
    "1": prompt_create_election,
    "2": list_open_elections,
    "3": prompt_vote_election,
    "4": show_election_votes
}


def menu():
    database_uri = input(DATABASE_PROMPT)
    if not database_uri:
        load_dotenv()
        database_uri = os.environ["DATABASE_URI"]

    connection = psycopg2.connect(database_uri)
    database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "5":
        try:
            MENU_OPTIONS[selection](connection)
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()