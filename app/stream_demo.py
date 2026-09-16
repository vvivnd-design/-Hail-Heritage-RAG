import asyncio
from datetime import datetime, timezone

class Broker:
    def __init__(self): self.documents=asyncio.Queue()

async def producer(b):
    for source in ["museum_profile_01.pdf","visitor_center_survey_02.pdf","museum_policy_03.pdf"]:
        event={"type":"document_updated","source":source,"time":datetime.now(timezone.utc).isoformat()}
        await b.documents.put(event); print("PRODUCED",event); await asyncio.sleep(.1)
    await b.documents.put(None)

async def consumer(b):
    while True:
        event=await b.documents.get()
        if event is None: break
        print("CONSUMED",{**event,"quality_gate":"passed","index_action":"scheduled"})

async def main():
    b=Broker(); await asyncio.gather(producer(b),consumer(b))
if __name__=="__main__": asyncio.run(main())
