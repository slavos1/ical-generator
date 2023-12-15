from argparse import ArgumentParser
from datetime import datetime
from functools import partial
from io import StringIO
from pathlib import Path

import pandas as pd
import pytz
from dateutil.parser import parse as dtparse
from ical.calendar import Calendar
from ical.calendar_stream import IcsCalendarStream
from ical.event import Event
from loguru import logger
from ruamel.yaml import YAML


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-o", "--output-file", type=Path, help="Output iCal")
    parser.add_argument("INPUT", type=Path, help="Input CSV")
    return parser.parse_args()


def parse_date(s, tz: pytz.timezone = pytz.utc, time: str = "") -> datetime:
    return tz.localize(dtparse(f"{s} {time}"))


def cli():
    args = parse_args()
    logger.info("Loading {}", args.INPUT)
    data = YAML(typ="safe").load(args.INPUT.open())
    tz = pytz.timezone(data.get("timezone", "UTC"))
    _pd = partial(parse_date, tz=tz)
    t = pd.read_csv(
        StringIO(data.get("csv", "")),
        converters={
            "From": _pd,
            "To": partial(_pd, time="23:59:59"),
            "Label": str.strip,
        },
        skip_blank_lines=True,
    ).reset_index()
    logger.debug("t:\n{}", t)
    calendar = Calendar(
        events=[Event(summary=r.Label, start=r.From, end=r.To) for _, r in t.iterrows()],
    )
    logger.info("Writing {} events to {}", len(calendar.events), args.output_file)
    with args.output_file.open("w") as ics_file:
        ics_file.write(IcsCalendarStream.calendar_to_ics(calendar))
