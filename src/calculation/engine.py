# src/calculation/engine.py
class CalculationEngine:
    def execute(self, extracted_data, market_data):
        # Dynamically generate calculation code
        calculation_logic = self._generate_logic(
            extracted_data['product_type'],
            extracted_data['payment_components']
        )
        
        # Safe execution environment
        return self._sandboxed_execute(calculation_logic, market_data)

    def _generate_logic(self, product_type, components):
        return llm.invoke(f"""Create Python calculation function for:
        Product: {product_type}
        Components: {components}
        Output format: {'{'}payment: float, currency: str, conditions: list{'}'}
        """)