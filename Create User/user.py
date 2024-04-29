import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserData:
    id: str
    full_name: str
    mob_num: str
    pan_num: str
    manager_id: str
    created_at: str = str(datetime.now())
    is_active: bool = True

    def generate_id(self):
        """
        generates uuid for the user
        """
        self.id = str(uuid.uuid4())
