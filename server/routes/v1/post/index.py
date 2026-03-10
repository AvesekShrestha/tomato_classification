from config.database.index import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,APIRouter
from routes.v1.post.dto.post_response import PostResponse
from routes.v1.post.dto.post_request import PostRequest
from schemas.post import Post
from utils.errors.index import NotFound
from utils.response.index import ResponseModel
from typing import List

router=APIRouter()

@router.get("/posts/{post_id}",response_model=ResponseModel[PostResponse])
def read_posts_by_id(post_id:int,db:AsyncSession=Depends(get_db)) -> ResponseModel[PostResponse]:
    post=db.query(Post).filter(Post.id==post_id).first()
    if not post:
        raise NotFound("Post not found")
    else:
        return ResponseModel[PostResponse](
            success=True,
            data=post,
            message="Post retrieved successfully"  
        )
       


@router.get("/posts/",response_model=ResponseModel[List[PostResponse]]) 
def read_posts(db:AsyncSession=Depends(get_db)) :
    posts=db.query(Post).all()
    if not posts:
        raise NotFound("No any posts found")
    return ResponseModel[PostResponse](
        Success=True,
        data=posts,
        message="All posts are retrieved successfully"
    )


@router.post("/posts/{post_id}",response_model=PostResponse)
def post_create(post:PostRequest,db:AsyncSession=Depends(get_db)):
    db_user=db.query(User).filter(User.id==post.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found")
    
    #create post
    db_posts=Post(content=post.content,
                  likes=post.likes,
                  dislikes=post.dislikes,
                  user_id=post.user_id)  #later get from JWT authentication. for now explicitly provided from JSON 
    db.add(db_posts)
    db.commit()
    db.refresh(db_posts)
    return db_posts


@router.patch("/posts/{post_id}")
def update_post(post_id:int,post:PostUpdate,db:AsyncSession=Depends(get_db)):
    db_posts=db.query(Post).filter(Post.id==post_id).first()
    if not db_posts:
        raise HTTPException(status_code=404,detail="post not found")
    else:
        update_data=post.dict(exclude_unset=True)
        for key,value in update_data.items():
            setattr(db_posts,key,value)

        db.commit()
        db.refresh(db_posts)
        return db_posts
    

@router.delete("/posts/{post_id}")
def delete_post(post_id:int,db:AsyncSession=Depends(get_db)):
    db_posts=db.query(Post).filter(Post.id==post_id).first()
    if not db_posts:
        raise HTTPException(status_code=404,detail="post not found")
    else:
        db.delete(db_posts)
        db.commit()
        return{"detail":f"Post with {post_id} deleted successfully"}
    