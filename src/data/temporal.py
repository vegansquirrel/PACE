# src/data/temporal.py
class TemporalProcessor:
    def process_dates(self, term_sheet):
        timeline = {}
        for event in term_sheet['temporal_events']:
            timeline[event['type']] = {
                'dates': self._parse_dates(event['description']),
                'reference': event.get('reference', 'trade_date')
            }
        return timeline

    def _parse_dates(self, date_description):
        return llm.invoke(f"""Convert these date descriptions to ISO format:
        {date_description}
        Return JSON array""")