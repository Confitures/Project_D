import os

a1 = os.path
print(f'a1 = {a1}')
print(str(a1))


a2 = [os.path.join('BASE_DIR', 'templates')]
print(f'a2 = {a2}')

# Path
path = "/home"
# Join various path components
print(os.path.join(path, "User/Desktop", "file.txt"))
# /home\User/Desktop\file.txt


# Path
path = "User/Documents"
# Join various path components
print(os.path.join(path, "home", "file.txt"))
# /home\file.txt


# Path
path = "/User"
# Join various path components
print(os.path.join(path, "Downloads", "file.txt", "/home"))
# /home



# Path
path = "/user1"
# Join various path components
print(os.path.join(path, path, path, path))
print(os.path.join('path', 'path', 'path', 'path'))
print(os.path.join(path+'1', path, path, path+'4'))
