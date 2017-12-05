# -*- coding: utf-8 -*-
import psycopg2

def open_connection():
	conn = psycopg2.connect(database="viberate_crawl", user = "postgres", password = "postgrespass", host = "127.0.0.1", port = "5432")
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

def check_if_hash_exists(conn,hash):
        feed_exists = False
        query = "SELECT transaction_hash FROM data where transaction_hash='%s'" % hash
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if rows and len(rows)>0:
                feed_exists = True
        return feed_exists

def retrieve_contract_watchlist(conn):
        try:
                info = {}
                query = "SELECT id, contract_address FROM ico"
                cur = conn.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                if rows and len(rows) > 0:
                        for ico in rows:
                                info[ico[1].upper()] = ico[0]
                return info

        except StandardError as Ex:
                print "Retrieve Contract Watchlist Error: " + str(Ex)

def insert_unknown_tx(conn, hash, method, ico_id):
	try:
		if not check_if_unknown_exists(conn, hash):
			query = "INSERT INTO unknown_transactions(transaction_hash, method, ico_id) VALUES ('%s','%s', '%s')" % (hash, method, ico_id)
			cur = conn.cursor()
			query = cur.mogrify(query)
			cur.execute(query)
			conn.commit()
	except StandardError as Ex:
		print "SQL Error Unknown_Tx: " + str(Ex)

def check_if_unknown_exists(conn,hash):
	feed_exists = False
	query = "SELECT transaction_hash FROM unknown_transactions where transaction_hash='%s'" % hash
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	if rows and len(rows)>0:
		feed_exists = True
	return feed_exists
