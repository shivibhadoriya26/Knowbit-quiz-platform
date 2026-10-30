
def main():
    while True:
        print("\n====== Test your knowledge ======")
        print("1. Registration")
        print("2. Login")
        print("3. Exit")

        ch = input("Choose an option: ")

        if ch == "1":
            registration()
        elif ch == "2":
            login()
        elif ch == "3":
            print("You have successfully exited the quiz")
            break
        else:
            print("Choose correct option")


user_details = {}
quiz_results = {}


def registration():
    print("\n==== Register Here ====")

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    contact = input("Enter contact number: ")
    enroll = input("Enter your enrollment number: ")
    college = input("Enter your college name: ")
    password = input("Enter password: ")

    if enroll in user_details:
        print("User already exists!")
        return

    user_details[enroll] = {
        "name": name,
        "email": email,
        "contact": contact,
        "college": college,
        "password": password
    }

    with open("registration.txt", "a") as file:
        file.write(f"Enrollment: {enroll}\n")
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Contact: {contact}\n")
        file.write(f"College: {college}\n")
        file.write("--------------------\n")

    print("Registration successful!")
    print("Please log in using your enrollment number and password.")


def login():
    print("\n---- LOGIN ----")

    enroll = input("Enter enrollment number: ")
    password = input("Enter password: ")

    if enroll in user_details and password == user_details[enroll]["password"]:
        print("Login successful!")

        with open("login.txt", "a") as file:
            file.write(f"{enroll},Login successful\n")

        dashboard(enroll)
    else:
        print("Invalid enrollment number or password.")


def dashboard(enroll):
    while True:
        print("\n====== DASHBOARD ======")
        print("1. Profile")
        print("2. Update profile")
        print("3. Attempt quiz")
        print("4. Result")
        print("5. Logout")

        opt = input("Choose an option: ")

        if opt == "1":
            profile(enroll)
        elif opt == "2":
            update_profile(enroll)
        elif opt == "3":
            attempt_quiz(enroll)
        elif opt == "4":
            result(enroll)
        elif opt == "5":
            logout(enroll)
            break
        else:
            print("Choose correct option")


def profile(enroll):
    print("\n---- PROFILE ----")
    print("Name:", user_details[enroll]["name"])
    print("Email id:", user_details[enroll]["email"])
    print("College:", user_details[enroll]["college"])
    print("Enrollment:", enroll)
    print("Contact no:", user_details[enroll]["contact"])


def update_profile(enroll):
    while True:
        print("\n---- UPDATE PROFILE ----")
        print("1. Update name")
        print("2. Update email")
        print("3. Update contact")
        print("4. Update college")
        print("5. Back")

        updatep = input("Choose an option: ")

        if updatep == "1":
            user_details[enroll]["name"] = input("Enter your new name: ")
            print("Profile updated successfully!")

        elif updatep == "2":
            user_details[enroll]["email"] = input("Enter your new email: ")
            print("Profile updated successfully!")

        elif updatep == "3":
            user_details[enroll]["contact"] = input("Enter your new contact: ")
            print("Profile updated successfully!")

        elif updatep == "4":
            user_details[enroll]["college"] = input("Enter your new college: ")
            print("Profile updated successfully!")

        elif updatep == "5":
            print("Back to dashboard")
            break

        else:
            print("Choose correct option")


