from app.services.sql_chain import SQLChain

chain = SQLChain()

# Test questions
questions = [
    "Which passenger are flying from Bangalore to Delhi?"
]

for q in questions:
    print("\nQuestion:", q)
    response = chain.run(q)
    print("Generated SQL:", response["sql"])
    print("Result:", response["result"])