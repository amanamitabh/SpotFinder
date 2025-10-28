import mysql.connector as mysql

server = "mysql-13627029-xmxn380-7f2a.i.aivencloud.com"
db = "defaultdb"
usr = "avnadmin"
pwd = "AVNS_sz-DYke8GCPEgYgbPeq"
con_obj = mysql.connect(host= server, database = db , username=usr, password=pwd, port=19214)
mycur = con_obj.cursor()
mycur.execute("CREATE TABLE parking(vacant int, occupied int, lat varchar(10), lon varchar(10), PRIMARY KEY());")
mycur.execute("INSERT INTO parking VALUES(4, 4, '110.229N', '251.001E');")
mycur.close()
con_obj.close()