def attempt_quiz(enroll):
    while True:
        print("\n------ Choose Quiz ------")
        print("1. DSA")
        print("2. DBMS")
        print("3. Python")
        print("4. System Design")
        print("5. Java")
        print("6. C++")
        print("7. Back to Dashboard")

        quiz = input("Choose a quiz: ")

        if quiz == "7":
            print("Back to dashboard")
            break

        elif quiz not in ["1", "2", "3", "4", "5", "6"]:
            print("Choose correct option")
            continue

        score = 0

        if quiz == "1":
            quiz_name = "DSA"
            print("\nYou are attempting quiz for DSA")

            q1 = input("""
1. Which data structure follows FIFO?
1. Stack
2. Queue
3. Tree
4. Graph
Enter your answer: """)
            if q1 == "2":
                score += 1

            q2 = input("""
2. Which data structure follows LIFO?
1. Queue
2. Array
3. Stack
4. Linked List
Enter your answer: """)
            if q2 == "3":
                score += 1

            q3 = input("""
3. What is the time complexity of Binary Search?
1. O(n)
2. O(log n)
3. O(n²)
4. O(1)
Enter your answer: """)
            if q3 == "2":
                score += 1

            q4 = input("""
4. Which data structure stores key-value pairs?
1. Stack
2. Queue
3. Hash Table
4. Tree
Enter your answer: """)
            if q4 == "3":
                score += 1

            q5 = input("""
5. Which data structure is used in BFS?
1. Queue
2. Stack
3. Heap
4. Array
Enter your answer: """)
            if q5 == "1":
                score += 1

            q6 = input("""
6. Which operation adds an element to a stack?
1. Pop
2. Push
3. Dequeue
4. Remove
Enter your answer: """)
            if q6 == "2":
                score += 1

            q7 = input("""
7. Which data structure represents hierarchical relationships?
1. Queue
2. Stack
3. Tree
4. Array
Enter your answer: """)
            if q7 == "3":
                score += 1

            q8 = input("""
8. What is the worst-case complexity of linear search?
1. O(1)
2. O(log n)
3. O(n)
4. O(n²)
Enter your answer: """)
            if q8 == "3":
                score += 1

            q9 = input("""
9. Which data structure is used for undo operations?
1. Stack
2. Queue
3. Graph
4. Tree
Enter your answer: """)
            if q9 == "1":
                score += 1

            q10 = input("""
10. Which traversal visits left subtree, root, then right subtree?
1. Preorder
2. Inorder
3. Postorder
4. Level order
Enter your answer: """)
            if q10 == "2":
                score += 1

            q11 = input("""
11. Which data structure stores elements at indexed positions?
1. Array
2. Graph
3. Tree
4. Stack only
Enter your answer: """)
            if q11 == "1":
                score += 1

            q12 = input("""
12. Which data structure is commonly used in DFS?
1. Queue
2. Stack
3. Hash Table
4. Array only
Enter your answer: """)
            if q12 == "2":
                score += 1

            q13 = input("""
13. What is the average time complexity of searching in a hash table?
1. O(n)
2. O(log n)
3. O(1)
4. O(n²)
Enter your answer: """)
            if q13 == "3":
                score += 1

            q14 = input("""
14. Which structure connects nodes using edges?
1. Stack
2. Queue
3. Graph
4. Array
Enter your answer: """)
            if q14 == "3":
                score += 1

            q15 = input("""
15. Which sorting algorithm repeatedly selects the smallest remaining element?
1. Merge Sort
2. Selection Sort
3. Quick Sort
4. Heap Sort
Enter your answer: """)
            if q15 == "2":
                score += 1

            q16 = input("""
16. What is the worst-case time complexity of Merge Sort?
1. O(n²)
2. O(log n)
3. O(n log n)
4. O(1)
Enter your answer: """)
            if q16 == "3":
                score += 1

            q17 = input("""
17. Which data structure is used to implement a priority queue efficiently?
1. Heap
2. Stack
3. Linked List only
4. String
Enter your answer: """)
            if q17 == "1":
                score += 1

            q18 = input("""
18. What is a node in a linked list?
1. A type of loop
2. An element containing data and links
3. A sorting method
4. A database query
Enter your answer: """)
            if q18 == "2":
                score += 1

            q19 = input("""
19. Which algorithm finds the shortest paths from a source in a graph with non-negative weights?
1. Binary Search
2. Dijkstra's Algorithm
3. Bubble Sort
4. Linear Search
Enter your answer: """)
            if q19 == "2":
                score += 1

            q20 = input("""
20. Which technique solves a problem by breaking it into smaller subproblems?
1. Recursion
2. Compilation
3. Indexing
4. Hashing only
Enter your answer: """)
            if q20 == "1":
                score += 1

        elif quiz == "2":
            quiz_name = "DBMS"
            print("\nYou are attempting quiz for DBMS")

            q1 = input("""
1. Which SQL command retrieves data?
1. INSERT
2. SELECT
3. UPDATE
4. DELETE
Enter your answer: """)
            if q1 == "2":
                score += 1

            q2 = input("""
2. Which key uniquely identifies a record?
1. Foreign Key
2. Candidate Key
3. Primary Key
4. Alternate Key
Enter your answer: """)
            if q2 == "3":
                score += 1

            q3 = input("""
3. Which command removes a table?
1. DELETE
2. DROP
3. UPDATE
4. SELECT
Enter your answer: """)
            if q3 == "2":
                score += 1

            q4 = input("""
4. What does SQL stand for?
1. Structured Query Language
2. Simple Question Language
3. Sequential Query Logic
4. System Query Link
Enter your answer: """)
            if q4 == "1":
                score += 1

            q5 = input("""
5. Which command inserts new records?
1. INSERT
2. DROP
3. SELECT
4. ALTER
Enter your answer: """)
            if q5 == "1":
                score += 1

            q6 = input("""
6. Which clause filters rows?
1. ORDER BY
2. WHERE
3. GROUP BY
4. FROM
Enter your answer: """)
            if q6 == "2":
                score += 1

            q7 = input("""
7. Which key connects records between tables?
1. Primary Key
2. Foreign Key
3. Alternate Key
4. Super Key
Enter your answer: """)
            if q7 == "2":
                score += 1

            q8 = input("""
8. Which command modifies existing records?
1. UPDATE
2. CREATE
3. SELECT
4. DROP
Enter your answer: """)
            if q8 == "1":
                score += 1

            q9 = input("""
9. What is a main goal of normalization?
1. Increase duplicate data
2. Reduce data redundancy
3. Remove all keys
4. Delete all tables
Enter your answer: """)
            if q9 == "2":
                score += 1

            q10 = input("""
10. Which SQL function counts rows?
1. SUM()
2. AVG()
3. COUNT()
4. MAX()
Enter your answer: """)
            if q10 == "3":
                score += 1

            q11 = input("""
11. Which SQL command changes a table structure?
1. ALTER
2. SELECT
3. INSERT
4. COMMIT
Enter your answer: """)
            if q11 == "1":
                score += 1

            q12 = input("""
12. Which command removes specific rows from a table?
1. DROP
2. DELETE
3. CREATE
4. ALTER
Enter your answer: """)
            if q12 == "2":
                score += 1

            q13 = input("""
13. Which clause sorts query results?
1. WHERE
2. HAVING
3. ORDER BY
4. JOIN
Enter your answer: """)
            if q13 == "3":
                score += 1

            q14 = input("""
14. What does a foreign key help maintain?
1. Referential integrity
2. Screen resolution
3. Program speed
4. File compression
Enter your answer: """)
            if q14 == "1":
                score += 1

            q15 = input("""
15. Which normal form removes partial dependency?
1. 1NF
2. 2NF
3. 3NF
4. 4NF
Enter your answer: """)
            if q15 == "2":
                score += 1

            q16 = input("""
16. Which SQL command saves a transaction permanently?
1. ROLLBACK
2. COMMIT
3. DELETE
4. DROP
Enter your answer: """)
            if q16 == "2":
                score += 1

            q17 = input("""
17. Which join returns matching rows from both tables?
1. INNER JOIN
2. CROSS JOIN
3. FULL JOIN only
4. SELF JOIN only
Enter your answer: """)
            if q17 == "1":
                score += 1

            q18 = input("""
18. What does ACID stand for in database transactions?
1. Atomicity, Consistency, Isolation, Durability
2. Access, Control, Input, Data
3. Automatic, Central, Indexed, Distributed
4. Array, Column, Integer, Database
Enter your answer: """)
            if q18 == "1":
                score += 1

            q19 = input("""
19. Which command gives a user database permissions?
1. GRANT
2. SELECT
3. UPDATE
4. ORDER BY
Enter your answer: """)
            if q19 == "1":
                score += 1

            q20 = input("""
20. Which SQL clause groups rows with the same values?
1. WHERE
2. GROUP BY
3. ORDER BY
4. DISTINCT
Enter your answer: """)
            if q20 == "2":
                score += 1

        elif quiz == "3":
            quiz_name = "Python"
            print("\nYou are attempting quiz for Python")

            q1 = input("""
1. Which keyword defines a function?
1. func
2. define
3. def
4. function
Enter your answer: """)
            if q1 == "3":
                score += 1

            q2 = input("""
2. Which data type stores key-value pairs?
1. List
2. Tuple
3. Dictionary
4. Set
Enter your answer: """)
            if q2 == "3":
                score += 1

            q3 = input("""
3. Which loop iterates over a sequence?
1. if
2. for
3. def
4. break
Enter your answer: """)
            if q3 == "2":
                score += 1

            q4 = input("""
4. Which symbol starts a single-line comment?
1. //
2. #
3. /*
4. --
Enter your answer: """)
            if q4 == "2":
                score += 1

            q5 = input("""
5. Which data type represents True or False?
1. int
2. str
3. bool
4. list
Enter your answer: """)
            if q5 == "3":
                score += 1

            q6 = input("""
6. Which method adds an item to a list?
1. append()
2. add_item()
3. push()
4. include()
Enter your answer: """)
            if q6 == "1":
                score += 1

            q7 = input("""
7. What is the result of 3 ** 2?
1. 5
2. 6
3. 9
4. 8
Enter your answer: """)
            if q7 == "3":
                score += 1

            q8 = input("""
8. Which keyword handles an exception?
1. catch
2. except
3. error
4. handle
Enter your answer: """)
            if q8 == "2":
                score += 1

            q9 = input("""
9. Which function returns the length of a list?
1. size()
2. count()
3. len()
4. length()
Enter your answer: """)
            if q9 == "3":
                score += 1

            q10 = input("""
10. Which keyword imports a module?
1. include
2. using
3. import
4. module
Enter your answer: """)
            if q10 == "3":
                score += 1

            q11 = input("""
11. Which brackets are used to create a list?
1. ()
2. []
3. {}
4. <>
Enter your answer: """)
            if q11 == "2":
                score += 1

            q12 = input("""
12. Which function displays output in Python?
1. input()
2. print()
3. output()
4. show()
Enter your answer: """)
            if q12 == "2":
                score += 1

            q13 = input("""
13. Which function converts a value to an integer?
1. str()
2. float()
3. int()
4. bool()
Enter your answer: """)
            if q13 == "3":
                score += 1

            q14 = input("""
14. Which keyword is used to make a decision?
1. if
2. loop
3. def
4. import
Enter your answer: """)
            if q14 == "1":
                score += 1

            q15 = input("""
15. Which operator checks equality?
1. =
2. ==
3. !=
4. =>
Enter your answer: """)
            if q15 == "2":
                score += 1

            q16 = input("""
16. Which data type is immutable?
1. List
2. Dictionary
3. Tuple
4. Set
Enter your answer: """)
            if q16 == "3":
                score += 1

            q17 = input("""
17. Which keyword exits a loop immediately?
1. continue
2. pass
3. break
4. return
Enter your answer: """)
            if q17 == "3":
                score += 1

            q18 = input("""
18. What does range(5) generate?
1. Numbers 1 to 5
2. Numbers 0 to 4
3. Numbers 0 to 5
4. Only the number 5
Enter your answer: """)
            if q18 == "2":
                score += 1

            q19 = input("""
19. Which keyword creates an anonymous function?
1. lambda
2. anonymous
3. function
4. def
Enter your answer: """)
            if q19 == "1":
                score += 1

            q20 = input("""
20. Which file mode is commonly used to read a file?
1. w
2. a
3. r
4. x
Enter your answer: """)
            if q20 == "3":
                score += 1

        elif quiz == "4":
            quiz_name = "System Design"
            print("\nYou are attempting quiz for System Design")

            q1 = input("""
1. What does scalability mean?
1. Handle increased workload
2. Delete data
3. Shut down
4. Change programming language
Enter your answer: """)
            if q1 == "1":
                score += 1

            q2 = input("""
2. Which architecture separates an application into layers?
1. Monolithic
2. Layered Architecture
3. Peer-to-Peer
4. Serverless
Enter your answer: """)
            if q2 == "2":
                score += 1

            q3 = input("""
3. What is the purpose of a load balancer?
1. Store passwords
2. Distribute incoming traffic
3. Delete requests
4. Create database tables
Enter your answer: """)
            if q3 == "2":
                score += 1

            q4 = input("""
4. What does caching help reduce?
1. Response time
2. User accounts
3. Network addresses
4. Programming languages
Enter your answer: """)
            if q4 == "1":
                score += 1

            q5 = input("""
5. Which database commonly stores data in tables?
1. Relational database
2. Graph database
3. Key-value store
4. Document database
Enter your answer: """)
            if q5 == "1":
                score += 1

            q6 = input("""
6. What is horizontal scaling?
1. Adding more machines
2. Increasing one machine's capacity
3. Removing all servers
4. Reducing user accounts
Enter your answer: """)
            if q6 == "1":
                score += 1

            q7 = input("""
7. What is a microservice?
1. An independent service focused on a function
2. A database table
3. A network cable
4. A programming variable
Enter your answer: """)
            if q7 == "1":
                score += 1

            q8 = input("""
8. Why is a database index used?
1. To speed up data retrieval
2. To replace backups
3. To remove all records
4. To shut down servers
Enter your answer: """)
            if q8 == "1":
                score += 1

            q9 = input("""
9. What does fault tolerance aim to provide?
1. Continued operation despite some failures
2. Guaranteed zero cost
3. Unlimited storage
4. No need for testing
Enter your answer: """)
            if q9 == "1":
                score += 1

            q10 = input("""
10. What is the purpose of a message queue?
1. Enable asynchronous communication
2. Style a web page
3. Compile source code
4. Replace every database
Enter your answer: """)
            if q10 == "1":
                score += 1

            q11 = input("""
11. What is vertical scaling?
1. Adding more servers
2. Increasing the resources of one machine
3. Removing a database
4. Dividing a program into files
Enter your answer: """)
            if q11 == "2":
                score += 1

            q12 = input("""
12. What is an API used for?
1. Allowing software systems to communicate
2. Cooling a server
3. Formatting a hard drive
4. Replacing an operating system
Enter your answer: """)
            if q12 == "1":
                score += 1

            q13 = input("""
13. Which HTTP method is commonly used to retrieve data?
1. POST
2. DELETE
3. GET
4. PATCH
Enter your answer: """)
            if q13 == "3":
                score += 1

            q14 = input("""
14. What is a CDN primarily used for?
1. Delivering content from distributed locations
2. Writing source code
3. Managing passwords only
4. Creating database schemas
Enter your answer: """)
            if q14 == "1":
                score += 1

            q15 = input("""
15. What does database replication do?
1. Creates copies of data across systems
2. Deletes duplicate files
3. Compresses all images
4. Changes programming languages
Enter your answer: """)
            if q15 == "1":
                score += 1

            q16 = input("""
16. What is a bottleneck in a system?
1. A component limiting overall performance
2. A backup copy
3. A user interface
4. A programming keyword
Enter your answer: """)
            if q16 == "1":
                score += 1

            q17 = input("""
17. What is the purpose of a firewall?
1. Increase screen brightness
2. Filter network traffic based on rules
3. Store application data
4. Compile programs
Enter your answer: """)
            if q17 == "2":
                score += 1

            q18 = input("""
18. What is eventual consistency?
1. Replicas become consistent after updates propagate
2. Data is never updated
3. Every request deletes data
4. A server never fails
Enter your answer: """)
            if q18 == "1":
                score += 1

            q19 = input("""
19. What does latency measure?
1. Delay in completing a request
2. Number of database tables
3. Amount of source code
4. Number of programming languages
Enter your answer: """)
            if q19 == "1":
                score += 1

            q20 = input("""
20. Why are backups important?
1. To recover data after loss
2. To increase screen resolution
3. To replace every database
4. To eliminate all network traffic
Enter your answer: """)
            if q20 == "1":
                score += 1

        elif quiz == "5":
            quiz_name = "Java"
            print("\nYou are attempting quiz for Java")

            q1 = input("""
1. Which keyword is used to create a class in Java?
1. define
2. class
3. struct
4. create
Enter your answer: """)
            if q1 == "2":
                score += 1

            q2 = input("""
2. Which method is the entry point of a Java program?
1. start()
2. run()
3. main()
4. init()
Enter your answer: """)
            if q2 == "3":
                score += 1

            q3 = input("""
3. Which data type stores whole numbers?
1. int
2. String
3. boolean
4. char
Enter your answer: """)
            if q3 == "1":
                score += 1

            q4 = input("""
4. Which keyword creates an object in Java?
1. make
2. object
3. new
4. create
Enter your answer: """)
            if q4 == "3":
                score += 1

            q5 = input("""
5. Which symbol ends most Java statements?
1. :
2. ;
3. ,
4. .
Enter your answer: """)
            if q5 == "2":
                score += 1

            q6 = input("""
6. Which type stores true or false?
1. int
2. char
3. boolean
4. String
Enter your answer: """)
            if q6 == "3":
                score += 1

            q7 = input("""
7. Which keyword is used for inheritance in Java?
1. extends
2. inherits
3. implements
4. super
Enter your answer: """)
            if q7 == "1":
                score += 1

            q8 = input("""
8. Which method compares the contents of strings?
1. ==
2. compare()
3. equals()
4. same()
Enter your answer: """)
            if q8 == "3":
                score += 1

            q9 = input("""
9. Which package is automatically imported in Java?
1. java.util
2. java.lang
3. java.io
4. java.net
Enter your answer: """)
            if q9 == "2":
                score += 1

            q10 = input("""
10. Which keyword prevents a class from being inherited?
1. static
2. private
3. final
4. const
Enter your answer: """)
            if q10 == "3":
                score += 1

            q11 = input("""
11. Which keyword is used to inherit an interface implementation?
1. extends
2. implements
3. imports
4. package
Enter your answer: """)
            if q11 == "2":
                score += 1

            q12 = input("""
12. Which collection stores unique elements?
1. ArrayList
2. HashSet
3. LinkedList
4. Vector
Enter your answer: """)
            if q12 == "2":
                score += 1

            q13 = input("""
13. Which keyword refers to the current object?
1. super
2. this
3. current
4. self
Enter your answer: """)
            if q13 == "2":
                score += 1

            q14 = input("""
14. Which access modifier allows access from anywhere?
1. private
2. protected
3. public
4. default
Enter your answer: """)
            if q14 == "3":
                score += 1

            q15 = input("""
15. Which block is used to handle exceptions?
1. try-catch
2. if-else
3. for-while
4. class-object
Enter your answer: """)
            if q15 == "1":
                score += 1

            q16 = input("""
16. Which keyword is used to define a constant-like variable?
1. final
2. fixed
3. constant
4. staticonly
Enter your answer: """)
            if q16 == "1":
                score += 1

            q17 = input("""
17. Which class is commonly used for reading console input?
1. Scanner
2. Printer
3. ConsoleReaderOnly
4. InputText
Enter your answer: """)
            if q17 == "1":
                score += 1

            q18 = input("""
18. Which concept allows one method name with different parameter lists?
1. Encapsulation
2. Method overloading
3. Garbage collection
4. Abstraction only
Enter your answer: """)
            if q18 == "2":
                score += 1

            q19 = input("""
19. What is the parent class of Java classes when no other parent is specified?
1. Main
2. Object
3. Parent
4. Class
Enter your answer: """)
            if q19 == "2":
                score += 1

            q20 = input("""
20. Which keyword exits a method and optionally sends a value back?
1. break
2. continue
3. return
4. exit
Enter your answer: """)
            if q20 == "3":
                score += 1

        elif quiz == "6":
            quiz_name = "C++"
            print("\nYou are attempting quiz for C++")

            q1 = input("""
1. Which symbol is used to end most C++ statements?
1. :
2. ;
3. ,
4. .
Enter your answer: """)
            if q1 == "2":
                score += 1

            q2 = input("""
2. Which header is commonly used for input and output?
1. <stdio.h>
2. <iostream>
3. <string.h>
4. <math.h>
Enter your answer: """)
            if q2 == "2":
                score += 1

            q3 = input("""
3. Which operator is used to get input with cin?
1. <<
2. >>
3. ==
4. &&
Enter your answer: """)
            if q3 == "2":
                score += 1

            q4 = input("""
4. Which keyword declares a class in C++?
1. object
2. class
3. define
4. create
Enter your answer: """)
            if q4 == "2":
                score += 1

            q5 = input("""
5. Which data type stores a whole number?
1. int
2. float
3. char
4. string
Enter your answer: """)
            if q5 == "1":
                score += 1

            q6 = input("""
6. Which loop checks its condition before each iteration?
1. do-while
2. while
3. switch
4. goto
Enter your answer: """)
            if q6 == "2":
                score += 1

            q7 = input("""
7. Which operator accesses a member through an object?
1. ->
2. .
3. ::
4. &
Enter your answer: """)
            if q7 == "2":
                score += 1

            q8 = input("""
8. Which concept allows the same function name with different parameters?
1. Encapsulation
2. Inheritance
3. Function overloading
4. Abstraction
Enter your answer: """)
            if q8 == "3":
                score += 1

            q9 = input("""
9. Which keyword allocates memory dynamically in C++?
1. malloc
2. new
3. create
4. alloc
Enter your answer: """)
            if q9 == "2":
                score += 1

            q10 = input("""
10. Which keyword returns a value from a function?
1. break
2. stop
3. return
4. continue
Enter your answer: """)
            if q10 == "3":
                score += 1

            q11 = input("""
11. Which operator is used to display output with cout?
1. >>
2. <<
3. ==
4. !=
Enter your answer: """)
            if q11 == "2":
                score += 1

            q12 = input("""
12. Which function is the usual entry point of a C++ program?
1. start()
2. run()
3. main()
4. begin()
Enter your answer: """)
            if q12 == "3":
                score += 1

            q13 = input("""
13. Which keyword is used to create an object dynamically?
1. new
2. class
3. object
4. this
Enter your answer: """)
            if q13 == "1":
                score += 1

            q14 = input("""
14. Which concept hides data and combines it with methods?
1. Inheritance
2. Encapsulation
3. Compilation
4. Recursion
Enter your answer: """)
            if q14 == "2":
                score += 1

            q15 = input("""
15. Which access specifier makes class members accessible only inside the class?
1. public
2. protected
3. private
4. global
Enter your answer: """)
            if q15 == "3":
                score += 1

            q16 = input("""
16. Which loop executes its body at least once?
1. for
2. while
3. do-while
4. range
Enter your answer: """)
            if q16 == "3":
                score += 1

            q17 = input("""
17. Which operator checks whether two values are equal?
1. =
2. ==
3. =>
4. :=
Enter your answer: """)
            if q17 == "2":
                score += 1

            q18 = input("""
18. Which feature allows a derived class to use a base class's features?
1. Inheritance
2. Encapsulation
3. Indexing
4. Compilation
Enter your answer: """)
            if q18 == "1":
                score += 1

            q19 = input("""
19. Which standard library container stores elements in sequence and supports indexing?
1. map
2. vector
3. set
4. stack only
Enter your answer: """)
            if q19 == "2":
                score += 1

            q20 = input("""
20. Which keyword can be used to define a constant variable?
1. const
2. fixed
3. constant
4. final
Enter your answer: """)
            if q20 == "1":
                score += 1

        print("\nYour score:", score, "/ 20")

        quiz_results[enroll] = {
            "quiz": quiz_name,
            "score": score
        }

        with open("results.txt", "a") as file:
            file.write(
                f"Enrollment: {enroll}, "
                f"Quiz: {quiz_name}, Score: {score}/20\n"
            )


def result(enroll):
    print("\n------ QUIZ RESULT ------")

    if enroll in quiz_results:
        print("Quiz:", quiz_results[enroll]["quiz"])
        print("Your score:", quiz_results[enroll]["score"], "/ 3")
    else:
        print("You have not attempted any quiz yet!")


def logout(enroll):
    print("Successfully logged out!")


main()

