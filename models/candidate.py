from typing import List
from connections import create_connection
import database


class Candidate:
    def __init__(self, candidate_text: str, election_id: int, _id: int = None):
        self.id = _id
        self.text = candidate_text
        self.election_id = election_id

    def __repr__(self):
        return f"Candidate({self.text!r}, {self.election_id!r}, {self.id!r})"

    def save(self):
        connection = create_connection()
        new_candidate_id = database.add_candidate(connection, self.text, self.election_id)
        connection.close()
        self.id = new_candidate_id

    @classmethod
    def get(cls, candidate_id: int) -> "Candidate":
        connection = create_connection()
        candidate = database.get_candidate(connection, candidate_id)
        connection.close
        return cls(candidate[1], candidate[2], candidate[0])

    def vote(self, username: str):
        connection = create_connection()
        database.add_election_vote(connection, username, self.id)
        connection.close()

    @property
    def votes(self) -> list(database.Vote):
        connection = create_connection()
        votes = database.get_votes_for_candidate(conection, self.id)
        connection.close()
        return votes
