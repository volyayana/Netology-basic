import sqlalchemy


class Database:
    def __init__(self):
        self.engine = sqlalchemy.create_engine('postgresql://netol:1111@localhost:5432/netol_db')
        self.connection = self.engine.connect()

    def get_country(self, name):
        return self.connection.execute(
            f"SELECT max(id)"
            f"  FROM countries c"
            f" WHERE lower(c.name) like lower('%%{name}%%');"
        ).fetchall()[0][0];

    def get_city(self, name, country_id):
        return self.connection.execute(
            f"SELECT max(id)"
            f"  FROM cities c"
            f" WHERE lower(c.name) like lower('%%{name}%%')"
            f"   AND country_id = {country_id};"
        ).fetchall()[0][0];

    def add_city(self, id, name, country_id):
        return self.connection.execute(
            f"INSERT INTO cities(id, name, country_id)"
            f"VALUES ({id}, '{name}', {country_id});"
        )

    def add_found_users(self, user_id, found_user_id):
        return self.connection.execute(
            f"INSERT INTO found_users(user_id, found_user_id) "
            f"VALUES ('{user_id}', {found_user_id});"
        )

    def check_found_users(self, user_id, found_user_id):
        return self.connection.execute(
            f"SELECT COUNT(*)"
            f"  FROM found_users fu"
            f" WHERE fu.user_id = {user_id}"
            f"   AND fu.found_user_id = {found_user_id};"
        ).fetchall()[0][0]

    def add_to_white_list(self, user_id, found_user_id):
        return self.connection.execute(
            f"INSERT INTO white_lists(user_id, white_user_id) "
            f"VALUES ({user_id}, '{found_user_id}');"
        )

    def get_white_list(self, user_id):
        return self.connection.execute(
            f"SELECT white_user_id "
            f"  FROM white_lists wl"
            f" WHERE wl.user_id = {user_id};"
        ).fetchall()

    def add_logs(self, user_id, function_name, exec_date):
        return self.connection.execute(
            f"INSERT INTO logs(user_id, function_name, exec_date) "
            f"VALUES ({user_id}, '{function_name}', TIMESTAMP '{exec_date}');"
        )