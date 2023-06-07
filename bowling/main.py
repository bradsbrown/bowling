"""Bowling Calculator API."""

import fastapi
import uvicorn

import bowling.calculator

app = fastapi.FastAPI(
    title="Bowling Calculator",
    version="1.0",
)


RollList = list[int | str]
FrameList = list[int | None]


@app.post("/", response_model=FrameList)
def get_frames(roll_list: RollList):
    return bowling.calculator.get_scores(roll_list)


def dev_run():
    uvicorn.run("bowling.main:app", host="0.0.0.0", port=8123)


if __name__ == "__main__":
    dev_run()
