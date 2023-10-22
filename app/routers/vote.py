from fastapi import status,HTTPException,Depends,Response, APIRouter
from .. import schemas, models, oath2
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} doesn't exist") # ensures that the post being voted on by the user exists

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
       if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
       new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
       db.add(new_vote)
       db.commit()

       return {"message": "successfully added a vote."}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found.")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfuly deleted vote."}