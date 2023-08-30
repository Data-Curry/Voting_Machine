from psycopg2.extras import execute_values
from typing import Tuple, List

Election = Tuple[int, str, str]
Candidate = Tuple[int, str, int]
Vote = Tuple[str, int]


CREATE_ELECTIONS = """CREATE TABLE IF NOT EXISTS elections
(id SERIAL PRIMARY KEY, title TEXT, creator_username TEXT);"""
CREATE_CANDIDATES = """CREATE TABLE IF NOT EXISTS candidates
(id SERIAL PRIMARY KEY, candidate_text TEXT, election_id INTEGER, FOREIGN KEY(election_id) REFERENCES elections (id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, candidate_id INTEGER, FOREIGN KEY(candidate_id) REFERENCES candidates (id));"""


SELECT_ELECTION = "SELECT * FROM elections WHERE id = %s;"
SELECT_ALL_ELECTIONS = "SELECT * FROM elections;"
SELECT_ELECTION_CANDIDATES = """SELECT * FROM candidates WHERE election_id = %s;"""
SELECT_CANDIDATE = "SELECT * FROM candidates WHERE id = %s;"
SELECT_VOTES_FOR_CANDIDATE = "SELECT * FROM votes WHERE candidate_id = %s;"

INSERT_ELECTION_RETURN_ID = "INSERT INTO elections (title, creator_username) VALUES (%s, %s) RETURNING id;"
INSERT_CANDIDATE_RETURN_ID  = "INSERT INTO candidates (candidate_text, election_id) VALUES %s;"
INSERT_VOTE = "INSERT INTO votes (username, candidate_id) VALUES (%s, %s);"


def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ELECTIONS)
            cursor.execute(CREATE_CANDIDATES)
            cursor.execute(CREATE_VOTES)


#  -- elections --


def get_election(connection, election_id: int) -> Election:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ELECTION, (election_id,))
            return cursor.fetchone()


def create_election(connection, title: str, creator:str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_ELECTION_RETURN_ID, (title, creator))

            election_id = cursor.fetchone()[0]
            return election_id


def get_elections(connection) -> List[Election]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_ELECTIONS)
            return cursor.fetchall()


def get_election_candidates(connection, election_id: int) -> List[Candidate]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ELECTION_CANDIDATES, (election_id,))
            return cursor.fetchall()


def add_election_vote(connection, username, candidate_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, candidate_id))


#  -- candidates --


def get_candidate(connection, candidate_id: int) -> Candidate:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CANDIDATE, (candidate_id,))
            return cursor.fetchone()


def add_candidate(connection, candidate_text, election_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CANDIDATE_RETURN_ID, (candidate_text, election_id))
            candidate_id = cursor.fetchone()[0]
            return candidate_id


#  -- votes --


def get_votes_for_candidate(connection, candidate_id: int) -> List[Vote]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_VOTES_FOR_CANDIDATE, (candidate_id,))
            return cursor.fetchall()

