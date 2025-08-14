import os
import yaml
import random
import re
import csv
from faker import Faker

fake = Faker()

class SchemaLoader:
    def __init__(self, folder='schemas'):
        self.folder = folder

    def find_schema_files(self):
        if not os.path.exists(self.folder):
            print(f"Schema folder '{self.folder}' does not exist!")
            return []
        return [os.path.join(self.folder, f) for f in os.listdir(self.folder) if f.endswith(('.yaml', '.yml'))]

    @staticmethod
    def load_schema(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

class DataGenerator:
    def __init__(self, schema, schema_filename):
        self.schema = schema
        self.schema_filename = schema_filename
        self.mode = schema.get('mode', 'plain').lower()
        if self.mode != 'plain':
            raise ValueError(f"Schema mode '{self.mode}' not supported by this generator (only 'plain').")
        if 'tables' not in schema:
            raise ValueError(f"Schema {schema_filename} must contain a 'tables' section.")
        self.tables = schema['tables']

    def generate_value(self, col, row_idx, used_uniques):
        col_type = col['type']

        if col.get('auto_increment'):
            return row_idx + 1

        if col_type == 'integer':
            return random.randint(col.get('min', 0), col.get('max', 100))

        if col_type == 'float':
            return round(random.uniform(col.get('min', 0), col.get('max', 1000)), 2)

        if col_type == 'string':
            pattern = col.get('regex')
            if pattern:
                attempts = 0
                value = fake.user_name()
                while (not re.match(pattern, value) or (col.get('unique') and value in used_uniques[col['name']])) and attempts < 100:
                    value = fake.user_name()
                    attempts += 1
                if attempts == 100:
                    raise Exception(f"Could not generate unique string matching regex '{pattern}' for column '{col['name']}' in schema '{self.schema_filename}'")
                if col.get('unique'):
                    used_uniques[col['name']].add(value)
                return value
            else:
                return fake.word()

        if col_type == 'boolean':
            return random.choice([True, False])

        # Add support for enum, date etc. later if needed

        return None

    def generate_rows(self, table_schema):
        columns = table_schema['columns']
        row_count = table_schema.get('rowCount', 50)
        used_uniques = {col['name']: set() for col in columns if col.get('unique')}
        rows = []
        for i in range(row_count):
            row = {}
            for col in columns:
                row[col['name']] = self.generate_value(col, i, used_uniques)
            rows.append(row)
        return rows

    @staticmethod
    def write_csv(table_name, columns, rows, output_folder='.'):
        os.makedirs(output_folder, exist_ok=True)
        filename = os.path.join(output_folder, f"{table_name}.csv")
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[col['name'] for col in columns])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} rows to '{filename}'")

    def generate_all_tables(self, output_folder):
        for table_name, table_schema in self.tables.items():
            rows = self.generate_rows(table_schema)
            self.write_csv(table_name, table_schema['columns'], rows, output_folder)

def main():
    schema_folder = 'schemas'
    output_root = 'output'

    loader = SchemaLoader(schema_folder)
    schema_files = loader.find_schema_files()

    if not schema_files:
        print(f"No YAML schema files found in folder '{schema_folder}'.")
        return

    for schema_path in schema_files:
        try:
            schema = loader.load_schema(schema_path)
            base_name = os.path.splitext(os.path.basename(schema_path))[0]
            output_folder = os.path.join(output_root, base_name)

            print(f"Processing schema '{schema_path}' in plain mode...")

            generator = DataGenerator(schema, base_name)
            generator.generate_all_tables(output_folder)

        except Exception as e:
            print(f"Error processing schema '{schema_path}': {e}")

if __name__ == "__main__":
    main()
