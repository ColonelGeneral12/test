from fastapi import FastAPI
from app.routers.vote import vote
#from . import models
#from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, users, auth, vote

#models.Base.metadata.create_all(bind=engine) # creates the needed tables

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "hello world"}

# This is how to execute queries using raw sql
# @app.get("/")
# def root():
#   cursor.execute("""SELECT * FROM post""")
#  posts = cursor.fetchall()   #retreving all possible posts
# return posts

# @app.post("/posts", status_code = status.HTTP_201_CREATED)
# def create(post: schemas.PostCreate):
#  new_post = cursor.fetchone()
#  conn.commit()  # saves the input to the database
#   return new_post

# @app.get("/posts/{id}")
# def get_post(id: int):  # fast api validates that the id is an integer
##  post = cursor.fetchone()
# if not post:
#    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
# return post

# @app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):

#   cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id)))
#  deleted_post = cursor.fetchone()
# conn.commit()

# if deleted_post == None:
##return {'message': 'post succesfully deleted'}

# @app.put("/posts/{id}")
# def update_post(id: int,post: schemas.PostCreate):
#   cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
## conn.commit()

#  if updated_posts == None:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

# return updated_posts
