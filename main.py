from fastapi import FastAPI

app = FastAPI()

@app.get('/students')
async def list_students():
    pass

@app.post('/students')
async def create_students():
    pass
    
@app.get('/students/{id}')
async def fetch_student():
    pass

@app.patch('/students/{id}')
async def update_student():
    pass

@app.delete('/students/{id}')
def delete_student():
    pass