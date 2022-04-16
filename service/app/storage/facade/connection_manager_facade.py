from storage.database import new_session
from storage.storage import storage

async def checkhealth_of_db():
    session = new_session()
    try:
        res = await storage.healthcheck(session)
        return res
    except Exception as e:
        print(e)
        return None
    finally:
        session.close()
