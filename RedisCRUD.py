# ============================================================
# Name: Steven McGraw
# Student ID: stemcg2613
# Course: SDC435 - Advanced Databases
# Assignment: Redis CRUD Python Application
# Date: November 21, 2026
#
# Purpose:
# This program connects to a Redis database using Python.
# It allows users to create, retrieve, update, and delete
# Redis sets through a menu-driven application.
# ============================================================

import redis
from datetime import datetime


# Connect to the Redis database
def connect_to_redis():
    try:
        connection = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )

        connection.ping()
        print("Successfully connected to Redis!")
        return connection

    except redis.RedisError as error:
        print(f"Redis connection error: {error}")
        return None


# Display the main menu
def display_menu():
    print("\n========== REDIS DATABASE MANAGER ==========")
    print("1. Query for set members")
    print("2. Add a new set")
    print("3. Update members of a set")
    print("4. Delete a set")
    print("5. Delete all data from the database")
    print("6. Exit the program")
    print("============================================")


# Create a new Redis set
def create_set(connection):
    print("\n--- CREATE A NEW SET ---")

    key = input("Enter the key for the new set: ").strip()

    if not key:
        print("Error: Set key cannot be empty.")
        return

    if connection.exists(key):
        print("Error: This key already exists.")
        return

    try:
        count = int(input("How many members will this set have? "))

        if count <= 0:
            print("Please enter a number greater than zero.")
            return

        members = []

        for number in range(count):
            member = input(
                f"Enter member {number + 1}: "
            ).strip()

            if member:
                members.append(member)

        if members:
            connection.sadd(key, *members)
            print(f"\nSet '{key}' created successfully!")
            print(f"Members: {connection.smembers(key)}")

        else:
            print("No valid members were entered.")

    except ValueError:
        print("Error: Please enter a valid number.")

    except redis.RedisError as error:
        print(f"Redis error: {error}")


# Retrieve members from a Redis set
def retrieve_set(connection):
    print("\n--- RETRIEVE SET MEMBERS ---")

    key = input("Enter the key of the set to retrieve: ").strip()

    try:
        if not connection.exists(key):
            print("Error: Set does not exist.")
            return

        members = connection.smembers(key)

        print(f"\nSet Name: {key}")
        print("Set Members:")

        for member in sorted(members):
            print(f"- {member}")

        print(f"Total Members: {len(members)}")

    except redis.RedisError as error:
        print(f"Redis error: {error}")


# Update an existing Redis set
def update_set(connection):
    print("\n--- UPDATE SET MEMBERS ---")

    key = input("Enter the key of the set to update: ").strip()

    try:
        if not connection.exists(key):
            print("Error: Set does not exist.")
            return

        while True:
            print("\n========== UPDATE SET MENU ==========")
            print("1. Add a member")
            print("2. Remove a member")
            print("3. Remove all members")
            print("4. Return to main menu")

            choice = input("Select an option: ").strip()

            if choice == "1":
                member = input("Enter member to add: ").strip()

                if member:
                    connection.sadd(key, member)
                    print(f"Member '{member}' added successfully.")

            elif choice == "2":
                member = input("Enter member to remove: ").strip()

                result = connection.srem(key, member)

                if result:
                    print(f"Member '{member}' removed successfully.")
                else:
                    print("Member was not found.")

            elif choice == "3":
                members = connection.smembers(key)

                if members:
                    connection.srem(key, *members)
                    print("All members removed successfully.")
                else:
                    print("Set is already empty.")

                print(f"Set cardinality: {connection.scard(key)}")

                break

            elif choice == "4":
                break

            else:
                print("Invalid option. Please try again.")

    except redis.RedisError as error:
        print(f"Redis error: {error}")


# Delete Redis set
def delete_set(connection):
    print("\n--- DELETE A SET ---")

    key = input("Enter the key of the set to delete: ").strip()

    try:
        result = connection.delete(key)

        if result:
            print(f"Set '{key}' deleted successfully.")
        else:
            print("Set does not exist.")

    except redis.RedisError as error:
        print(f"Redis error: {error}")


# Delete all data from the Redis database
def delete_all_data(connection):
    print("\n--- DELETE ALL DATABASE DATA ---")

    confirmation = input(
        "Are you sure you want to delete ALL data? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        try:
            connection.flushdb()
            print("All Redis database data deleted successfully.")

        except redis.RedisError as error:
            print(f"Redis error: {error}")

    else:
        print("Database deletion canceled.")


# Main application
def main():
    print("============================================")
    print("SDC435 - REDIS CRUD APPLICATION")
    print("Student: Steven McGraw")
    print("Student ID: stemcg2613")
    print("============================================")

    print(f"System Date and Time: {datetime.now()}")

    connection = connect_to_redis()

    if connection is None:
        print("Unable to start application.")
        return

    while True:
        display_menu()

        choice = input("\nEnter your menu selection (1-6): ").strip()

        if choice == "1":
            retrieve_set(connection)

        elif choice == "2":
            create_set(connection)

        elif choice == "3":
            update_set(connection)

        elif choice == "4":
            delete_set(connection)

        elif choice == "5":
            delete_all_data(connection)

        elif choice == "6":
            print("\nExiting Redis Database Manager.")
            print("Goodbye!")
            connection.close()
            break

        else:
            print("Invalid selection. Please enter 1-6.")


# Start the application
if __name__ == "__main__":
    main()
