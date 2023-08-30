from typing import List
from connections import create_connection
from models import candidate
import database


class Election:
    def __init__(self, title: str, creator: str, _id: int = None):
        self.id = _id
        self.title = title
        self.creator = creator

    def __repr__(self):
        return f"Election({self.title!r}, {self.creator!r}, {self.id!r})"  # Election('title', 'creator', 1)

    def save(self):
        connection = create_connection()
        new_election_id = database.create_election(connection, self.title, self.creator)
        connection.close()
        self.id = new_election_id

    def add_candidate(self, candidate_text: str):
        Candidate(candidate_text, self.id).save()

    @property
    def candidates(self) -> List["Candidate"]:
        connection = create_connection()
        candidates = database.get_election_candidates(connection, self.id)
        connection.close()
        return [(candidate[1], candidate[2], candidate[0]) for candidate in candidates]

    @classmethod
    def get(cls, election_id:int) -> "Election":  # quotes tell Python to evaluate this after it finishes evaluating the class
        connection = create_connection()
        election = database.get_election(connection, election_id)
        connection.close()
        return cls(election[1], election[2], election[0])

    @classmethod
    def all(cls) -> List["Election"]:
        connection = create_connection()
        elections = database.get_elections(connection)
        connection.close()
        return [cls(election[1], election[2], election[0]) for election in elections]




