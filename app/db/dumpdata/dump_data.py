from typing import Callable

from fastapi import Depends
import csv
import sys

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.repositories import ScienceRepository, CategoryRepository, FormulaRepository
from app.api.dependencies.database import get_repository


class Dumper:
    def __init__(self, session):
        self.session = session
        self.dump_dir = "app/db/dumpdata/"
        self.encoding = "utf-8"

    def dump_science(self):
        with open(self.dump_dir + 'science.csv', encoding=self.encoding) as file:
            table = list(csv.DictReader(file))
        science_repo = ScienceRepository(self.session)
        for line in table:
            line.pop("id")
            science_repo.create(**line)

    def dump_category(self):
        with open(self.dump_dir + "category.csv", encoding=self.encoding) as file:
            table = list(csv.DictReader(file))
        category_repo = CategoryRepository(self.session)
        for line in table:
            line.pop("id")
            category_repo.create(**line)

    def dump_formula(self):
        with open(self.dump_dir + "formula.csv", encoding=self.encoding) as file:
            table = list(csv.DictReader(file))
        formula_repo = FormulaRepository(self.session)
        for line in table:
            line.pop("id")
            formula_repo.create(**line)

    def dump_all(self):
        for name in self.__dir__():
            attr = getattr(self, name)
            if isinstance(attr, Callable) and "dump" in name:
                attr()


def dump_data(session: Session):
    dumper = Dumper(session=session)
    dumper.dump_all()


