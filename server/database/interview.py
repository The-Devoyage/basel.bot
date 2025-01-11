from enum import Enum
from typing import List, Optional
from classes.user_claims import UserClaims
from database.base import BaseMongoModel


class InterviewType(str, Enum):
    APPLICATION = "application"
    GENERAL = "general"


class Interview(BaseMongoModel):
    name: str
    description: str
    url: Optional[str] = None
    organization_name: Optional[str] = None
    interview_type: InterviewType = InterviewType.GENERAL
    position: Optional[str] = None
    tags: List[str] = []
    status: bool = True


def get_pipeline(user_claims: Optional[UserClaims], taken_by_me: bool = False):
    pipeline = [
        {
            "$lookup": {
                "from": "InterviewQuestion",
                "localField": "_id",
                "foreignField": "interview.$id",
                "as": "questions",
            }
        },
        {
            "$unwind": {
                "path": "$questions",
                "preserveNullAndEmptyArrays": True,
            }
        },
    ]

    # Add the conditional `$lookup` for `InterviewQuestionResponse`
    if user_claims and taken_by_me:
        pipeline.append(
            {
                "$lookup": {
                    "from": "InterviewQuestionResponse",
                    "let": {"question_id": "$questions._id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": [
                                                "$interview_question.$id",
                                                "$$question_id",
                                            ]
                                        },
                                        {"$eq": ["$user.$id", user_claims.user.id]},
                                    ]
                                }
                            }
                        },
                        {
                            "$group": {
                                "_id": "$interview_question.$id",  # Group by question ID
                                "response_count": {"$sum": 1},  # Count unique responses
                            }
                        },
                    ],
                    "as": "question_responses",
                }
            }
        )
    else:
        pipeline.append(
            {
                "$lookup": {
                    "from": "InterviewQuestionResponse",
                    "let": {"question_id": "$questions._id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": [
                                        "$interview_question.$id",
                                        "$$question_id",
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "question_responses",
                }
            }
        )

    # Continue with the rest of the pipeline
    pipeline += [
        {"$addFields": {"questions.response_count": {"$size": "$question_responses"}}},
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "description": {"$first": "$description"},
                "url": {"$first": "$url"},
                "organization_name": {"$first": "$organization_name"},
                "interview_type": {"$first": "$interview_type"},
                "position": {"$first": "$position"},
                "tags": {"$first": "$tags"},
                "status": {"$first": "$status"},
                "question_count": {"$sum": 1},
                "response_count": {"$sum": "$questions.response_count"},
                "created_at": {"$first": "$created_at"},
                "updated_at": {"$first": "$updated_at"},
                "deleted_at": {"$first": "$deleted_at"},
            }
        },
        {
            "$match": {
                "response_count": {"$gt": 0}
                if (taken_by_me and user_claims)
                else {"$gte": 0}
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "description": 1,
                "url": 1,
                "organization_name": 1,
                "interview_type": 1,
                "position": 1,
                "tags": 1,
                "status": 1,
                "question_count": 1,
                "response_count": 1,
                "created_at": 1,
                "updated_at": 1,
                "deleted_at": 1,
            }
        },
    ]
    return pipeline
