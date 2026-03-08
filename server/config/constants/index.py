from dotenv import load_dotenv
import os

load_dotenv()


database_url = os.environ["DATABASE_URL"]
jwt_private_key = os.environ["JWT_PRIVATE_KEY"]



