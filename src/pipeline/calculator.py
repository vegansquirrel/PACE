import RestrictedPython

class CalculationEngine:
    def execute(self, terms, market_data):
        code = self._generate_code(terms)
        return self._safe_execute(code, market_data)
    
    def _generate_code(self, terms):
        return self.llm.generate(
            f"""Create Python function to calculate payments for:
            Product Type: {terms['product_type']}
            Components: {terms['payment_components']}
            Market Data: {list(market_data.keys())}"""
        )
    
    def _safe_execute(self, code, inputs):
        restricted_globals = {
            '__builtins__': {
                'float': float,
                'min': min,
                'max': max,
                'sum': sum
            }
        }
        loc = {}
        exec(RestrictedPython.compile_restricted(code), restricted_globals, loc)
        return loc['calculate'](inputs)