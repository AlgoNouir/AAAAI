from aaaai.agent import Agent
from datetime import datetime


class WhiteAgent(Agent):
    @property
    def _ignoreFuncs(self):
        return ["whatHappen", *super()._ignoreFuncs]

    def whatHappen(self, event, detail):
        events = self.system_prompt.get("EVENTS", {})

        eventSelected = self.select(
            (
                f"is event {event} exists on category options? if not response None."
                f" | event detail: {detail}"
            ),
            list(events.keys()),
        )

        # check event
        if eventSelected is None:
            eventSelected = event
        # events data
        eventBatch = events.get(eventSelected, "")
        eventBatch += f"time: {datetime.now()}, event: {event}, detail:{detail}\n"
        events[eventSelected] = eventBatch

        # remember events
        self.system_prompt["EVENTS"] = events
