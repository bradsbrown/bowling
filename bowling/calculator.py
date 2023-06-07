"""Bowling Calculator Core Logic."""
import dataclasses
import typing

Strike = typing.Literal["X"]
Spare = typing.Literal["/"]

STRIKE_VAL: Strike = "X"
SPARE_VAL: Spare = "/"

FirstRollType = int | Strike
SecondRollType = int | Spare


@dataclasses.dataclass
class Frame:
    first_roll: FirstRollType
    second_roll: SecondRollType | None = None

    @property
    def is_complete(self):
        return self.first_roll == STRIKE_VAL or (self.first_roll and self.second_roll)

    @property
    def numerical_sum(self):
        if isinstance(self.first_roll, int) and isinstance(self.second_roll, int):
            return self.first_roll + self.second_roll

    @property
    def first_roll_val(self):
        if self.first_roll is None:
            return self.first_roll
        return 10 if self.first_roll == STRIKE_VAL else self.first_roll

    @property
    def second_roll_val(self):
        if self.second_roll is None:
            return self.second_roll
        if isinstance(self.second_roll, int):
            return self.second_roll
        return 10 - self.first_roll_val

    @property
    def is_strike(self):
        return self.first_roll == STRIKE_VAL

    @property
    def is_spare(self):
        if not self.is_complete:
            return None
        if self.is_strike:
            return False
        return self.second_roll == SPARE_VAL or self.numerical_sum == 10

    @property
    def raw_score(self):
        if not self.is_complete:
            return None
        if self.is_strike or self.is_spare:
            return 10
        return self.numerical_sum

    @property
    def rolls(self):
        return tuple(
            x for x in (self.first_roll_val, self.second_roll_val) if x is not None
        )

    @staticmethod
    def _get_bonus(rolls, count):
        if len(rolls) < count:
            return None
        return sum(rolls[:count])

    def score(self, next_rolls):
        score = self.raw_score
        if not score or (not self.is_spare and not self.is_strike):
            return score
        if self.is_spare:
            bonus = self._get_bonus(next_rolls, 1)
            if not bonus:
                return None
            return score + bonus
        if self.is_strike:
            bonus = self._get_bonus(next_rolls, 2)
            if not bonus:
                return None
            return score + bonus


@dataclasses.dataclass
class Game:
    frame_list: list[Frame] = dataclasses.field(default_factory=list)

    @staticmethod
    def normalize_value(raw_val: str | int):
        if not isinstance(raw_val, str):
            return raw_val
        if raw_val.isdigit():
            return int(raw_val)
        for comp_val in (STRIKE_VAL, SPARE_VAL):
            if raw_val == comp_val:
                return comp_val
        return None

    @classmethod
    def from_rolls(cls, roll_list: list[str | int]):
        parsed_rolls = [cls.normalize_value(x) for x in roll_list]

        frame_list = []
        idx = 0
        while True:
            if idx >= len(parsed_rolls):
                break
            val = parsed_rolls[idx]
            try:
                next_val = parsed_rolls[idx + 1]
            except IndexError:
                next_val = None

            if val == STRIKE_VAL:
                frame_list.append(Frame(first_roll=STRIKE_VAL))
                idx += 1
                continue

            assert isinstance(val, int)
            assert next_val in (SPARE_VAL, None) or isinstance(val, int)
            frame_list.append(Frame(first_roll=val, second_roll=next_val))
            idx += 2

        return cls(frame_list=frame_list)

    @property
    def frames(self):
        score_list = []
        for idx, frame in enumerate(self.frame_list):
            next_rolls = [
                roll
                for next_frame in self.frame_list[idx + 1 :]
                for roll in next_frame.rolls
            ]
            frame_score = frame.score(next_rolls)
            score_list.append(frame_score)
        return score_list[:10]


def get_scores(roll_list: list[str | int]) -> list[int | None]:
    return Game.from_rolls(roll_list).frames
