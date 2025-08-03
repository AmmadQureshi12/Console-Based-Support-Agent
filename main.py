# from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool
# from agents.run import RunConfig
# from pydantic import BaseModel

# # ---------------- ✅ User Context ----------------
# class UserContext(BaseModel):
#     name: str
#     is_premium_user: bool
#     issue_type: str  # billing or technical

# # ---------------- 🔐 Gemini API Setup ----------------
# gemini_api_key = "AIzaSyBcuIq6WJpTnrlbcZPql8G2X_RE-7LMhv8"  # Replace with your actual Gemini API key

# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True,
# )

# # ---------------- 🔧 Tools ----------------
# @function_tool
# def refund(context: UserContext) -> str:
#     if context.is_premium_user:
#         return f"✅ Refund has been issued for {context.name}."
#     return "❌ Refunds are only available for premium users."

# @function_tool
# def restart_service(context: UserContext) -> str:
#     if context.issue_type.lower() == "technical":
#         return f"🔁 Service has been restarted successfully for {context.name}."
#     return "⚠️ No technical issue found. Restart not needed."

# # ---------------- 🧾 Specialized Agents ----------------
# billing_agent = Agent(
#     name="billing_agent",
#     instructions="You are a billing assistant. Help users with billing issues like invoices, payments, refunds, etc.",
#     model=model,
#     tools=[refund]
# )

# technical_agent = Agent(
#     name="technical_agent",
#     instructions="You are a technical assistant. Help users with technical issues like errors, bugs, or internet problems.",
#     model=model,
#     tools=[restart_service]
# )

# # ---------------- 📦 Triage Agent ----------------
# triage_agent = Agent(
#     name="triage_agent",
#     instructions="""
# You are a smart support assistant. Your job is to decide whether a user's issue is about billing or technical support.

# - If user mentions refund, money, or billing → hand off to Billing Agent.
# - If user mentions error, restart, service, or technical issue → hand off to Technical Agent.
# - If it's something else, respond politely that we can't help with that.

# Always choose the correct handoff.
# """,
#     model=model,
#     handoffs=[billing_agent, technical_agent]
# )

# # ---------------- 🖥️ CLI Interface ----------------
# def main():
#     print("\n📞 Welcome to Console Support System (by Ammad Qureshi)\n")
#     name = input("Enter Your Name: ")
#     premium_input = input("Are you a Premium user? (Yes/No): ").strip().lower()
#     is_premium = premium_input == "yes"

#     issue_type = input("Is your issue technical or billing?: ").strip().lower()

#     context = UserContext(
#         name=name,
#         is_premium_user=is_premium,
#         issue_type=issue_type,
#     )

#     print("\n✅ You can now start chatting with support (type 'exit' to quit)\n")

#     while True:
#         user_input = input(f"{context.name}: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("👋 Thank you for using Support. Goodbye!")
#             break

#         # Build full input message
#         full_input = f"""
# User Name: {context.name}
# Premium User: {context.is_premium_user}
# Issue Type: {context.issue_type}

# User Query: {user_input}
# """

#         print("\n🤖 [Triage Agent analyzing your query... Please wait]\n")

#         try:
#             result = Runner.run_sync(
#                 triage_agent,
#                 input=full_input,
#             )

#             output_text = result.final_output.lower()

#             # 🧠 Simple keyword check to simulate handoff
#             if "refund" in output_text or "invoice" in output_text:
#                 print("📡 Transferring to **billing_agent**...\n")
#             elif "restart" in output_text or "error" in output_text or "service" in output_text:
#                 print("📡 Transferring to **technical_agent**...\n")
#             else:
#                 print("📨 Message handled directly by triage agent.\n")

#             print("✅ Final Output:\n")
#             print(result.final_output)

#         except Exception as e:
#             print("⚠️ Error:", e)

# # ---------------- ▶️ Run ----------------
# if __name__ == "__main__":
#     main()

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool
from agents.run import RunConfig
from pydantic import BaseModel

