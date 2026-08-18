from app.config.settings import DEFAULT_PHONE
from app.rag.knowledge_base import search_knowledge
from app.tools.customer_tools import query_balance


def route_intent(user_input: str) -> str:
    text = (user_input or "").lower()

    if any(keyword in text for keyword in ["余额", "花费", "消费", "剩余"]):
        return "balance"
    if any(keyword in text for keyword in ["订单", "物流", "快递"]):
        return "order"
    if any(keyword in text for keyword in ["退款", "到账", "政策", "说明", "流程", "多久"]):
        return "knowledge"
    if any(keyword in text for keyword in ["投诉", "故障", "问题", "工单"]):
        return "ticket"
    if any(keyword in text for keyword in ["人工", "转人工", "客服"]):
        return "human_handoff"

    return "unknown"


def execute_action(intent: str, user_input: str):
    if intent == "balance":
        return {
            "success": True,
            "intent": "balance",
            "tool": "query_balance",
            "data": query_balance(DEFAULT_PHONE),
            "message": "已为您查询账户余额。",
        }

    if intent == "order":
        return {
            "success": True,
            "intent": "order",
            "tool": "query_order",
            "data": {"order_id": None, "status": "not_implemented"},
            "message": "订单查询功能已预留，当前为示例版本。",
        }

    if intent == "knowledge":
        result = search_knowledge(user_input)
        return {
            "success": True,
            "intent": "knowledge",
            "tool": "search_knowledge",
            "data": result,
            "message": result.get("answer", "已为您查询相关知识。"),
        }

    if intent == "ticket":
        return {
            "success": True,
            "intent": "ticket",
            "tool": "create_ticket",
            "data": {"ticket_id": "TICKET-0001"},
            "message": "已为您创建工单，客服人员会尽快处理。",
        }

    if intent == "human_handoff":
        return {
            "success": True,
            "intent": "human_handoff",
            "tool": "escalate_to_human",
            "data": {"status": "queued"},
            "message": "已为您转接人工客服。",
        }

    return {
        "success": True,
        "intent": "unknown",
        "tool": None,
        "data": {},
        "message": "我目前可以帮助您查询余额，或为您转接人工客服。",
    }


def handle_customer_query(user_input: str):
    intent = route_intent(user_input)
    result = execute_action(intent, user_input)

    return {
        "intent": result.get("intent"),
        "success": result.get("success", True),
        "message": result.get("message", ""),
        "data": result.get("data", {}),
        "tool": result.get("tool"),
    }


def run_agent(user_input: str):
    return handle_customer_query(user_input)