from app.chains.sql_chain import SQLChain

sql_chain = SQLChain()

questions = [
    "List all the table names present in the database" ]


for q in questions:
    print("\nQuestion:", q)
    response = sql_chain.run(q)
    print("Response:", response)