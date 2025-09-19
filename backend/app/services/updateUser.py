from beanie import PydanticObjectId
from app.models.User import Users
from app.exceptions import UserNotFoundException, UserAlreadyVerifiedException

class UserService:
    @staticmethod
    async def verifyUserByEmail(email: str):
        """
        Finds a user by email, verifies them, and saves the change.
        Returns the updated user object.
        """
        user = await Users.find_one(Users.email == email)
        if not user:
            raise UserNotFoundException("User with that email not found.")

        if user.isVerified:
            raise UserAlreadyVerifiedException("Account is already verified.")

        user.isVerified = True
        await user.save()
        return user