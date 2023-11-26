from fastapi import HTTPException
from sqlalchemy import or_

# Search Method. Get a list of records based on the search parameter
def search_records(table, columns, param, connection):
    try:
        # Search in all selected columns with an or_
        filters = [column.like(f"%{param}%") for column in columns]
        query = table.select().where(or_(*filters))

        # Send back everything
        result = connection.execute(query)
        records = []
        for row in result:
            records.append(row._mapping)
        
        return records
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

# Generic Search Operation. Right now only works with one column
def create_search_route(table, column, model, connection, app):
    @app.get(f"/search{table.name.lower()}/{{param}}")
    async def search_record_route(param: str):
        records = search_records(table, column, param, connection)
        return records


"""
# Read (Get)
@app.get(f"/{table.name.lower()}/{{id}}")
async def read_record_route(id: int):
    record = read_record(table, id, connection)
    return record
"""

"""
# Get Method. Get the data from the Database
def read_record(table, id, connection):
    try:
        query = table.select().where(table.c.Id == id)
        result = connection.execute(query)
        row = result.first()
        return row._mapping
    
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")
"""

# Search Broker
"""
@app.get("/searchbroker/{name}")
async def get_broker(name: str):
    try:
        result = connection.execute(brokers.select().where(
            or_(
                brokers.c.First_Name.like(f"%{name}%"),
                brokers.c.Last_Name.like(f"%{name}%")
            )))
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")
    
    rows = [
            {
                "Id": row.Id,
                "First_Name": row.First_Name,
                "Last_Name": row.Last_Name,
                "Email_Address": row.Email_Address,
                "Username": row.Username,
                "Password": row.Pass
            }
            for row in result
    ]
    
    return rows
"""