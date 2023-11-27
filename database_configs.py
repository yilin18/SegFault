from constants import *


# TODO: MySQL transaction database connection details
mysql_transaction_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'yyl511'
}

# TODO: Neo4j transaction database connection details
neo4j_transaction_config = {
    'uri': 'bolt://localhost:7687',
    'user': 'neo4j',
    'password': '111111111'
}

# TODO: MySQL social media database connection details
mysql_social_media_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'sm'
}

# TODO: Neo4j social media database connection details
neo4j_social_media_config = {
    'uri': 'bolt://localhost:7687',
    'user': 'neo4j',
    'password': '111111111'
}


# Container of all the configs
dataset_to_mysql_config = {
    TRANSACTION: mysql_transaction_config,
    SOCIAL_MEDIA: mysql_social_media_config
}

dataset_to_neo4j_config = {
    TRANSACTION: neo4j_transaction_config,
    SOCIAL_MEDIA: neo4j_social_media_config
}
