import MySQLdb
import os


class QueryWrapper:
    def __init__(self):
        username = os.getenv("DANARBU_DBUSER")
        password = os.getenv("DANARBU_DBPASSWORD")
        schema = os.getenv("DANARBU_DBSCHEMA")
        hostname = os.getenv("DANARBU_DBHOST")
        self.db_connection = MySQLdb.connect(
            user=username, passwd=password, db=schema, host=hostname
        )

    def cursor(self):
        return self.db_connection.cursor()


def simple_search(search_string):
    wrapper = QueryWrapper()
    cursor = wrapper.cursor()
    cursor.execute(
        """
        SELECT nafn, stada, kyn, aldur, faeding, andlat, sysla_heiti, sokn_heiti, baer_heiti,
            MATCH (nafn,stada,athugasemdir, baer_heiti, sysla_heiti, sokn_heiti, faeding, andlat)
            AGAINST (%s IN BOOLEAN MODE) as score
        FROM tbl_danarbu
        WHERE
            MATCH (nafn,stada,athugasemdir, baer_heiti, sysla_heiti, sokn_heiti, faeding, andlat)
            AGAINST (%s IN BOOLEAN MODE)
        ORDER BY score DESC;
    """,
        (search_string, search_string,),
    )
    return cursor.fetchall()
