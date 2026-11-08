## My Business Assistant — Campus Study Hub

I created a study room assistant called Casey for a fictional business, Campus Study Hub. The assistant uses a separate tool to check available study rooms in different buildings. The room availability data is simulated and does not represent actual reservations. Requests to reserve, cancel, or change a booking are directed to the front desk because they require human assistance. If real student data were used, the assistant could provide inaccurate information or expose private reservation details.


## Week 11 — Adding a Model to My Assistant

I added an Ollama model to my study room assistant so it can answer questions that my Python rules do not cover. The model correctly answered that the study hub closes at 10 pm using the information in its instructions. When I asked whether the study hub sells coffee, the model said it did not know and suggested asking the front desk. I kept room availability checks in Python so the assistant uses the room lookup tool instead of guessing which rooms are available. I also kept reservation requests in Python because the model should not make or change reservations on its own.