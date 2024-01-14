from sql import Others as con
query="select id from product"
d=con().run_query(query,).fetchall()
print(d)
for i in d:
    parameters=(0,)
    print(parameters)
    query="Update product set mesProximoDevovlucion = ? "
    con().run_query(query,parameters)
