from service.exceptions.exceptions import StorageFacadeException
from storage.database import new_session


# Review this code and refactor all facade methods that use sessions of SQL to use this abstraction layer
# This is a policy to follow/use when you want to communicate with Postgres Database.
# This function takes care of transactions
async def run_with_transaction(work, session=None, should_commit=True):
    if session is None: session = new_session()
    try:
        result = await work(session)
        if should_commit: await session.commit()
        return result
    except Exception as e:
        print(e) # refactor using correct logging method
        await session.rollback()
        raise StorageFacadeException(e)
    finally:
        await session.close()