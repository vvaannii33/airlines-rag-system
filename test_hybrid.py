from app.hybrid_pipeline import HybridPipeline

pipeline = HybridPipeline()

questions = [

    
    "Show me all the flights available"
]

for q in questions:
    print("\nQuestion:", q)
    response = pipeline.run(q)
    print("Response:", response)