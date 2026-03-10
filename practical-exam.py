import csv

FILENAME = "Admission.csv"

#Function to add a record
def WriteRecord():
    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)

        reg = input("Enter Registration Number: ")
        name = input("Enter Candidate Name: ")
        city = input("Enter City: ")

        record = [reg, name, city]
        writer.writerow(record)

        print("Record added successfully.\n")


#Function to display all records
def DisplayRecord():
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            print("\nReg_Number\tCandidate_Name\tCity")
            print("-" * 40)
            for row in reader:
                print(row[0], "\t\t", row[1], "\t\t", row[2])
            print()
    except FileNotFoundError:
        print("File not found.\n")


# Function to search by registration number
def SearchRegNumber():
    reg_search = input("Enter Registration Number to search: ")
    found = False

    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == reg_search:
                print("\nRecord Found:")
                print("Reg Number:", row[0])
                print("Name:", row[1])
                print("City:", row[2])
                found = True
                break

    if not found:
        print("Record not found.\n")


# Function to search by city
def SearchCity():
    city_search = input("Enter City to search: ")
    found = False

    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        print("\nMatching Records:")
        for row in reader:
            if row[2].lower() == city_search.lower():
                print(row)
                found = True

    if not found:
        print("No record found for this city.\n")


# Menu Driven Program
while True:
    print("Candidate Record Keeping")
    print("1. Add Record")
    print("2. Display Record")
    print("3. Search RegRecord")
    print("4. Search City")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        WriteRecord()
    elif choice == '2':
        DisplayRecord()
    elif choice == '3':
        SearchRegNumber()
    elif choice == '4':
        SearchCity()
    elif choice == '5':
        print("Program terminated.")
        break
    else:
        print("Invalid choice. Try again.\n")
