from client_side_api import VerifyUser

if __name__ == '__main__':
    status = VerifyUser(unverified=True)
    unverified_users = status.ids
    for unverified_user in unverified_users:
        user = VerifyUser(id = unverified_user)
        discord_username = user.username #username will follow the format 'member#xxxx'
        # using discord.py api get member with the username 
        # guild.get_member_name(discord_username) -> This should return a server member object where you can add roles 
        print(user.__dict__)