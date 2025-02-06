from dateutil.parser import parse

class TemporalProcessor:
    def process_dates(self, temporal_events):
        timeline = {}
        for event in temporal_events:
            cleaned = self._clean_event_description(event)
            timeline[event['type']] = {
                'dates': [parse(d).isoformat() for d in cleaned['dates']],
                'reference_point': cleaned['reference']
            }
        return timeline
    
    def _clean_event_description(self, event):
        # LLM-assisted cleaning
        return self.llm.generate(
            f"Convert to ISO dates: {event['description']}",
            response_format="json"
        )