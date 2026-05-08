from app.hybrid_pipeline import HybridPipeline

pipeline = HybridPipeline()

questions = [

    # SQL
    "Show flights after 10 AM",

    # RAG
    "What is probation?",

    # Mixed
    "Show flights after 10 AM and explain probation",

    # Invalid
    "What is the capital of India?",

    # Ambiguous
    "Show flights",

    # Guardrail
    "Drop flights table",

    # Write operation
    "Insert into flights values (...)"
]



for q in questions:
    print("\nQuestion:", q)
    response = pipeline.run(q)
    print("Response:", response)