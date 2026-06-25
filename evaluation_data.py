from dotenv import load_dotenv
load_dotenv()
from datasets import Dataset, Features, Value, Sequence
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from app.services.rag_pipeline import RAGPipeline
from app.utils.logger_config import logger
import pandas as pd

rag_pipeline = RAGPipeline()
request_counter = 0

evaluation_data = [
    {"question" : "What is the probation period for technical roles?",
     "ground_truth" : "120 calendar days"
    },
    {"question" : "How many bereavement leave days are allowed?",
     "ground_truth" : "Up to 5 consecutive working days"
    },
    {"question" : "When is final settlement processed?",
     "ground_truth" : "Within 7 working days after clearance"
    },
    {"question" : "What is the impact of probation on benefits?",
     "ground_truth" : "Employees are not eligible for Annual leave encashment,Internal role transfers and Performance bonuses"
    },
    {"question" : "When is the mid-probation review conducted?",
     "ground_truth" : "Conducted at 45 days for 90-day probations, or at 60 days for 120-day probations."
    },
    {"question" : "Within how many days of the final review must confirmation decision be made?",
     "ground_truth" : "Within 5 working days."
    },
    {"question" : "What is the time period for reporting suspected violations of equal opportunity and anti-discrimination policies?",
     "ground_truth" : "Within 15 working days of occurence or discovery."
    },
    {"question" : "What is the criteria for probation extension?",
     "ground_truth" : f"""The employee has achieved at least 60% of their probationary objectives. 
                        b. A written PIP with measurable targets is issued within 5 working days of the 
                        original probation end date. 
                        c. The Department Head and HR Manager both sign off on the extension 
                        request. """
    },
    {"question" : "When is the final probation review conducted?",
     "ground_truth" : "Conducted within the last 10 working days of the probation period."
    },
    {"question" : "When must the company property be returned by employee during the exit procedure?",
     "ground_truth" : "Company property (ID badge, uniforms, devices) must be returned on or before the last working day."
    }   
]

features = Features({
    "question" : Value("string"),
    "ground_truth" : Value("string"),
    "answer" : Value("string"),
    "contexts" : Sequence(Value("string")),
    "retrieval_time": Value("float32"),
    "generation_time":Value("float32"),
    "total_time": Value("float32"),
    "total_tokens": Value("int32"),
    "cost": Value("float32")
    })

results = []
question_number = 1
for item in evaluation_data:

    response = rag_pipeline.run(item["question"])

    results.append({
        "question": item["question"],
        "ground_truth": item["ground_truth"],
        "answer": response.answer,
        "contexts": response.context_docs,
        "retrieval_time": response.retrieval_time,
        "generation_time":response.generation_time,
        "total_time":response.total_time,
        "total_tokens": response.total_tokens,
        "cost": response.cost
    })
    question_number = 1

    for row in results:
        print(f"Question {question_number}:", row["question"])
        print("Answer:", row["answer"])
        print("Contexts:", row["contexts"])
        print("="*50)
        question_number += 1

dataset = Dataset.from_list(results, features=features)

result = evaluate(
    dataset,
    metrics = [faithfulness, answer_relevancy]
)

print(result.to_pandas())

df = pd.DataFrame(results)
df.to_csv("evaluation_results.csv", index=False)
print("Evaluation results saved to evaluation_results.csv")
