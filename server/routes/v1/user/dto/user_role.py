from enum import Enum

class UserRole(str, Enum) : 
    FARMER = "farmer"
    ADMIN = "admin"
    EXPERT = "expert"

