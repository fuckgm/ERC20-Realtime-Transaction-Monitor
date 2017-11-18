# -*- coding: utf-8 -*-
import psycopg2

def open_connection():
	conn = psycopg2.connect(database="contract_monitoring", user = "postgres", password = "postgrespass", host = "127.0.0.1", port = "5432")
	#conn = psycopg2.connect(database="erc20monitoring", user = "kevin", password = "aKWCBhsv10hnWk9jVcS4", host = "v179.ncsrv.de", port = "5432")
	#print "database successfully opened"
	return conn

def insert_data(conn, snap):
    try:
        if snap["success"]:
                snap["success"] = 1
        else:
                snap["success"] = 0
        query = "INSERT INTO data (transaction_hash, ico_id, erc20_to, tx_to, tx_from, eth_value, erc20_value, type, status, success, gas_limit, gas_used, block_number, block_timestamp) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )" % (snap["hash"], snap["ico_id"], snap["erc20_to"],snap["tx_to"],snap["tx_from"],snap["eth_value"],snap["erc20_value"],snap["type"],snap["status"],snap["success"],snap["gas_limit"],snap["gas_used"],snap["blockNumber"], snap["blockTimestamp"])
        cur = conn.cursor()
        query = cur.mogrify(query)
        cur.execute(query)
        conn.commit()

    except StandardError as Ex:
        print "SQL ERROR: " + str(Ex)