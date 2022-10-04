import pymysql
import cv2
import numpy as np
from PIL import Image
import io
# database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="source")
print(connection)
cursor = connection.cursor()

MyCursor = connection.cursor()


# print("1., Insert image\n", "2. Read Image")
# MenuInput = input()


def InsertBlob(filepath, filename, email):
    with open(filepath, "rb") as file:
        BinaryData = file.read()
    SQLStatement = "INSERT INTO Images (Photo, name, email) VALUES (%s, %s, %s)"
    MyCursor.execute(SQLStatement, (BinaryData, filename, email))
    connection.commit()


def RetrieveBlob(ID):
    SQLStatement2 = "SELECT * FROM Images WHERE id = '{0}'"
    MyCursor.execute(SQLStatement2.format(str(ID)))
    MyResult = MyCursor.fetchone()[1]
    StoreFilePath = "RetrievedImages/img{0}.jpg".format(str(ID))
    print(MyResult[:10])
    image_file = io.BytesIO(MyResult)
    image = Image.open(image_file)
    with open(StoreFilePath, "wb") as File:
        # File.write(MyResult)
        image.save(File, "JPEG")
        image = np.asarray(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow("Generated Image", image)
        cv2.waitKey(0)
        File.close()


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

# if int(MenuInput) == 1:
#     user-file_path = input("Enter a file path ")
#     InsertBlob(user-file_path)
# elif int(MenuInput) == 2:
#     userID = input("Enter ID  ")
#     RetrieveBlob(userID)

# RetrieveBlob(29)
