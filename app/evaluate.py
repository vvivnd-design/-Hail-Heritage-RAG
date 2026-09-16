from app.vector_store import VectorStore
TESTS=[
    ("ما الهدف من منصة راوي حائل؟","المتاحف"),
    ("كيف تتعامل المنصة مع البيانات الشخصية؟","البيانات"),
    ("ماذا تفعل بوابة جودة البيانات؟","الجودة"),
]
def run():
    store=VectorStore(); passed=0
    for q,term in TESTS:
        ok=term in " ".join(x["text"] for x in store.search(q,3))
        passed+=int(ok); print(("PASS" if ok else "FAIL"),q)
    print(f"Retrieval hit rate: {passed}/{len(TESTS)}")
if __name__=="__main__": run()
