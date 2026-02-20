"""anan

Raises:
FileNotFoundError: _description_
ValueError: _description_

Returns:
_type_: _description_
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


def normalize_smiles(smiles: str) -> str:
    """Normalisation for string

    Args:
        smiles (str): _description_

    Returns:
        str: _description_
    """
    return "".join(smiles.strip().split())


@dataclass
class CheckResult:
    """data class

    tbd
    """

    is_correct: bool
    expected: Optional[str]
    user: str
    accepted: List[str]


class AnswerChecker:
    """Loads answers from:

    - CSV: columns: id,answer
      answer can be multiple acceptable SMILES separated by ';'
    - TXT: each line: id=answer (same ';' rule)

    """

    def __init__(self, answers_path: str) -> None:
        """init

        Args:
            answers_path (str): _description_
        """
        self.answers_path = Path(answers_path)
        self.answers: Dict[str, List[str]] = self._load_answers()

    def _load_answers(self) -> Dict[str, List[str]]:
        """answer loader

        Raises:
            FileNotFoundError: _description_

        Returns:
            Dict[str, List[str]]: _description_
        """
        if not self.answers_path.exists():
            raise FileNotFoundError(f"Answers file not found: {self.answers_path}")

        if self.answers_path.suffix.lower() == ".csv":
            return self._load_csv(self.answers_path)
        return self._load_txt(self.answers_path)

    @staticmethod
    def _split_answers(raw: str) -> List[str]:
        """splits answers in csv

        Args:
            raw (str): _description_

        Returns:
            List[str]: _description_
        """
        parts = [p.strip() for p in raw.split(";")]
        return [p for p in parts if p]

    def _load_csv(self, path: Path) -> Dict[str, List[str]]:
        """loads csv

        Args:
            path (Path): _description_

        Raises:
            ValueError: _description_

        Returns:
            Dict[str, List[str]]: _description_
        """
        answers: Dict[str, List[str]] = {}
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if (
                not reader.fieldnames
                or "id" not in reader.fieldnames
                or "answer" not in reader.fieldnames
            ):
                raise ValueError("CSV must have headers: id,answer")

            for row in reader:
                qid = (row.get("id") or "").strip()
                ans = (row.get("answer") or "").strip()
                if qid:
                    answers[qid] = self._split_answers(ans)
        return answers

    def _load_txt(self, path: Path) -> Dict[str, List[str]]:
        """loads

        Args:
            path (Path): _description_

        Returns:
            Dict[str, List[str]]: _description_
        """
        answers: Dict[str, List[str]] = {}
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                qid, ans = line.split("=", 1)
                qid = qid.strip()
                ans = ans.strip()
                if qid:
                    answers[qid] = self._split_answers(ans)
        return answers

    def check(self, question_id: str, user_smiles: str) -> CheckResult:
        """checks answer

        Args:
            question_id (str): _description_
            user_smiles (str): _description_

        Returns:
            CheckResult: _description_
        """
        user_norm = normalize_smiles(user_smiles)
        accepted = self.answers.get(question_id, [])
        accepted_norm = [normalize_smiles(a) for a in accepted]

        is_correct = user_norm != "" and user_norm in accepted_norm
        expected = accepted[0] if accepted else None

        return CheckResult(
            is_correct=is_correct,
            expected=expected,
            user=user_smiles,
            accepted=accepted,
        )
