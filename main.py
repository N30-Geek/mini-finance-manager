from db.database import Database

if __name__ == "__main__":
    db = Database()
    if  db.add_user(
        "Néo geek",
        "dryikob878@gmail.com",
        "hacker0070",
        "KJDKlkjklsl89@@",
    ):
        print("The user was saved successffy")
    else:
        print("Something is wrong!")
