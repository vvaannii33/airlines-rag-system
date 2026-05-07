from app.services.sql_chain import SQLChain

chain = SQLChain()

# Test questions
questions = [
    "What is probation?"
]

for q in questions:
    print("\nQuestion:", q)
    response = chain.run(q)
    print("Generated SQL:", response["sql"])
    print("Result:", response["result"])