class TermValidator:
    ESSENTIAL_CHECKS = [
        ('product_type', lambda x: x in ['autocallable', 'convertible']),
        ('underlyings', lambda x: len(x) > 0),
        ('dates.maturity', lambda x: TermValidator._valid_iso_date(x)),
        ('terms.nominal_amount', lambda x: x > 0)
    ]

    @staticmethod
    def _valid_iso_date(date_str):
        try:
            datetime.fromisoformat(date_str)
            return True
        except ValueError:
            return False

    def validate(self, extracted_data):
        errors = []
        for path, validator in self.ESSENTIAL_CHECKS:
            value = self._nested_get(extracted_data, path)
            if not validator(value):
                errors.append(f"Validation failed for {path}")
        
        if errors:
            raise ValidationError(f"Critical issues: {errors}")

    def _nested_get(self, data, path):
        keys = path.split('.')
        for key in keys:
            data = data.get(key, {})
        return data