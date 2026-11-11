# Week 12 answers

## Exercise 1
1. The customer typed "I want to change my shipping address," "It's order A102," and "9 Pine Street, Tampa."
2. Two tool requests were refused. The model first used order ID A100 and then an address the customer had never provided.
3. Ollama receives 14 messages: one system message, three user messages, three assistant messages, six messages representing the three tool calls, and the new "thanks" message.
4. The payment safety rule detects the word "card" in "gift cards" and sends the question to a human. This is acceptable because an unnecessary handoff is safer than potentially allowing sensitive payment information to reach the model.

## Exercise 3
**Terminal output:**
```text
Type a message, or type quit to stop.
You: I want to change my shipping address
Sunny: Your request to change the shipping address for order A100 has been submitted and is awaiting staff approval.
You: quit
Messages in this conversation: 3
Staff review
Request 1: A100 to 123 Main St, Anytown, AN 12345
Approve? yes or no: no
Request 1 rejected.
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street
```

**What happened:**
With the `customer_said()` check disabled, Sunny submitted an address change using order A100 and an address I never provided. The request reached staff review, where I rejected it, so the original address remained unchanged. This is dangerous because a staff member could accidentally approve an unauthorized change and send someone's package to the wrong address. Keeping the guardrail enabled prevents this by requiring the customer to provide the order ID and address before submitting a request.