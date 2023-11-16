from fastapi import HTTPException

# Post Method. Insert data to the Database
def create_record(table, data, connection):
    try:
        query = table.insert().values(**data)
        result = connection.execute(query)
        connection.commit()
        return result.lastrowid
    
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

# Get Method. Get the data from the Database
def read_record(table, id, connection):
    try:
        query = table.select().where(table.c.Id == id)
        result = connection.execute(query)
        row = result.first()
        return row._mapping
    
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}")

# Put Method. Update the data in the Database
def update_record(table, id, data, connection):
    try:
        query = table.update().where(table.c.Id == id).values(**data)
        connection.execute(query)
        connection.commit()
        return
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}") 

# Delete Method. Delete the row with id in the Database
def delete_record(table, id, connection):
    try:
        query = table.delete().where(table.c.Id == id)
        connection.execute(query)
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Invalid Query: {e}") 

# Generic CRUD Operations!
def create_table_routes(table, model, connection, app):
    # Create (Post)
    @app.post(f"/{table.name.lower()}")
    async def create_record_route(item: model):
        id = create_record(table, item.model_dump(), connection)
        return {
            "message": f"{table.name} created",
            "Id": id
        }
    
    # Read (Get)
    @app.get(f"/{table.name.lower()}/{{id}}")
    async def read_record_route(id: int):
        record = read_record(table, id, connection)
        return record
    
    # Update (Put)
    @app.put(f"/{table.name.lower()}/{{id}}")
    async def update_record_route(id: int, item: model):
        update_record(table, id, item.model_dump(), connection)
        return { "message": f"{table.name} updated" }
    
    # Delete
    @app.delete(f"/{table.name.lower()}/{{id}}")
    async def delete_record_route(id: int):
        delete_record(table, id, connection)
        return { "message": f"{table.name} deleted" }