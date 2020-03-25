try:
    import sys
    import pymysql
    import pymysql.cursors
    from common import SECTION, OPTIONS, print_log_msg, Log, configs
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(1)


class Database:
    """
    Database connection class.
    """
    def __init__(self):
        self.host = configs.get(SECTION.db.name).get(OPTIONS.db_host.name)
        self.username = configs.get(SECTION.db.name).get(OPTIONS.db_user.name)
        self.password = configs.get(SECTION.db.name).get(OPTIONS.db_password.name)
        self.port = configs.get(SECTION.db.name).get(OPTIONS.db_port.name)
        self.dbname = configs.get(SECTION.db.name).get(OPTIONS.db_name.name)
        self.connection = None


    def open_connection(self):
        """
        Connect to MySQL Database.
        """
        try:
            if self.connection is None:
                self.connection = pymysql.connect(host=self.host, user=self.username, password=self.password,
                        db=self.dbname, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        except pymysql.MySQLError as pymysql_err:
            print_log_msg(pymysql_err, Log.ERROR.name)
            sys.exit(0)
        finally:
            print_log_msg('Connection opened successfully.', Log.INFO.value)


    def run_query(self, result):
        """
        Execute SQL query.
        Args:
            result - final dictionary with team names and scores.
        Returns:
            ---
        """
        try:
            self.open_connection()

            with self.connection.cursor() as cursor:
                # Delete old data
                cursor.execute("TRUNCATE TABLE betting")
                for teams, urls_coefficient in result.items():
                    for scores_list in urls_coefficient:
                        for url, coefficient in scores_list.items():
                            # Create a new record
                            teams_info_path = ("INSERT INTO `betting` (`Teams`,`URLs`,`Win Coefficient`,\
                                    `Draw Coefficient`,`Loss Coefficient`) VALUES (%s, %s, %s, %s, %s)")
                            cursor.execute(teams_info_path, (teams, url, coefficient[0], coefficient[1], coefficient[2]))
                # Connection is not autocommit by default.
                # So you must to save your changes.
                self.connection.commit()

        except pymysql.MySQLError as pymysql_err:
            print_log_msg(pymysql_err, Log.ERROR.value)
            print_log_msg("Can't append scores to the db:", Log.ERROR.value)

        finally:
            if self.connection:
                self.connection.close()
                self.connection = None
                print_log_msg('Data has already appended in to DB successfully', Log.INFO.value)
                print_log_msg('Database connection closed.', Log.INFO.value)
