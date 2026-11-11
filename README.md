## My Business Assistant — Campus Study Hub

I created a study room assistant called Casey for a fictional business, Campus Study Hub. The assistant uses a separate tool to check available study rooms in different buildings. The room availability data is simulated and does not represent actual reservations. New reservation requests are submitted to a queue for front desk approval, while cancellations and reservation changes are directed to the front desk for human assistance. If real student data were used, the assistant could provide inaccurate information or expose private reservation details.


## Week 11 — Adding a Model to My Assistant

I added an Ollama model to my study room assistant so it can answer questions that my Python rules do not cover. The model correctly answered that the study hub closes at 10 pm using the information in its instructions. When I asked whether the study hub sells coffee, the model said it did not know and suggested asking the front desk. I kept room availability checks in Python so the assistant uses the room lookup tool instead of guessing which rooms are available. I also kept reservation requests in Python because the model should not make or change reservations on its own.


## Week 12 - Upgrading My Assistant

I upgraded Casey to use a model that can choose tools for checking study room availability and submitting reservation requests. I added a toolbox that checks for missing information, rejects details the student did not provide, and verifies that the requested room is available in the selected building. Reservation requests now enter a queue where the front desk must approve or reject them before a room is officially reserved. Casey still sends cancellations and reservation changes directly to the front desk without asking the model. I tested the upgraded assistant using FakeModel and the real Ollama model, and all 40 tests passed. This project showed me how Python rules, model-selected tools, and human approval can work together to make an assistant more reliable.