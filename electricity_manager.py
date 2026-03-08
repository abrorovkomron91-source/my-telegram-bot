import pandas as pd
import os

class ElectricityManager:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.load_data()

    def load_data(self):
        # Read the Excel file, assuming the header is on the second row (index 1)
        self.df = pd.read_excel(self.excel_path, header=1)
        # Clean up column names to match the structure
        self.df.columns = ['№', 'МАГАЗИН', 'Имоха', 'Умоха', 'итого_кВт', 'итого_сумма']

    def update_merchant(self, merchant_name, new_reading):
        # Find the merchant by partial name match
        mask = self.df['МАГАЗИН'].str.contains(merchant_name, case=False, na=False)
        if not mask.any():
            return f"Мағозаи '{merchant_name}' ёфт нашуд."

        idx = self.df[mask].index[0]
        
        # Logic: Current 'Имоха' becomes the new 'Умоха'
        old_reading = self.df.at[idx, 'Имоха']
        self.df.at[idx, 'Умоха'] = old_reading
        self.df.at[idx, 'Имоха'] = new_reading
        
        # Calculate difference (kWh)
        diff_kwh = new_reading - old_reading
        self.df.at[idx, 'итого_кВт'] = diff_kwh
        
        # Determine rate: 1.1 for Banks, 1.3 for others
        rate = 1.1 if "БАНК" in str(self.df.at[idx, 'МАГАЗИН']).upper() else 1.3
        total_sum = diff_kwh * rate
        self.df.at[idx, 'итого_сумма'] = round(total_sum, 2)
        
        self.save_data()
        return {
            "merchant": self.df.at[idx, 'МАГАЗИН'],
            "old_reading": old_reading,
            "new_reading": new_reading,
            "diff_kwh": diff_kwh,
            "rate": rate,
            "total_sum": total_sum
        }

    def save_data(self):
        # Save back to Excel, keeping the header structure if possible
        # For simplicity, we save the current dataframe. 
        # In a production bot, we'd use openpyxl to preserve formatting.
        self.df.to_excel(self.excel_path, index=False, startrow=1)

if __name__ == "__main__":
    # Test logic
    manager = ElectricityManager('ПУЛИБАРК.xlsx')
    # Test with PANTERA
    result = manager.update_merchant("ПАНТЕРА", 8000.0)
    print(result)
