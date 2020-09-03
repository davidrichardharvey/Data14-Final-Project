import pyodbc
from s3_project.Config.config_manager import find_variable
from s3_project.functions import create_table_schema
import ast
from s3_project.Config.config_manager import find_hidden_variable


class ProjectDatabase:
    def __init__(self, to_create: bool = False):
        self.__server = find_hidden_variable('server')
        self.__database = find_hidden_variable('database')
        self.__username = find_hidden_variable('username')
        self.__password = find_hidden_variable('password')
        self.__connection_string = "DRIVER={SQL Server};"
        self.__connection_string += f"SERVER={self.__server};"
        self.__connection_string += f"DATABASE={self.__database};"
        self.__connection_string += f"UID={self.__username};"
        self.__connection_string += f"PWD={self.__password}"
        self.__sparta = pyodbc.connect(self.__connection_string)
        self.__cursor = self.__sparta.cursor()
        self._tables = []
        self._existing_tables = []
        self._schemas = []
        self._pk_issues = []
        self._fk_issues = []
        if to_create:
            self.run_methods()

    def _sql_query(self, sql_query):
        return self.__cursor.execute(sql_query)

    def _get_schemas(self):
        # Looks up the schema for each of the tables in the config file
        print('Getting Schemas')
        tables = find_variable('all_tables', 'TABLE SCHEMAS').split(', ')
        for table in tables:
            self._tables.append({'Name': table, 'Schema': ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))})

    def _create_table_no_keys(self):
        # Creates a table without any primary or foreign keys from the table dictionaries
        print(f"Creating Tables")
        for table in self._tables:
            all_lines = []
            schema = table['Schema']
            columns = schema.keys()

            # Adds each line needed in the SQL query to a list
            for column in columns:
                line = f"{column} {schema[column]['variable type']} {schema[column]['if null']}"
                if 'PK' in schema[column].keys():
                    line = f"{line} {schema[column]['PK']}"
                all_lines.append(line)

            # Writes the query. If there is an issue making the table (e.g. it already exists in the database, it is
            # added to a list and printed using a try-except clause. Adds the schema to a JSON file
            query = f"""
                    USE SpartaGlobal
                    CREATE TABLE {table['Name']}
                    (
                    """
            query += ',\n'.join(all_lines)
            query += ');'
            self._sql_query(query)
            try:
                self.__sparta.commit()
            except pyodbc.Error:
                self._existing_tables.append(table['Name'])
        self._create_json()
        if len(self._existing_tables) > 0:
            print(f"\nThese tables could not be added: {', '.join(self._existing_tables)}"
                  f"\nThey may already exist in the database; please drop them before trying again\n")
        else:
            print("Successfully created tables")

    def _create_json(self):
        # Creates a JSON file specifying the schema for the tables
        for table in self._tables:
            self._schemas.append(table['Schema'])
            if table['Name'] not in self._existing_tables:
                create_table_schema(table, 'database_schema.json')

    def _add_primary_keys(self, table):
        # Adds primary keys to tables in the database. If it can't, it adds the tables with issues to a list
        primary_keys = []
        for column in table['Schema']:
            column_details = table['Schema'][column]
            if 'PK' in column_details.keys():
                primary_keys.append(column)
        try:
            self._sql_query(f"""
                            ALTER TABLE {table['Name']} ADD PRIMARY KEY ({','.join(primary_keys)});
                            """)
            self.__sparta.commit()
        except pyodbc.ProgrammingError:
            self._pk_issues.append(table['Name'])

    def _add_foreign_keys(self, table):
        # Alters the tables to assign foreign keys
        for column in table['Schema']:
            column_details = table['Schema'][column]
            if 'FK' in column_details.keys():
                try:
                    self._sql_query(f"""
                                    ALTER TABLE {table['Name']}
                                    ADD FOREIGN KEY ({column}) REFERENCES {column_details['FK'][0]}\
                                    ({column_details['FK'][1]})
                                    """)
                    self.__sparta.commit()
                except pyodbc.ProgrammingError:
                    self._fk_issues.append(table['Name'])

    def _add_keys(self):
        # Applies the methods to add tables to database. Prints a statement if any errors arise
        print('Assigning Keys')
        for table in self._tables:
            self._add_primary_keys(table)
            self._add_foreign_keys(table)

        # Prints a message stating any tables with an issue assigning primary keys
        if len(self._pk_issues) > 0:
            print(f"\nPrimary keys could not be added to these tables: {', '.join(self._pk_issues)}\n"
                  f"They may already have been assigned.\n")
        else:
            print("Successfully added primary keys to tables")

        # Prints a message for the issues involving assigning foreign keys
        if len(self._pk_issues) > 1:
            print(f"\nForeign keys could not be added to these tables: {', '.join(self._fk_issues)}\n"
                  f"They may already have been assigned.\n")
        else:
            print("Successfully added foreign keys to tables")

    def run_methods(self):
        self._get_schemas()
        self._create_table_no_keys()
        self._add_keys()
