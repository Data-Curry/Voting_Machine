from psycopg2.extras import execute_values
from typing import Tuple, List

Election = Tuple[int, str, str]
Vote = Tuple[str, int]
ElectionWithCandidate = Tuple[int, str, str, int, str,int]
ElectionResults = Tuple[int, str, int, float]


CREATE_ELECTIONS = """CREATE TABLE IF NOT EXISTS elections
(id SERIAL PRIMARY KEY, title TEXT, creator_username TEXT);"""
CREATE_CANDIDATES = """CREATE TABLE IF NOT EXISTS candidates
(id SERIAL PRIMARY KEY, candidate_text TEXT, election_id INTEGER, FOREIGN KEY(election_id) REFERENCES elections (id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, candidate_id INTEGER, FOREIGN KEY(candidate_id) REFERENCES candidates (id));"""


SELECT_ALL_ELECTIONS = "SELECT * FROM elections;"
SELECT_ELECTION_WITH_CANDIDATES = """SELECT * FROM elections
JOIN candidates ON elections.id = candidates.election_id
WHERE elections.id = %s;"""
SELECT_ELECTION_VOTE_DETAILS = """SELECT 
candidates.id, 
candidates.candidate_text, 
COUNT(votes.candidate_id) AS vote_count, 
COUNT(votes.candidate_id) / SUM(COUNT(votes.candidate_id)) OVER() * 100.0 AS vote_percentage 
FROM candidates 
LEFT JOIN votes ON candidates.id = votes.candidate_id 
WHERE candidates.election_id = %s 
GROUP BY candidates.id;"""

INSERT_ELECTION_RETURN_ID = "INSERT INTO elections (title, creator_username) VALUES (%s, %s) RETURNING id;"
INSERT_CANDIDATE = "INSERT INTO candidates (candidate_text, election_id) VALUES %s;"
INSERT_VOTE = "INSERT INTO votes (username, candidate_id) VALUES (%s, %s);"


def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ELECTIONS)
            cursor.execute(CREATE_CANDIDATES)
            cursor.execute(CREATE_VOTES)


def get_elections(connection) -> List[Election]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_ELECTIONS)
            return cursor.fetchall()


def get_election_details(connection, election_id) -> List[ElectionWithCandidate]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ELECTION_WITH_CANDIDATES, (election_id,))
            return cursor.fetchall()


def get_election_and_vote_results(connection, election_id) -> List[ElectionResults]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ELECTION_VOTE_DETAILS, (election_id,))
            return cursor.fetchall()

def create_election(connection, title, creator, candidates):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_ELECTION_RETURN_ID, (title, creator))

            election_id = cursor.fetchone()[0]
            candidate_values = [(candidate_text, election_id) for candidate_text in candidates]

            execute_values(cursor, INSERT_CANDIDATE, candidate_values)


def add_election_vote(connection, username, candidate_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, candidate_id))