import logging
import sqlite3
from datetime import datetime
from typing import Optional, Union
from classes.profile_picture import ProfilePicture
from sqlite3 import Cursor
from classes.user import User

logger = logging.getLogger(__name__)

class ProfilePictureModel:
  def __init__(self, db_path):
    self.db_path = db_path 

  def _get_connection(self):
    return sqlite3.connect(self.db_path)
  
  def get_profile_picture_by_user_id(
    self, cursor: Cursor, user_id: int
  ) -> Optional[ProfilePicture]:
    cursor.execute(
      """
      SELECT * FROM profile_picture WHERE user_id = ?
      """,
      (user_id,),
    )
    row = cursor.fetchone()
    if not row:
      return None
    columns = [column[0] for column in cursor.description]
    data = dict(zip(columns, row))
    return ProfilePicture(**data)

  # def get_profile_pictures()