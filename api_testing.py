from client_side_api import VerifyUser

if __name__ == '__main__':
    status = VerifyUser('prof#1234')
    print(status.isrole)