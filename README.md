# data-generation
A flexible data generator that creates realistic datasets from YAML-defined schemas — perfect for testing, prototyping, and seeding databases with custom-shaped data.
# data-generation

**A flexible, schema-driven data generator that creates realistic synthetic datasets from YAML definitions. Perfect for testing, prototyping, and seeding custom-shaped databases — effortlessly and at scale!**

***

## 🚀 Features

- **Multi-schema support**: Automatically processes multiple YAML schema files from a folder.
- **Schema-driven**: Define tables, columns, constraints, and data characteristics all in YAML.
- **Realistic data**: Uses the powerful [Faker](https://faker.readthedocs.io/) library for believable data generation.
- **Plain tables support**: Quickly generate independent tables without needing relationships or foreign keys.
- **Custom constraints**: Supports data types like integer, float, string, boolean — with options for uniqueness, regex filters, auto-increment, and value ranges.
- **Clean output**: Generates CSV files organized by schema, easy to load into any database or tooling.
- **Extensible architecture**: Designed with classes for easy expansion to relational data, advanced constraints, and more.

***

## 📦 Installation

Make sure you have Python 3.10+ installed.

Install the required libraries with:
pyymal
faker
pandas

***

## 📁 Setup Your Schemas

- Create a folder named `schemas` next to the script.
- Inside `schemas`, add one or more YAML files describing your data schemas.
- Each YAML file should define the `mode` as `plain` and include one or more tables.

### Example `schemas/sample_schema.yaml`
[bank-user.yaml](schemas/bank-user.yaml)


***

## ▶️ Usage

Simply run the main script:

python data_generator.py



The tool will:

- Scan the `schemas/` folder for all `.yaml` / `.yml` files.
- Generate CSVs for each table, inside the folder `output/<schema-file-base-name>/`.
- Respect constraints like uniqueness, regex, auto-increment, and value bounds.

Example output structure:
output/
└── sample_schema/
├── users.csv
└── products.csv



***

## 🎯 Why Use This Tool?

- **Speed up development & testing**: Spin up realistic datasets in minutes with zero coding.
- **Customizable & transparent**: Your data definitions live in easy-to-edit YAML files—no black boxes.
- **Extendable**: Built with maintainability and adaptability in mind.
- **Portable formats**: Get clean CSV outputs compatible with virtually every tool and platform.

***

## 🔧 How to Extend

Want to add:

- Relational data with foreign keys?
- More data types (enums, dates, timestamps)?
- Schema versioning and evolution support?
- Additional output formats like JSON or SQL INSERTs?

The code's modular classes make it straightforward — and I’m happy to help!

***

## 📚 Dependencies

- [PyYAML](https://pyyaml.org/)
- [Faker](https://faker.readthedocs.io/en/master/)

***

## 🙏 Contributing

Feel free to fork, suggest features, or report issues! Your contributions make this tool better.

***

Happy data generating! 🎉

***

If you want, I can also help with:

- CLI argument parsing for flexible configuration
- Sample YAML schema collections
- Detailed usage examples or integration tips

Just let me know!


