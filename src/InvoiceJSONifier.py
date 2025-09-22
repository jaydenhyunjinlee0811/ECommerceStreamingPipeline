import csv 

class InvoiceJSONifier:
    @classmethod 
    def run(
        cls, 
        sourceFp: str
    ):
        lst = list()
        with open(
            sourceFp, 
            'r', 
            encoding='utf-8',
            errors='ignore'
        ) as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if row.get("Quantity"):
                    row['Quantity'] = int(row['Quantity'])
                if row.get('UnitPrice'):
                    row['UnitPrice'] = float(row['UnitPrice'])
                if row.get("CustomerID"):
                    row['CustomerID'] = int(row['CustomerID'])

                row['source'] = 'Invoice'
                lst.append(row)

        return lst