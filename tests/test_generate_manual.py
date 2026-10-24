from app.generate import generate_answer


context = """
Company Leave Policy

Employees can carry forward a maximum of 5 unused annual leave
days into the next calendar year.
"""

answer = generate_answer(
    question="How many annual leave days can employees carry forward?",
    context=context,
)

print("Generated answer:", answer)
