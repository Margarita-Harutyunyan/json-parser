import json
import random
import string

def generateRandomJsonFile(filename):
    data = generateRandomData()
    with open(filename, 'w') as file:
        json.dump(data, file, indent = 4)
    return list(data.keys())

def generateRandomData():
    data = {
        "name": generateRandomString(),
        "age": random.randint(18, 30),
        "address": generateRandomAddress(),
        "scores": generateRandomScores()
    }
    return data

def generateRandomString(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generateRandomAddress():
    address = {
        "street": generateRandomString(),
        "city": generateRandomString(),
        "country": generateRandomString()
    }
    return address

def generateRandomScores():
    subjects = ["Math", "Science", "History", "English"]
    scores = {}
    for subject in subjects:
        scores[subject] = random.randint(60, 100)
    return scores

generateRandomJsonFile("random_data.json")
