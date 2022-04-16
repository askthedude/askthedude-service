from storage.facade import connection_manager_facade


async def healthcheck():
    res = await connection_manager_facade.checkhealth_of_db()
    return res
