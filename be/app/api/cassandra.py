from os import getenv

from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.query import dict_factory


class Cassandra:
    def __init__(
        self,
        host: str = getenv("CASSANDRA_MASTER_SERVICE_HOST", "0.0.0.0"),
        port: str = getenv("CASSANDRA_MASTER_SERVICE_PORT", "9042"),
        ttl: int = 31536000,  # 1 year
        replication: int = 1,
        table: str = "default_table",
        keyspace: str = "default_ks",
    ):
        self.cluster = Cluster(contact_points=[host], port=int(port), execution_profiles={EXEC_PROFILE_DEFAULT: self.create_exec_profile()})
        self.db = self.cluster.connect()

        self.create_keyspace(keyspace, replication)
        self.db.set_keyspace(keyspace)

        self.create_table(table, ttl)

        self.keyspace = keyspace
        self.table = table

    def create_exec_profile(self):
        return ExecutionProfile(
            # load_balancing_policy=WhiteListRoundRobinPolicy(['127.0.0.1']),
            # retry_policy=DowngradingConsistencyRetryPolicy(),
            # consistency_level=ConsistencyLevel.LOCAL_QUORUM,
            # serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
            request_timeout=15,
            row_factory=dict_factory,
        )

    def create_keyspace(self, keyspace: str, rep: int):
        res = self.db.execute(
            f"CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH replication = {{'class':'SimpleStrategy', 'replication_factor' : %(rep)s}}", {"rep": rep}
        )
        self.db.set_keyspace(keyspace)
        return res

    def create_table(self, table: str, ttl: int):
        return self.db.execute(
            f"CREATE TABLE IF NOT EXISTS {table} (short_url text primary key, long_url varchar, time timestamp) WITH default_time_to_live = %(ttl)s",
            {"ttl": ttl},
        )

    def get_all(self):
        return self.db.execute(f"SELECT * FROM {self.table}").all()

    def get(self, short_url: str):
        return self.db.execute(f"SELECT * FROM {self.table} WHERE short_url = %(short_url)s", {"short_url": short_url}).one()

    def set(self, short_url: str, long_url: str):
        return self.db.execute(
            f"INSERT INTO {self.table} (short_url, long_url, time) VALUES (%(short_url)s, %(long_url)s, toTimeStamp(now())) IF NOT EXISTS",
            {"short_url": short_url, "long_url": long_url},
        )
