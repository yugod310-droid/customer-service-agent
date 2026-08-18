from pathlib import Path


KNOWLEDGE_FILE = Path(__file__).resolve().parents[2] / "data" / "knowledge" / "faqs.txt"


def _load_faqs():
    if not KNOWLEDGE_FILE.exists():
        return []

    entries = []
    current = {}

    for line in KNOWLEDGE_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Q:"):
            if current.get("question"):
                entries.append(current)
            current = {"question": line[2:].strip(), "answer": ""}
        elif line.startswith("A:"):
            if current:
                current["answer"] = line[2:].strip()
    if current.get("question"):
        entries.append(current)

    return entries


def search_knowledge(query: str):
    text = (query or "").lower()
    records = _load_faqs()

    matches = []
    for item in records:
        q = item.get("question", "").lower()
        a = item.get("answer", "").lower()
        score = 0
        if q and any(keyword in q for keyword in ["退款", "到账", "流程", "政策", "说明"]):
            score += 1
        if any(keyword in text for keyword in ["退款", "到账", "多久", "流程", "政策", "说明", "如何", "怎么办"]):
            score += 1
        if any(keyword in q for keyword in ["退款", "到账", "多久", "流程", "政策", "说明"]):
            score += 1
        if any(keyword in text for keyword in ["退款", "到账", "多久", "流程", "政策", "说明"]):
            score += 1

        if text and (text in q or q in text or any(keyword in q for keyword in text.split()) or any(keyword in text for keyword in q.split())):
            score += 2

        if score > 0:
            matches.append({"question": item.get("question"), "answer": item.get("answer"), "score": score})

    if not matches:
        return {"matches": [], "answer": "暂无相关知识库记录，建议转人工客服。"}

    matches = sorted(matches, key=lambda item: item["score"], reverse=True)
    best = matches[0]
    return {
        "matches": matches[:3],
        "answer": best["answer"],
        "source": "knowledge_base",
    }
