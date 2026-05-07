from app.hybrid_pipeline import HybridPipeline

pipeline = HybridPipeline()

questions = [
    "Show flights after 10 AM and explain probation"
]



for q in questions:
    print("\nQuestion:", q)
    response = pipeline.run(q)
    print("Response:", response)