def query_balance(phone: str):
    """查询余额工具，返回结构化结果。"""
    phone = phone or "unknown"
    balance = 50

    return {
        "success": True,
        "data": {
            "phone": phone,
            "balance": balance,
            "currency": "CNY",
        },
        "message": f"手机号 {phone}，当前余额 {balance} 元",
        "error_code": None,
    }


def query_order(order_id: str):
    """订单查询工具。当前作为示例接口预留。"""
    return {
        "success": True,
        "data": {"order_id": order_id, "status": "processing"},
        "message": f"订单 {order_id} 当前处理中。",
        "error_code": None,
    }


def create_ticket(issue: str):
    """创建工单工具。"""
    return {
        "success": True,
        "data": {"ticket_id": "TICKET-0001", "issue": issue},
        "message": "工单已创建，客服人员将尽快处理。",
        "error_code": None,
    }


def escalate_to_human():
    """转人工客服工具。"""
    return {
        "success": True,
        "data": {"status": "queued"},
        "message": "已为您转人工客服。",
        "error_code": None,
    }