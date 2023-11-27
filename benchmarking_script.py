# pip install mysql-connector-python
import mysql.connector
# pip install neo4j
from neo4j import GraphDatabase
import csv
import matplotlib.pyplot as plt
import numpy as np
from constants import *
from database_configs import dataset_to_mysql_config, dataset_to_neo4j_config
from transaction_queries import transcation_queries_by_type_and_db
from social_media_queries import social_medial_queries_by_type_and_db


# Container of all the queries
dataset_to_queries = {
    TRANSACTION: transcation_queries_by_type_and_db,
    SOCIAL_MEDIA: social_medial_queries_by_type_and_db
}


def benchmark():
    # Open a CSV file to store the results
    with open('query_execution_times.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Writing the header
        writer.writerow(['Dataset Name', 'Query Type', 'Database Type', 'Query Name', 'Query', 'Average Execution Time (ms)'])
        # Begin benchmarking all the queries, and store the results in a csv file
        benchmark_all_queries(writer)


def benchmark_all_queries(csv_writer):
    # For each kind of dataset
    for dataset_name in dataset_to_queries:
        queries_by_type_and_db = dataset_to_queries[dataset_name]

        # Dictionaries to store average execution time for each query type
        mysql_times_by_type = {}
        neo4j_times_by_type = {}

        # For each query type (i.e. short, long, aggregated, nested)
        for query_type in queries_by_type_and_db:
            queries_by_db = queries_by_type_and_db[query_type]
            mysql_queries = queries_by_db[MYSQL]
            neo4j_queries = queries_by_db[NEO4J]
            num_queries = len(mysql_queries)

            # Dictionaries to store average execution time for each query
            mysql_times = {}
            neo4j_times = {}

            # For each query
            for i in range(num_queries):
                query_name = f"{query_type} Query {i}"

                mysql_query = mysql_queries[i]
                execution_times = [benchmark_mysql_query(mysql_query, dataset_to_mysql_config[dataset_name]) for _ in range(QUERY_RUN_TIMES)]
                avg_time = sum(execution_times) / len(execution_times)
                mysql_times[query_name] = avg_time
                csv_writer.writerow([dataset_name, query_type, MYSQL, query_name, mysql_query, avg_time])

                neo4j_query = neo4j_queries[i]
                execution_times = [benchmark_neo4j_query(neo4j_query, dataset_to_neo4j_config[dataset_name]) for _ in range(QUERY_RUN_TIMES)]
                avg_time = sum(execution_times) / len(execution_times)
                neo4j_times[query_name] = avg_time
                csv_writer.writerow([dataset_name, query_type, NEO4J, query_name, neo4j_query, avg_time])

            # Store the average execution time for the current query type
            query_type_name = f"{query_type} Query"
            mysql_cur_type_avg_time = sum(mysql_times.values()) / len(mysql_times)
            neo4j_cur_type_avg_time = sum(neo4j_times.values()) / len(mysql_times)
            mysql_times_by_type[query_type_name] = mysql_cur_type_avg_time
            neo4j_times_by_type[query_type_name] = neo4j_cur_type_avg_time

            # Plotting the bar graph for each query type
            plot_bar_graph(mysql_times, neo4j_times, f"{dataset_name} {query_type} Queries Average Execution Times")

        # Plotting the bar graph for each dataset
        plot_bar_graph(mysql_times_by_type, neo4j_times_by_type, f"{dataset_name} Average Execution Times")


def benchmark_mysql_query(query, mysql_config):
    # connection = mysql.connector.connect(**mysql_config)
    # cursor = connection.cursor()
    # start_time = time()
    # cursor.execute(query)
    # end_time = time()
    # cursor.close()
    # connection.close()
    # return end_time - start_time
    # Connect to the MySQL database
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor(buffered=True)

    # Record the start time using MySQL server-side function
    cursor.execute("SELECT NOW(6)")
    start_time = cursor.fetchone()[0]

    # Execute your query
    cursor.execute(query)

    # Record the end time using MySQL server-side function
    cursor.execute("SELECT NOW(6)")
    end_time = cursor.fetchone()[0]

    # Calculate the time difference in milliseconds
    cursor.execute(f"SELECT TIMESTAMPDIFF(MICROSECOND, '{start_time}', '{end_time}')")
    execution_time_microseconds = cursor.fetchone()[0]
    execution_time_milliseconds = execution_time_microseconds / 1000

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return execution_time_milliseconds


def benchmark_neo4j_query(query, neo4j_config):
    # driver = GraphDatabase.driver(neo4j_config['uri'], auth=(neo4j_config['user'], neo4j_config['password']))
    # with driver.session() as session:
    #     start_time = time()
    #     session.run(query)
    #     end_time = time()
    # driver.close()
    # return end_time - start_time
    driver = GraphDatabase.driver(neo4j_config['uri'], auth=(neo4j_config['user'], neo4j_config['password']))
    records, result_summary, keys = driver.execute_query(query, database_='neo4j')
    driver.close()
    # print(result_summary.result_available_after + result_summary.result_consumed_after)
    execution_time_milliseconds = result_summary.result_available_after + result_summary.result_consumed_after
    return execution_time_milliseconds


def plot_bar_graph(mysql_times, neo4j_times, title):
    # Labels for each pair of bars
    queries = list(mysql_times.keys())

    # Heights of the bars
    mysql_avg_times = list(mysql_times.values())
    neo4j_avg_times = list(neo4j_times.values())

    # Setting the positions of the bars
    x = np.arange(len(queries))  # the label locations
    width = 0.35  # the width of the bars

    # Creating the bar graph
    plt.figure(figsize=(12, 6))
    bars1 = plt.bar(x - width/2, mysql_avg_times, width, label=MYSQL)
    bars2 = plt.bar(x + width/2, neo4j_avg_times, width, label=NEO4J)

    # Adding text labels on the bars
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round_to_significant(yval, 3), va='bottom', ha='center')

    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round_to_significant(yval, 3), va='bottom', ha='center')

    # Adding some text for labels, title and custom x-axis tick labels, etc.
    plt.ylabel('Average Execution Time (milliseconds)')
    plt.xlabel('Query')
    plt.title(title)
    plt.xticks(x, queries, rotation=45, ha='right')  # Rotate labels and align right
    plt.legend()

    plt.tight_layout()  # Adjust layout to fit rotated labels
    plt.show()


def round_to_significant(x, n):
    if x == 0:
        return 0
    else:
        return round(x, -int(np.floor(np.log10(abs(x)))) + (n - 1))


if __name__ == "__main__":
    benchmark()
