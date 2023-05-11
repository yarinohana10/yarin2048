
import pymongo
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# async def main():
#     return {"message": "Hello World"}


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["admin"]
print(db)
collection = db["player_name"]

all_records = collection.find()

# for row in all_records:
#      print(row)

@app.post("/api/v1/players")
def save_player(name: str, score: int):
    player = {"name": name, "score": score}
    result = collection.insert_one(player)
    return {"id": str(result.inserted_id)}


@app.put("/api/v1/players/{name}")
def update_player(name: str, score: int):
    query = {"name": name}
    update = {"$set": {"score": score}}
    result = collection.update_one(query, update)
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": "Player score updated successfully"}




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)
