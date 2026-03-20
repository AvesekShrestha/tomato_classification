from sqlalchemy.ext.asyncio import AsyncSession
from routes.v1.post.post_repository import PostRepository
from routes.v1.post.comment.comment_repository import CommentRepository
from routes.v1.post.reaction.dto.reaction_request import ReactionRequest
from routes.v1.post.dto.post_response import PostResponse
from routes.v1.post.comment.dto.comment_response import CommentResponse 
from schemas.comment import Comment
from schemas.reaction import TargetType
from .reaction_repository import ReactionRepository
from schemas.post import Post

class ReactionService : 

    def __init__(self) : 
        self.reaction_repository = ReactionRepository()
        self.post_repository = PostRepository()
        self.comment_repository = CommentRepository()

    async def toggle_post_reaction(self, payload : ReactionRequest, user_id : int, db : AsyncSession) -> PostResponse:

        post : Post = await self.post_repository.find_by_id(post_id=payload.target_id, db=db)
        updated_post : Post = await self.reaction_repository.toggle_reaction(payload=payload, user_id=user_id, target=post, db=db)

        response : PostResponse = PostResponse(
            id=updated_post.id,
            title=updated_post.title,
            content=updated_post.content,
            like=updated_post.like,
            dislike=updated_post.dislike,
            image=updated_post.image,
            user=updated_post.user,
            create_at=updated_post.created_at
        )  
        return response

    async def toggle_comment_reaction(self, payload : ReactionRequest, user_id : int, db : AsyncSession) -> CommentResponse:

        payload = payload.model_copy(update={"target_type" : TargetType.COMMENT})
        comment : Comment = await self.comment_repository.find_by_id(comment_id=payload.target_id, db=db)

        updated_comment : Comment = await self.reaction_repository.toggle_reaction(payload=payload, user_id=user_id, target=comment, db=db)

        response : CommentResponse = CommentResponse(
            id=updated_comment.id,
            content=updated_comment.content,
            like=updated_comment.like,
            dislike=updated_comment.dislike,
            created_at=updated_comment.created_at,
            user=updated_comment.user
        )

        return response