# ---------------- ✅ User Context ----------------
class UserContext(BaseModel):
    name: str
    is_premium_user: bool
    issue_type: str  # billing or technical

# ---------------- 🔐 Gemini API Setup ----------------
gemini_api_key = "AIzaSyBcuIq6WJpTnrlbcZPql8G2X_RE-7LMhv8"  # Replace with your actual Gemini API key

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# ---------------- 🔧 Tools ----------------
@function_tool
def refund(context: UserContext) -> str:
    if context.is_premium_user:
        return f"✅ Refund has been issued for {context.name}."
    return "❌ Refunds are only available for premium users."

@function_tool
def restart_service(context: UserContext) -> str:
    if context.issue_type.lower() == "technical":
        return f"🔁 Service has been restarted successfully for {context.name}."
    return "⚠️ No technical issue found. Restart not needed."

# ---------------- 🧾 Specialized Agents ----------------
billing_agent = Agent(
    name="billing_agent",
    instructions="You are a billing assistant. Help users with billing issues like invoices, payments, refunds, etc.",
    model=model,
    tools=[refund]
)

technical_agent = Agent(
    name="technical_agent",
    instructions="You are a technical assistant. Help users with technical issues like errors, bugs, or internet problems.",
    model=model,
    tools=[restart_service]
)

# ---------------- 📦 Triage Agent ----------------
triage_agent = Agent(
    name="triage_agent",
    instructions="""
You are a smart support assistant. Your job is to decide whether a user's issue is about billing or technical support.

- If user mentions refund, money, or billing → hand off to Billing Agent.
- If user mentions error, restart, service, or technical issue → hand off to Technical Agent.
- If it's something else, respond politely that we can't help with that.

Always choose the correct handoff.
""",
    model=model,
    handoffs=[billing_agent, technical_agent]
)

# ---------------- 🖥️ CLI Interface ----------------
def main():
    print("\n📞 Welcome to Console Support System (by Ammad Qureshi)\n")
    name = input("Enter Your Name: ")
    premium_input = input("Are you a Premium user? (Yes/No): ").strip().lower()
    is_premium = premium_input == "yes"

    issue_type = input("Is your issue technical or billing?: ").strip().lower()

    context = UserContext(
        name=name,
        is_premium_user=is_premium,
        issue_type=issue_type,
    )

    print("\n✅ You can now start chatting with support (type 'exit' to quit)\n")

    while True:
        user_input = input(f"{context.name}: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Thank you for using Support. Goodbye!")
            break

        # Full input for the triage agent
        full_input = f"""
User Name: {context.name}
Premium User: {context.is_premium_user}
Issue Type: {context.issue_type}

User Query: {user_input}
"""

        print("\n🤖 [Triage Agent analyzing your query... Please wait]\n")

        try:
            # Step 1: Run triage agent
            result = Runner.run_sync(
                triage_agent,
                input=full_input,
            )

            output_text = result.final_output.lower()

            # Step 2: Display LLM's routing decision
            print("🤖 Triage Agent Decision:")
            print(result.final_output)

            # Step 3: Follow up with correct agent based on LLM message
            if "billing" in output_text:
                print("\n🔁 Handoff to Billing Agent...\n")
                billing_result = Runner.run_sync(
                    billing_agent,
                    input=user_input,
                )
                print("📦 Billing Agent Says:\n", billing_result.final_output)

            elif "technical" in output_text:
                print("\n🔁 Handoff to Technical Agent...\n")
                technical_result = Runner.run_sync(
                    technical_agent,
                    input=user_input,
                )
                print("🛠 Technical Agent Says:\n", technical_result.final_output)

            else:
                print("📨 No handoff. Message handled directly.\n")

        except Exception as e:
            print("⚠️ Error:", e)

# ---------------- ▶️ Run ----------------
if __name__ == "__main__":
    main()
