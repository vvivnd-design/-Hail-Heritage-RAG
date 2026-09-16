import requests
from app.config import settings

SYSTEM_PROMPT = '''أنت مساعد معرفي متخصص في التراث والمتاحف.
أجب حصرا من السياق المسترجع.
إذا لم يكف السياق، قل: «لا تتوافر في المصادر المفهرسة معلومات كافية للإجابة الموثوقة».
لا تخمن أسماء أو تواريخ أو أرقاما.
استخدم إحالات [1] و[2] عند الاستناد إلى المقاطع.'''

def fallback(contexts):
    if not contexts:
        return "لا تتوافر في المصادر المفهرسة معلومات كافية للإجابة الموثوقة."
    return "\n\n".join(
        ["لم يفعل نموذج التوليد؛ وهذه أكثر المقاطع صلة بالسؤال:"]
        + [f"[{i}] {c['text'][:450]}" for i,c in enumerate(contexts[:3],1)]
    )

def generate_answer(question, contexts):
    if not settings.openrouter_api_key:
        return fallback(contexts)
    context = "\n\n".join(
        f"[{i}] المصدر: {c['metadata'].get('source','unknown')}\n{c['text']}"
        for i,c in enumerate(contexts,1)
    )
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {settings.openrouter_api_key}", "Content-Type":"application/json"},
        json={"model":settings.openrouter_model,
              "messages":[{"role":"system","content":SYSTEM_PROMPT},
                          {"role":"user","content":f"السياق:\n{context}\n\nالسؤال: {question}"}],
              "temperature":0.1},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
