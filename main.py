from app.agent.customer_agent import handle_customer_query
from app.config.settings import PROJECT_NAME, VERSION


def main():
    print(f"欢迎使用{PROJECT_NAME} v{VERSION}")
    user_input = "查询余额"
    result = handle_customer_query(user_input)
    print(result)


if __name__ == "__main__":
    main()