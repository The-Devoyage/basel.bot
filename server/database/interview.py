from enum import Enum
from typing import List, Optional
from beanie import BackLink, Link, PydanticObjectId
from pydantic import Field
import pymongo
from database.base import BaseMongoModel
from database.organization import Organization


class InterviewType(str, Enum):
    APPLICATION = "application"
    GENERAL = "general"


class Interview(BaseMongoModel):
    description: str
    position: str
    url: Optional[str] = None
    organization: Optional[Link[Organization]] = None
    questions: Optional[List[BackLink["InterviewQuestion"]]] = Field(  # type:ignore
        original_field="interview"  # type:ignore
    )
    interview_type: InterviewType = InterviewType.GENERAL
    tags: List[str] = []
    status: bool = True

    class Settings:
        indexes = [[("description", pymongo.TEXT), ("position", pymongo.TEXT)]]


def get_pipeline(
    user_id: Optional[PydanticObjectId] = None,
    taken_by_me: bool = False,
    is_public: bool = True,
    shareable_link_id: Optional[PydanticObjectId] = None,
):
    pipeline = [
        {
            "$lookup": {
                "from": "Organization",
                "localField": "organization.$id",
                "foreignField": "_id",
                "as": "organization",
            }
        },
        {
            "$unwind": {
                "path": "$organization",
                "preserveNullAndEmptyArrays": True,
            }
        },
    ]

    # Add the conditional `$lookup` for `InterviewTranscript`
    if user_id:
        pipeline.append(
            {
                "$lookup": {
                    "from": "InterviewTranscript",
                    "let": {"interview_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": [
                                                "$interview.$id",
                                                "$$interview_id",
                                            ]
                                        },
                                        {"$eq": ["$user.$id", user_id]},
                                    ]
                                }
                            }
                        },
                    ],
                    "as": "interview_transcripts",
                }
            }
        )
        # pipeline.append(
        #     {
        #         "$unwind": {
        #             "path": "$interview_transcripts",
        #             "preserveNullAndEmptyArrays": True,
        #         }
        #     }
        # )
        pipeline.append(
            {
                "$lookup": {
                    "from": "InterviewAssessment",
                    "let": {"interview_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": [
                                                "$interview.$id",
                                                "$$interview_id",
                                            ]
                                        },
                                        {"$eq": ["$user.$id", user_id]},
                                    ]
                                }
                            }
                        },
                    ],
                    "as": "assessment",
                }
            }
        )
        pipeline.append(
            {"$addFields": {"assessment": {"$arrayElemAt": ["$assessment", 0]}}}
        )
        if shareable_link_id:
            pipeline += [
                {
                    "$lookup": {
                        "from": "ShareableLink",
                        "let": {"interview_id": "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$and": [
                                            {
                                                "$eq": [
                                                    "$_id",
                                                    shareable_link_id,
                                                ]
                                            },
                                            {
                                                "$in": [
                                                    "$$interview_id",
                                                    {
                                                        "$ifNull": [
                                                            "$interviews.$id",
                                                            [],
                                                        ]
                                                    },
                                                ]
                                            },
                                        ]
                                    }
                                }
                            }
                        ],
                        "as": "matched_shareable_link",
                    }
                },
                {"$match": {"matched_shareable_link": {"$ne": []}}},
            ]

    # Get all assessment count
    pipeline.append(
        {
            "$lookup": {
                "from": "InterviewAssessment",
                "let": {"interview_id": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": [
                                    "$interview.$id",
                                    "$$interview_id",
                                ]
                            }
                        }
                    }
                ],
                "as": "total_assessments",
            }
        }
    )

    # Continue with the rest of the pipeline
    pipeline += [
        {
            "$addFields": {
                "total_assessments_count": {
                    "$size": {"$ifNull": ["$total_assessments", []]}
                }
            }
        },
        {
            "$addFields": {
                "interview_transcripts_count": {
                    "$size": {"$ifNull": ["$interview_transcripts", []]}
                }
            }
        },
        {"$addFields": {"organization": "$organization"}},
        {
            "$group": {
                "_id": "$_id",
                "uuid": {"$first": "$uuid"},
                "description": {"$first": "$description"},
                "url": {"$first": "$url"},
                "organization": {"$first": "$organization"},
                "interview_type": {"$first": "$interview_type"},
                "position": {"$first": "$position"},
                "tags": {"$first": "$tags"},
                "status": {"$first": "$status"},
                "total_assessments": {"$first": "$total_assessments_count"},
                "interview_transcripts_count": {
                    "$first": "$interview_transcripts_count"
                },
                "assessment": {"$first": "$assessment"},
                "created_at": {"$first": "$created_at"},
                "updated_at": {"$first": "$updated_at"},
                "deleted_at": {"$first": "$deleted_at"},
            }
        },
        {
            "$match": {
                "interview_transcripts_count": {"$gt": 0}
                if (taken_by_me and user_id)
                else {"$gte": 0}
            }
        },
        {
            "$project": {
                "_id": 0 if is_public else 1,
                "uuid": 1,
                "description": 1,
                "url": 1,
                "interview_type": 1,
                "position": 1,
                "organization.name": 1,
                "organization.uuid": 1,
                "organization.slug": 1,
                "tags": 1,
                "status": 1,
                "total_assessments": 1,
                "created_at": 1,
                "updated_at": 1,
                "deleted_at": 1,
                "started": {
                    "$cond": {
                        "if": {"$gt": ["$interview_transcripts_count", 0]},
                        "then": True,
                        "else": False,
                    }
                },
                "submitted": {
                    "$cond": {
                        "if": {"$ne": ["$assessment", None]},
                        "then": True,
                        "else": False,
                    }
                },
            }
        },
    ]
    return pipeline
