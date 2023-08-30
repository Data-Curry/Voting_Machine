from typing import List
import random

import database
from models.election import Election
from models.candidate import Candidate
from connections import create_connection


DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "
MENU_PROMPT = """-- Menu --

1) Create new election
2) List open elections
3) Vote in an election
4) Show election votes
5) Exit

Enter your choice: """
NEW_CANDIDATE_PROMPT = "Enter new candidate's name (or leave empty to stop adding candidates): "


def prompt_create_election():
    election_title = input("Enter election title: ")
    election_creator = input("Enter election creator: ")
    election = Election(election_title, election_creator)
    election.save()

    while (new_candidate := input(NEW_CANDIDATE_PROMPT)):
        election.add_candidate(new_candidate)


def list_open_elections():
    for election in Election.all():
        print(f"{election.id}: {election.title} (created by {election.creator})")


def prompt_vote_election():
    election_id = int(input("Enter election you would like to vote in: "))
    _print_election_candidates(Election.get(election_id).candidates)

    candidate_id = int(input("Enter candidate you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    Candidate.get(candidate_id).vote(username)


def _print_election_candidates(candidates: List[Candidate]):
    for candidate in candidates:
        print(f"{candidate[2]}: {candidate[0]}")


def show_election_votes():
    connection = create_connection()
    election_id = int(input("Enter election you would like to see votes for: "))
    candidates = Election.get(election_id).candidates  # candidate_text, election_id, candidate_id
    title = Election.get(election_id).title
    votes_per_candidate = []
    vote_count = []
    total_votes = 0
    print(f"Election for {title}... ")
    for candidate in candidates:
        c_id = candidate[2]
        candidate_votes = database.get_votes_for_candidate(connection, c_id)
        votes_per_candidate.append(candidate_votes)

    for candidate in votes_per_candidate:
        c_votes = len(candidate)
        vote_count.append(c_votes)
        total_votes += c_votes

    try:
        for candidate, votes in zip(candidates, vote_count):
            percentage = votes / total_votes * 100
            print(f"{candidate[0]} got {votes} votes ({percentage:.2f}% of total)")
    except ZeroDivisionError:
        print("No votes have been cast in this election.")


MENU_OPTIONS = {
    "1": prompt_create_election,
    "2": list_open_elections,
    "3": prompt_vote_election,
    "4": show_election_votes
}


def menu():
    connection = create_connection()
    database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "5":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()