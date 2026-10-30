import streamlit as st
import hashlib
import hmac
import secrets
from pathlib import Path
from datetime import datetime

def show_brand():
    st.markdown(
        "<h2 style='color:#2563eb;'>Knowbit | Learn Smarter</h2>",
        unsafe_allow_html=True
    )

st.set_page_config(
    page_title="Knowbit | Learn Smarter",
    layout="wide",
    initial_sidebar_state="collapsed"
)
def show_footer():
    st.markdown(
        """
        <div style="text-align:center; padding:20px; color:#64748b;">
            © 2026 Knowbit | Learn Smarter
        </div>
        """,
        unsafe_allow_html=True
    )
# ---------- FILE STORAGE ----------
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

REGISTRATION_FILE = DATA_DIR / "registration.txt"
LOGIN_FILE = DATA_DIR / "login.txt"
RESULTS_FILE = DATA_DIR / "results.txt"

# ---------- SESSION INITIALIZATION ----------
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "register"

for file_path in (REGISTRATION_FILE, LOGIN_FILE, RESULTS_FILE):
    file_path.touch(exist_ok=True)


def hash_password(password, salt=None):
    """Return a salted PBKDF2 password hash and its salt."""
    salt = salt or secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        200_000
    ).hex()
    return salt, password_hash

def save_registration(full_name, username, email):
    with REGISTRATION_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{username}|{full_name}|{email}\n")


def save_login(username, password):
    salt, password_hash = hash_password(password)
    with LOGIN_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{username}|{salt}|{password_hash}\n")


def load_registered_users():
    users = {}
    with REGISTRATION_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            parts = line.rstrip("\n").split("|")
            if len(parts) == 3:
                username, full_name, email = parts
                users[username] = {
                    "full_name": full_name,
                    "email": email
                }
    return users


def load_login_records():
    records = {}
    with LOGIN_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            parts = line.rstrip("\n").split("|")
            if len(parts) == 3:
                username, salt, password_hash = parts
                records[username] = (salt, password_hash)
    return records


def verify_login(username, password):
    records = load_login_records()
    if username not in records:
        return False
    salt, saved_hash = records[username]
    _, entered_hash = hash_password(password, salt)
    return hmac.compare_digest(saved_hash, entered_hash)


def save_quiz_result(username, subject, score, total, accuracy):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with RESULTS_FILE.open("a", encoding="utf-8") as file:
        file.write(
            f"{username}|{subject}|{score}|{total}|{accuracy:.1f}|{timestamp}\n"
        )


def load_user_results(username):
    results = []
    with RESULTS_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            parts = line.rstrip("\n").split("|")
            if len(parts) == 6 and parts[0] == username:
                try:
                    results.append({
                        "subject": parts[1],
                        "score": int(parts[2]),
                        "total": int(parts[3]),
                        "accuracy": float(parts[4]),
                        "date": parts[5]
                    })
                except ValueError:
                    continue
    return results

# ---------- CUSTOM DESIGN ----------
st.markdown('''
<style>
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div,
[data-testid="stMetricLabel"] {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}
[data-testid="stMetric"] {
    background-color: #EAF0FF !important;
    padding: 16px !important;
    border-radius: 12px !important;
}
.stAlert [data-testid="stAlertContainer"] {
    background-color: #EAF0FF !important;
    color: #243D8E !important;
}
.stAlert [data-testid="stAlertContent"],
.stAlert [data-testid="stAlertContent"] p {
    color: #243D8E !important;
}
.stRadio label,
.stRadio label p,
.stRadio [data-testid="stMarkdownContainer"] p {
    color: #172033 !important;
}
.stRadio [role="radiogroup"] label {
    background-color: #FFFFFF !important;
    border: 1px solid #D1D9E8 !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    margin-bottom: 8px !important;
}
.stRadio [role="radiogroup"] label span,
.stRadio [role="radiogroup"] label p {
    color: #172033 !important;
}
.stRadio [role="radiogroup"] label:hover {
    border-color: #2563EB !important;
}
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #F5F7FB !important;
    color: #172033 !important;
}
.stTextInput input,
.stTextInput input:focus,
.stTextInput textarea {
    background-color: #FFFFFF !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    border: 1px solid #D1D9E8 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
.stTextInput label {
    color: #172033 !important;
}
.stTextInput input::placeholder {
    color: #68738A !important;
    opacity: 1 !important;
}
.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.stButton > button, .stFormSubmitButton > button {
    background-color: #2563EB !important;
    color: white !important;
    border: 2px solid #2563EB !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background-color: #1D4ED8 !important;
    border-color: #1D4ED8 !important;
}
.brand {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #2448C5;
}
.brand span { color: #172033; }
.hero {
    background: linear-gradient(120deg, #101B3C, #2448C5);
    padding: 46px 42px;
    border-radius: 22px;
    color: white;
    margin-top: 22px;
    margin-bottom: 32px;
}
.eyebrow {
    color: #C5D2FF;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
}
.hero h1 {
    color: white;
    font-size: 42px;
    line-height: 1.2;
    margin: 14px 0;
}
.hero p {
    color: #E0E7FF;
    font-size: 16px;
    max-width: 580px;
    line-height: 1.7;
}
.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #172033;
    margin-bottom: 4px;
}
.section-subtitle {
    color: #68738A;
    margin-bottom: 22px;
}
.quiz-card {
    background: white;
    border: 1px solid #E3E8F2;
    border-radius: 16px;
    padding: 25px 23px;
    min-height: 185px;
    margin-bottom: 18px;
    box-shadow: 0 5px 18px rgba(23, 32, 51, 0.035);
}
}
.quiz-number {
    color: #3155C8;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}
.quiz-card h3 {
    color: #172033;
    font-size: 21px;
    margin-top: 14px;
    margin-bottom: 8px;
}
.quiz-card p {
    color: #68738A;
    font-size: 14px;
    line-height: 1.6;
}
.info-strip {
    background: #EAF0FF;
    border: 1px solid #D9E3FF;
    padding: 18px 22px;
    border-radius: 13px;
    color: #243D8E;
    margin-top: 8px;
    margin-bottom: 30px;
    }
.footer-note {
    color: #7B8498;
    text-align: center;
    font-size: 12px;
    padding-top: 28px;
}
</style>
''', unsafe_allow_html=True)

# ---------- QUIZ QUESTIONS ----------
# Six subjects with 20 questions each.

quiz_data = {
    "DSA": [
        {"q": "Which data structure follows FIFO?", "o": ["Stack", "Queue", "Tree", "Graph"], "a": "Queue"},
        {"q": "Which data structure follows LIFO?", "o": ["Queue", "Stack", "Linked list", "Graph"], "a": "Stack"},
        {"q": "Which data structure stores key-value pairs?", "o": ["Stack", "Queue", "Hash table", "Tree only"], "a": "Hash table"},
        {"q": "What is the worst-case time complexity of linear search?", "o": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "a": "O(n)"},
        {"q": "Binary search requires which condition?", "o": ["Random data", "Sorted data", "A graph", "A stack"], "a": "Sorted data"},
        {"q": "Which structure is commonly used for BFS?", "o": ["Stack", "Queue", "Heap", "Array only"], "a": "Queue"},
        {"q": "Which structure is commonly used for DFS?", "o": ["Queue", "Stack", "Hash table", "Priority queue only"], "a": "Stack"},
        {"q": "Which sorting algorithm repeatedly selects the minimum element?", "o": ["Merge sort", "Selection sort", "Quick sort", "Heap sort"], "a": "Selection sort"},
        {"q": "What is the average time complexity of merge sort?", "o": ["O(n)", "O(log n)", "O(n log n)", "O(n²)"], "a": "O(n log n)"},
        {"q": "Which data structure represents hierarchical relationships?", "o": ["Queue", "Tree", "Stack", "Array"], "a": "Tree"},
        {"q": "What is a node in a linked list?", "o": ["Only an index", "Data and link(s)", "A sorting method", "A loop"], "a": "Data and link(s)"},
        {"q": "Which structure is best suited for priority-based removal?", "o": ["Queue", "Priority queue", "Simple stack", "String"], "a": "Priority queue"},
        {"q": "What is the worst-case time complexity of bubble sort?", "o": ["O(1)", "O(log n)", "O(n)", "O(n²)"], "a": "O(n²)"},
        {"q": "Which traversal visits the root between left and right subtrees?", "o": ["Preorder", "Inorder", "Postorder", "Level order"], "a": "Inorder"},
        {"q": "Which graph traversal explores neighbors level by level?", "o": ["DFS", "BFS", "Binary search", "Insertion sort"], "a": "BFS"},
        {"q": "What does an algorithm describe?", "o": ["A hardware device", "Steps to solve a problem", "A database only", "A programming language"], "a": "Steps to solve a problem"},
        {"q": "Which structure can efficiently support access by index?", "o": ["Array", "Linked list", "Tree only", "Graph only"], "a": "Array"},
        {"q": "What is a cycle in a graph?", "o": ["A path returning to its starting vertex", "A sorted array", "A stack operation", "A tree leaf"], "a": "A path returning to its starting vertex"},
        {"q": "Which technique solves a problem by breaking it into smaller subproblems?", "o": ["Compilation", "Divide and conquer", "Casting", "Hashing only"], "a": "Divide and conquer"},
        {"q": "What does O(1) time complexity mean?", "o": ["Constant time", "Linear time", "Quadratic time", "Exponential time"], "a": "Constant time"}
    ],

    "DBMS": [
        {"q": "What does DBMS stand for?", "o": ["Data Backup Management Software", "Database Management System", "Digital Base Mapping System", "Database Memory Service"], "a": "Database Management System"},
        {"q": "Which language is commonly used to query relational databases?", "o": ["HTML", "SQL", "CSS", "XML only"], "a": "SQL"},
        {"q": "What uniquely identifies each row in a table?", "o": ["Foreign key", "Primary key", "Duplicate key", "Null key"], "a": "Primary key"},
        {"q": "What does a foreign key do?", "o": ["Encrypts every row", "Links related tables", "Sorts all records", "Deletes duplicates automatically"], "a": "Links related tables"},
        {"q": "Which SQL command retrieves data?", "o": ["SELECT", "UPDATE", "DROP", "INSERT"], "a": "SELECT"},
        {"q": "Which SQL command adds new rows?", "o": ["ALTER", "INSERT", "SELECT", "GRANT"], "a": "INSERT"},
        {"q": "Which SQL command modifies existing rows?", "o": ["UPDATE", "CREATE", "SELECT", "COMMIT only"], "a": "UPDATE"},
        {"q": "Which clause filters rows in a query?", "o": ["ORDER BY", "WHERE", "GROUP BY", "FROM only"], "a": "WHERE"},
        {"q": "Which clause sorts query results?", "o": ["SORT", "ORDER BY", "ARRANGE", "FILTER"], "a": "ORDER BY"},
        {"q": "What is normalization intended to reduce?", "o": ["Data redundancy", "Data accuracy", "Table names", "All relationships"], "a": "Data redundancy"},
        {"q": "What does SQL JOIN do?", "o": ["Combines related rows from tables", "Deletes a database", "Creates a password", "Sorts a single column only"], "a": "Combines related rows from tables"},
        {"q": "Which constraint prevents duplicate values in a column?", "o": ["UNIQUE", "DEFAULT", "CHECK only", "NULL"], "a": "UNIQUE"},
        {"q": "What does NULL generally represent in a database?", "o": ["Zero only", "Unknown or missing value", "An empty table", "False in every case"], "a": "Unknown or missing value"},
        {"q": "Which ACID property ensures a transaction is all-or-nothing?", "o": ["Consistency", "Isolation", "Atomicity", "Durability"], "a": "Atomicity"},
        {"q": "Which ACID property helps preserve valid database rules?", "o": ["Consistency", "Isolation", "Atomicity", "Duplication"], "a": "Consistency"},
        {"q": "Which command removes rows matching a condition?", "o": ["DELETE", "SELECT", "CREATE", "GRANT"], "a": "DELETE"},
        {"q": "What is an index mainly used for?", "o": ["Speeding up data retrieval", "Replacing all tables", "Encrypting passwords automatically", "Removing all constraints"], "a": "Speeding up data retrieval"},
        {"q": "Which SQL function counts rows?", "o": ["SUM()", "COUNT()", "ROUND()", "JOIN()"], "a": "COUNT()"},
        {"q": "What is a relational database organized around?", "o": ["Tables and relationships", "Only audio files", "Only tree nodes", "Web page styles"], "a": "Tables and relationships"},
        {"q": "Which command saves a transaction's changes?", "o": ["ROLLBACK", "COMMIT", "DELETE", "REVOKE"], "a": "COMMIT"}
    ],

    "Python": [
        {"q": "Which keyword defines a function in Python?", "o": ["function", "def", "define", "fun"], "a": "def"},
        {"q": "Which data type stores True or False?", "o": ["int", "str", "bool", "list"], "a": "bool"},
        {"q": "Which symbol starts a single-line comment?", "o": ["//", "#", "/*", "--"], "a": "#"},
        {"q": "Which collection is ordered and mutable?", "o": ["tuple", "list", "frozenset", "string"], "a": "list"},
        {"q": "Which brackets create a tuple literal?", "o": ["{}", "[]", "()", "<>"], "a": "()"},
        {"q": "Which keyword starts a conditional branch?", "o": ["if", "for", "def", "import"], "a": "if"},
        {"q": "Which loop iterates over items in a sequence?", "o": ["for", "class", "try", "with"], "a": "for"},
        {"q": "What does len([1, 2, 3]) return?", "o": ["2", "3", "4", "6"], "a": "3"},
        {"q": "Which method adds an item to the end of a list?", "o": ["add()", "append()", "push_end()", "insert_end()"], "a": "append()"},
        {"q": "Which keyword returns a value from a function?", "o": ["yield only", "return", "break", "pass"], "a": "return"},
        {"q": "What is the result of 5 // 2?", "o": ["2.5", "2", "3", "1"], "a": "2"},
        {"q": "Which built-in function converts a value to an integer when possible?", "o": ["str()", "int()", "list()", "boolstr()"], "a": "int()"},
        {"q": "Which keyword handles an exception?", "o": ["catch", "except", "error", "rescue"], "a": "except"},
        {"q": "What does range(3) generate?", "o": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3 only"], "a": "0, 1, 2"},
        {"q": "Which operator checks equality?", "o": ["=", "==", "!=", ":="], "a": "=="},
        {"q": "Which collection stores unique values?", "o": ["list", "tuple", "set", "string"], "a": "set"},
        {"q": "How do you access the first item of a list named items?", "o": ["items[1]", "items[0]", "items.first", "items(-1)"], "a": "items[0]"},
        {"q": "Which keyword imports a module?", "o": ["include", "import", "using", "require"], "a": "import"},
        {"q": "What does input() return by default?", "o": ["Integer", "String", "Boolean", "List"], "a": "String"},
        {"q": "Which value represents the absence of a value in Python?", "o": ["undefined", "None", "empty", "void"], "a": "None"}
    ],

    "System Design": [
        {"q": "What is scalability?", "o": ["Ability to handle increased workload", "Deleting old data", "Writing fewer comments", "Changing a font"], "a": "Ability to handle increased workload"},
        {"q": "What does a load balancer do?", "o": ["Distributes incoming requests", "Stores passwords only", "Writes database queries", "Compresses every image"], "a": "Distributes incoming requests"},
        {"q": "What is caching?", "o": ["Keeping frequently used data for faster access", "Deleting all backups", "Increasing network distance", "Replacing authentication"], "a": "Keeping frequently used data for faster access"},
        {"q": "What is a database replica?", "o": ["A copy of database data", "A CSS file", "A login form", "A network cable"], "a": "A copy of database data"},
        {"q": "What does high availability aim to provide?", "o": ["Minimal service downtime", "More manual steps", "A larger logo", "Fewer users"], "a": "Minimal service downtime"},
        {"q": "What is a bottleneck?", "o": ["A component limiting overall performance", "A backup copy", "A user profile", "A type of password"], "a": "A component limiting overall performance"},
        {"q": "What is horizontal scaling?", "o": ["Adding more machines or instances", "Adding RAM to one machine only", "Reducing all users", "Changing screen size"], "a": "Adding more machines or instances"},
        {"q": "What is vertical scaling?", "o": ["Adding resources to one machine", "Adding more separate servers", "Removing the database", "Splitting a logo"], "a": "Adding resources to one machine"},
        {"q": "What is an API?", "o": ["An interface for software systems to communicate", "A type of monitor", "A database row", "A sorting algorithm"], "a": "An interface for software systems to communicate"},
        {"q": "What is a microservices architecture?", "o": ["An application split into smaller services", "One giant source file only", "A database without tables", "A network with no servers"], "a": "An application split into smaller services"},
        {"q": "Why use a message queue?", "o": ["To communicate asynchronously between components", "To style web pages", "To replace every API", "To increase image size"], "a": "To communicate asynchronously between components"},
        {"q": "What does fault tolerance mean?", "o": ["The system can continue despite certain failures", "The system never needs testing", "The database has no data", "Every request is rejected"], "a": "The system can continue despite certain failures"},
        {"q": "What is a CDN commonly used for?", "o": ["Delivering content from distributed locations", "Compiling Python", "Creating database keys", "Managing keyboard input"], "a": "Delivering content from distributed locations"},
        {"q": "What does latency measure?", "o": ["Delay before a response", "Number of employees", "File name length", "Database table count"], "a": "Delay before a response"},
        {"q": "What does throughput measure?", "o": ["Work completed per unit of time", "Color contrast", "Password length", "Server height"], "a": "Work completed per unit of time"},
        {"q": "Why is rate limiting used?", "o": ["To restrict request frequency", "To make passwords public", "To remove all caching", "To disable monitoring"], "a": "To restrict request frequency"},
        {"q": "What is a single point of failure?", "o": ["One component whose failure can disrupt the system", "A duplicated backup", "A successful test", "A design pattern for colors"], "a": "One component whose failure can disrupt the system"},
        {"q": "What is sharding?", "o": ["Splitting data across multiple partitions or servers", "Combining every password", "Compressing source code", "Removing all indexes"], "a": "Splitting data across multiple partitions or servers"},
        {"q": "Why are logs useful?", "o": ["Troubleshooting and understanding system events", "Replacing all tests", "Increasing latency", "Removing user requests"], "a": "Troubleshooting and understanding system events"},
        {"q": "What is a health check used for?", "o": ["Checking whether a service is operating", "Changing database names", "Formatting a document", "Sorting an array"], "a": "Checking whether a service is operating"}
    ],

     "Java": [
        {"q": "Which keyword declares a class in Java?", "o": ["define", "class", "struct", "object"], "a": "class"},
        {"q": "Which method is the usual Java application entry point?", "o": ["start()", "main()", "runApp()", "initMain()"], "a": "main()"},
        {"q": "Which type stores a whole number such as 10?", "o": ["int", "boolean", "char", "String"], "a": "int"},
        {"q": "Which keyword creates an object?", "o": ["make", "new", "create", "object"], "a": "new"},
        {"q": "Which keyword is used for inheritance between classes?", "o": ["inherits", "extends", "implements only", "superclass"], "a": "extends"},
        {"q": "Which keyword is used when a class implements an interface?", "o": ["extends", "implements", "interfaceOf", "inherits"], "a": "implements"},
        {"q": "Which type stores true or false?", "o": ["int", "boolean", "char", "double"], "a": "boolean"},
        {"q": "Which method compares the contents of many Java objects such as Strings?", "o": ["same()", "equals()", "compareOnly()", "is()"], "a": "equals()"},
        {"q": "Which collection does not allow duplicate elements?", "o": ["List", "Set", "ArrayList", "Queue"], "a": "Set"},
        {"q": "Which keyword prevents a class from being subclassed?", "o": ["static", "final", "private", "constant"], "a": "final"},
        {"q": "Which block is commonly used to handle exceptions?", "o": ["try-catch", "if-else only", "for-while", "switch-case only"], "a": "try-catch"},
        {"q": "Which keyword refers to the current object?", "o": ["self", "this", "current", "that"], "a": "this"},
        {"q": "Which keyword refers to a parent-class member or constructor?", "o": ["base", "parent", "super", "this"], "a": "super"},
        {"q": "Which Java type represents text?", "o": ["String", "char only", "text", "word"], "a": "String"},
        {"q": "Which loop executes at least once before checking its condition?", "o": ["for", "while", "do-while", "foreach only"], "a": "do-while"},
        {"q": "Which access modifier allows access from anywhere, subject to class accessibility?", "o": ["private", "public", "protected only", "hidden"], "a": "public"},
        {"q": "What is method overloading?", "o": ["Same method name with different parameter lists", "Deleting a method", "Changing a variable value", "Creating unrelated classes"], "a": "Same method name with different parameter lists"},
        {"q": "Which package contains the basic Scanner class?", "o": ["java.io", "java.util", "java.net", "java.sql"], "a": "java.util"},
        {"q": "What is the purpose of a constructor?", "o": ["Initialize a new object", "Delete a package", "Return a Boolean only", "Repeat a loop"], "a": "Initialize a new object"},
        {"q": "Which keyword declares a constant-like class variable?", "o": ["fixed", "final", "const", "immutable"], "a": "final"}
    ],

    "C++": [
        {"q": "Which symbol ends most C++ statements?", "o": [".", ";", ":", ","], "a": ";"},
        {"q": "Which header provides common input and output streams?", "o": ["<iostream>", "<stringonly>", "<input>", "<stdiofile>"], "a": "<iostream>"},
        {"q": "Which operator is commonly used with cout to send output?", "o": ["<<", ">>", "==", "&&"], "a": "<<"},
        {"q": "Which operator is commonly used with cin to receive input?", "o": [">>", "<<", "!=", "||"], "a": ">>"},
        {"q": "Which function is the usual program entry point?", "o": ["start()", "main()", "begin()", "run()"], "a": "main()"},
        {"q": "Which type stores a whole number?", "o": ["int", "bool", "char", "void"], "a": "int"},
        {"q": "Which keyword creates a class?", "o": ["object", "class", "define", "structclass"], "a": "class"},
        {"q": "Which symbol accesses a member through an object?", "o": [".", "::", "#", "@"], "a": "."},
        {"q": "Which operator accesses a member through a pointer?", "o": [".", "->", "::", "**"], "a": "->"},
        {"q": "Which concept lets one function name have different parameter lists?", "o": ["Overloading", "Encapsulation only", "Compilation", "Iteration"], "a": "Overloading"},
        {"q": "Which keyword allocates dynamic memory for an object or array?", "o": ["malloc only", "new", "create", "alloc"], "a": "new"},
        {"q": "Which keyword releases memory allocated with new for a single object?", "o": ["free", "remove", "delete", "clear"], "a": "delete"},
        {"q": "Which loop checks its condition before each iteration?", "o": ["while", "do-while", "Both always execute once", "Neither"], "a": "while"},
        {"q": "Which access specifier hides class members from ordinary outside access?", "o": ["public", "private", "open", "global"], "a": "private"},
        {"q": "Which feature allows a derived class to reuse a base class?", "o": ["Inheritance", "Compilation", "Iteration", "Casting"], "a": "Inheritance"},
        {"q": "What is a pointer?", "o": ["A variable that stores an address", "A loop counter only", "A class constructor", "A text string"], "a": "A variable that stores an address"},
        {"q": "Which operator gets the address of a variable?", "o": ["*", "&", "->", "%"], "a": "&"},
        {"q": "Which standard container stores elements in a resizable sequence?", "o": ["std::vector", "std::cout", "std::cin", "std::endl"], "a": "std::vector"},
        {"q": "Which keyword declares a value that should not be modified through that name?", "o": ["fixed", "const", "static only", "final"], "a": "const"},
        {"q": "What is a constructor called for?", "o": ["Initializing an object", "Ending every loop", "Printing output only", "Importing a header"], "a": "Initializing an object"}
    ]
}


def reset_to_dashboard():
    st.session_state.screen = "dashboard"
    st.session_state.selected_quiz = None
    st.session_state.quiz_submitted = False
    st.session_state.last_result = None


# ---------- REGISTRATION AND LOGIN ----------
if st.session_state.current_user is None:
    show_brand()
    def show_footer():
     st.markdown(
        """
        <div style="text-align:center; padding:20px; color:#64748b;">
            © 2026 Knowbit | Learn Smarter
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">YOUR LEARNING SPACE</div>
        <h1>Welcome to Knowbit.</h1>
        <p>Create an account to get started, or log in if you already
        have a Knowbit account.</p>
    </div>
    """, unsafe_allow_html=True)

    registered_users = load_registered_users()

    if st.session_state.auth_view == "register":
        st.subheader("Create your Knowbit account")
        with st.form("register_form"):
            full_name = st.text_input("Full name")
            new_username = st.text_input("Choose a username")
            email = st.text_input("Email address")
            new_password = st.text_input("Create a password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            register_clicked = st.form_submit_button("Create account")

        if register_clicked:
            full_name = full_name.strip()
            username = new_username.strip()
            email = email.strip()

            if not full_name or not username or not email or not new_password:
                st.error("Please complete all fields.")
            elif "|" in full_name or "|" in username or "|" in email:
                st.error("Please do not use the | character in your details.")
            elif len(username) < 3:
                st.error("Username must contain at least 3 characters.")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email address.")
            elif len(new_password) < 8:
                st.error("Password must contain at least 8 characters.")
            elif new_password != confirm_password:
                st.error("The passwords do not match.")
            elif username in registered_users:
                st.error("That username already exists. Please log in.")
            else:
                save_registration(full_name, username, email)
                save_login(username, new_password)
                st.session_state.auth_view = "login"
                st.success("Registration successful! Please log in.")
                st.rerun()

        st.write("Already registered?")
        if st.button("Go to Login", key="go_login"):
            st.session_state.auth_view = "login"
            st.rerun()

    else:
        st.subheader("Welcome back")
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            login_clicked = st.form_submit_button("Login")

        if login_clicked:
            username = login_username.strip()
            if verify_login(username, login_password):
                st.session_state.current_user = username
                st.session_state.screen = "dashboard"
                st.session_state.selected_quiz = None
                st.session_state.quiz_submitted = False
                st.rerun()
            else:
                st.error("Incorrect username or password. Please try again.")

        st.write("New to Knowbit?")
        if st.button("Create an account", key="go_register"):
            st.session_state.auth_view = "register"
            st.rerun()

    show_footer()
    st.stop()

    # ---------- LOGOUT AND USER HEADER ----------
user = st.session_state.current_user
registered_users = load_registered_users()
user_details = registered_users.get(user, {})
header_col, logout_col = st.columns([5, 1])

with header_col:
    display_name = user_details.get("full_name", user)
    st.caption(f"Welcome, **{display_name}**")

with logout_col:
    if st.button("Log out", key="logout_button"):
        st.session_state.current_user = None
        st.session_state.auth_view = "login"
        st.session_state.screen = "auth"
        st.session_state.selected_quiz = None
        st.session_state.quiz_submitted = False
        st.session_state.last_result = None
        st.rerun()
# ---------- SHARED HEADER ----------
show_brand()
st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR LEARNING SPACE</div>
    <h1>Learn smarter.<br>Build confidence.</h1>
    <p>Practice technical concepts, test your knowledge,
    and track your progress — one question at a time.</p>
</div>
""", unsafe_allow_html=True)


descriptions = {
    "DSA": "Explore data structures, searching, sorting, and algorithms.",
    "DBMS": "Practice SQL, database keys, queries, and normalization.",
    "Python": "Test Python syntax, data types, functions, and loops.",
    "System Design": "Explore scalability, caching, and system architecture.",
    "Java": "Practice Java syntax, classes, inheritance, and exceptions.",
    "C++": "Explore C++ fundamentals, pointers, classes, and STL."
}

subjects = [
    ("DSA", "Data Structures & Algorithms", "CATEGORY 01"),
    ("DBMS", "Database Management", "CATEGORY 02"),
    ("Python", "Python Programming", "CATEGORY 03"),
    ("System Design", "System Design", "CATEGORY 04"),
    ("Java", "Java Programming", "CATEGORY 05"),
    ("C++", "C++ Programming", "CATEGORY 06")
]

# ---------- DASHBOARD SCREEN ----------
if st.session_state.screen == "dashboard":
    st.markdown(
        '<div class="section-title">Explore categories</div>'
        '<div class="section-subtitle">Choose a subject and get ready to challenge yourself.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    for index, (subject, title, category) in enumerate(subjects):
        column = col1 if index % 2 == 0 else col2
        with column:
            st.markdown(
                f"""
                <div class="quiz-card">
                    <div class="quiz-number">{category}</div>
                    <h3>{title}</h3>
                    <p>{descriptions[subject]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Start {subject} quiz", key=f"start_{subject}"):
                st.session_state.selected_quiz = subject
                st.session_state.quiz_submitted = False
                st.session_state.screen = "quiz"
                st.rerun()

    # Personal progress summary
    st.divider()
    st.subheader("Your learning progress")
    history = load_user_results(user)

    if history:
        total_attempts = len(history)
        average_accuracy = sum(item["accuracy"] for item in history) / total_attempts
        best_attempt = max(history, key=lambda item: item["accuracy"])
        m1, m2, m3 = st.columns(3)
        m1.metric("Quiz attempts", total_attempts)
        m2.metric("Average accuracy", f"{average_accuracy:.1f}%")
        m3.metric("Best subject", best_attempt["subject"])

        st.markdown("### Recent attempts")
        for item in reversed(history[-10:]):
            st.write(
                f"**{item['subject']}** — {item['score']}/{item['total']} "
                f"({item['accuracy']:.1f}%) · {item['date']}"
            )
    else:
        st.info("Your quiz progress will appear here after your first attempt.")

# ---------- QUIZ SCREEN ----------
elif st.session_state.screen == "quiz":
    selected = st.session_state.selected_quiz

    if selected not in quiz_data:
        st.session_state.screen = "dashboard"
        st.rerun()

    back_col, title_col = st.columns([1, 5])
    with back_col:
        if st.button("← Subjects", key="quiz_back"):
            reset_to_dashboard()
            st.rerun()
    with title_col:
        st.subheader(f"{selected} Quiz")

    st.write("20 questions · 1 point per correct answer")
    questions = quiz_data[selected]

    with st.form(key=f"form_{selected}"):
        user_answers = []
        for i, question in enumerate(questions):
            st.markdown(f"**Question {i + 1}. {question['q']}**")
            answer = st.radio(
                "Choose your answer:",
                question["o"],
                index=None,
                key=f"{selected}_answer_{i}",
                label_visibility="collapsed"
            )
            user_answers.append(answer)

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        score = sum(
            1 for question, answer in zip(questions, user_answers)
            if answer == question["a"]
        )
        total = len(questions)
        accuracy = (score / total) * 100 if total else 0

        save_quiz_result(user, selected, score, total, accuracy)

        st.session_state.last_result = {
            "subject": selected,
            "score": score,
            "total": total,
            "accuracy": accuracy,
            "answers": user_answers.copy()
        }
        st.session_state.quiz_submitted = True
        st.session_state.screen = "result"
        st.rerun()

# ---------- RESULT SCREEN ----------
elif st.session_state.screen == "result":
    result = st.session_state.last_result

    if not result:
        st.session_state.screen = "dashboard"
        st.rerun()

    st.subheader(f"{result['subject']} — Your Results")
    m1, m2 = st.columns(2)
    m1.metric("Your Score", f"{result['score']} / {result['total']}")
    m2.metric("Accuracy", f"{result['accuracy']:.1f}%")

    if result["score"] >= 16:
        st.success("Excellent work! You have a strong understanding of this subject.")
    elif result["score"] >= 10:
        st.info("Good effort! Review the explanations and keep practising.")
    else:
        st.warning("Keep learning! Review the correct answers and try again.")

    st.markdown("### Answer Review")
    questions = quiz_data[result["subject"]]

    for i, question in enumerate(questions):
        your_answer = result["answers"][i]
        correct_answer = question["a"]
        st.markdown(f"**Q{i + 1}. {question['q']}**")

        if your_answer == correct_answer:
            st.success(f"Your answer: {your_answer} — Correct!")
        else:
            st.error(f"Your answer: {your_answer or 'Not answered'}")
            st.write(f"Correct answer: **{correct_answer}**")

    action_col1, action_col2 = st.columns(2)
    with action_col1:
        if st.button("Try This Quiz Again", key="retry_quiz"):
            selected = result["subject"]
            for i in range(len(quiz_data[selected])):
                answer_key = f"{selected}_answer_{i}"
                if answer_key in st.session_state:
                    del st.session_state[answer_key]
            st.session_state.last_result = None
            st.session_state.quiz_submitted = False
            st.session_state.screen = "quiz"
            st.rerun()

    with action_col2:
        if st.button("Back to Subjects", key="result_back"):
            reset_to_dashboard()
            st.rerun()


# ---------- BOTTOM SECTION ----------
st.markdown("""
<div class="info-strip">
    <strong>Small steps. Stronger skills.</strong><br>
    Build your technical knowledge through consistent practice.
</div>
""", unsafe_allow_html=True)
show_footer()

import streamlit as st
import hashlib

st.set_page_config(
    page_title="Knowbit | Learn Smarter",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<style>

/* Make quiz score and metric text dark */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div,
[data-testid="stMetricLabel"] {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* Keep score text readable throughout the results section */
[data-testid="stMetric"] {
    background-color: #EAF0FF !important;
    padding: 16px !important;
    border-radius: 12px !important;
}

/* Change yellow warning boxes to light blue */
.stAlert [data-testid="stAlertContainer"] {
    background-color: #EAF0FF !important;
    color: #243D8E !important;
}

.stAlert [data-testid="stAlertContent"],
.stAlert [data-testid="stAlertContent"] p {
    color: #243D8E !important;
}

/* Fix quiz answer options */
.stRadio label,
.stRadio label p,
.stRadio [data-testid="stMarkdownContainer"] p {
    color: #172033 !important;
}

.stRadio [role="radiogroup"] label {
    background-color: #FFFFFF !important;
    border: 1px solid #D1D9E8 !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    margin-bottom: 8px !important;
}

.stRadio [role="radiogroup"] label span {
    color: #172033 !important;
}

.stRadio [role="radiogroup"] label p {
    color: #172033 !important;
}

.stRadio [role="radiogroup"] label:hover {
    border-color: #2563EB !important;
}
/* Fix dark input boxes on the light Knowbit design */
.stApp,
[data-testid="stAppViewContainer"] {
    background-color: #F5F7FB !important;
    color: #172033 !important;
}

.stTextInput input,
.stTextInput input:focus {
    background-color: #FFFFFF !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    border: 1px solid #D1D9E8 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

.stTextInput label {
    color: #172033 !important;
}

.stTextInput input::placeholder {
    color: #68738A !important;
    opacity: 1 !important;
}

.stTabs [data-baseweb="tab"] {
    color: #172033 !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #2563EB !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #2563EB !important;
}

.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.stButton > button,
.stFormSubmitButton > button {
    background-color: #2563EB !important;
    color: white !important;
    border: 2px solid #2563EB !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #1D4ED8 !important;
    border-color: #1D4ED8 !important;
}

.brand {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #2448C5;
}

.brand span {
    color: #172033;
}

.hero {
    background: linear-gradient(120deg, #101B3C, #2448C5);
    padding: 46px 42px;
    border-radius: 22px;
    color: white;
    margin-top: 22px;
    margin-bottom: 32px;
}

.eyebrow {
    color: #C5D2FF;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
}

.hero h1 {
    color: white;
    font-size: 42px;
    line-height: 1.2;
    margin: 14px 0;
}

.hero p {
    color: #E0E7FF;
    font-size: 16px;
    max-width: 580px;
    line-height: 1.7;
}

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #172033;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #68738A;
    margin-bottom: 22px;
}

.quiz-card {
    background: white;
    border: 1px solid #E3E8F2;
    border-radius: 16px;
    padding: 25px 23px;
    min-height: 185px;
    margin-bottom: 18px;
    box-shadow: 0 5px 18px rgba(23, 32, 51, 0.035);
}

.quiz-number {
    color: #3155C8;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}

.quiz-card h3 {
    color: #172033;
    font-size: 21px;
    margin-top: 14px;
    margin-bottom: 8px;
}

.quiz-card p {
    color: #68738A;
    font-size: 14px;
    line-height: 1.6;
}

.info-strip {
    background: #EAF0FF;
    border: 1px solid #D9E3FF;
    padding: 18px 22px;
    border-radius: 13px;
    color: #243D8E;
    margin-top: 8px;
    margin-bottom: 30px;
}

.footer-note {
    color: #7B8498;
    text-align: center;
    font-size: 12px;
    padding-top: 28px;
}
</style>
""", unsafe_allow_html=True)


# ---------- QUIZ QUESTIONS ----------
# Six subjects with 20 questions each.

quiz_data = {
    "DSA": [
        {"q": "Which data structure follows FIFO?", "o": ["Stack", "Queue", "Tree", "Graph"], "a": "Queue"},
        {"q": "Which data structure follows LIFO?", "o": ["Queue", "Stack", "Linked list", "Graph"], "a": "Stack"},
        {"q": "Which data structure stores key-value pairs?", "o": ["Stack", "Queue", "Hash table", "Tree only"], "a": "Hash table"},
        {"q": "What is the worst-case time complexity of linear search?", "o": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "a": "O(n)"},
        {"q": "Binary search requires which condition?", "o": ["Random data", "Sorted data", "A graph", "A stack"], "a": "Sorted data"},
        {"q": "Which structure is commonly used for BFS?", "o": ["Stack", "Queue", "Heap", "Array only"], "a": "Queue"},
        {"q": "Which structure is commonly used for DFS?", "o": ["Queue", "Stack", "Hash table", "Priority queue only"], "a": "Stack"},
        {"q": "Which sorting algorithm repeatedly selects the minimum element?", "o": ["Merge sort", "Selection sort", "Quick sort", "Heap sort"], "a": "Selection sort"},
        {"q": "What is the average time complexity of merge sort?", "o": ["O(n)", "O(log n)", "O(n log n)", "O(n²)"], "a": "O(n log n)"},
        {"q": "Which data structure represents hierarchical relationships?", "o": ["Queue", "Tree", "Stack", "Array"], "a": "Tree"},
        {"q": "What is a node in a linked list?", "o": ["Only an index", "Data and link(s)", "A sorting method", "A loop"], "a": "Data and link(s)"},
        {"q": "Which structure is best suited for priority-based removal?", "o": ["Queue", "Priority queue", "Simple stack", "String"], "a": "Priority queue"},
        {"q": "What is the worst-case time complexity of bubble sort?", "o": ["O(1)", "O(log n)", "O(n)", "O(n²)"], "a": "O(n²)"},
        {"q": "Which traversal visits the root between left and right subtrees?", "o": ["Preorder", "Inorder", "Postorder", "Level order"], "a": "Inorder"},
        {"q": "Which graph traversal explores neighbors level by level?", "o": ["DFS", "BFS", "Binary search", "Insertion sort"], "a": "BFS"},
        {"q": "What does an algorithm describe?", "o": ["A hardware device", "Steps to solve a problem", "A database only", "A programming language"], "a": "Steps to solve a problem"},
        {"q": "Which structure can efficiently support access by index?", "o": ["Array", "Linked list", "Tree only", "Graph only"], "a": "Array"},
        {"q": "What is a cycle in a graph?", "o": ["A path returning to its starting vertex", "A sorted array", "A stack operation", "A tree leaf"], "a": "A path returning to its starting vertex"},
        {"q": "Which technique solves a problem by breaking it into smaller subproblems?", "o": ["Compilation", "Divide and conquer", "Casting", "Hashing only"], "a": "Divide and conquer"},
        {"q": "What does O(1) time complexity mean?", "o": ["Constant time", "Linear time", "Quadratic time", "Exponential time"], "a": "Constant time"}
    ],

    "DBMS": [
        {"q": "What does DBMS stand for?", "o": ["Data Backup Management Software", "Database Management System", "Digital Base Mapping System", "Database Memory Service"], "a": "Database Management System"},
        {"q": "Which language is commonly used to query relational databases?", "o": ["HTML", "SQL", "CSS", "XML only"], "a": "SQL"},
        {"q": "What uniquely identifies each row in a table?", "o": ["Foreign key", "Primary key", "Duplicate key", "Null key"], "a": "Primary key"},
        {"q": "What does a foreign key do?", "o": ["Encrypts every row", "Links related tables", "Sorts all records", "Deletes duplicates automatically"], "a": "Links related tables"},
        {"q": "Which SQL command retrieves data?", "o": ["SELECT", "UPDATE", "DROP", "INSERT"], "a": "SELECT"},
        {"q": "Which SQL command adds new rows?", "o": ["ALTER", "INSERT", "SELECT", "GRANT"], "a": "INSERT"},
        {"q": "Which SQL command modifies existing rows?", "o": ["UPDATE", "CREATE", "SELECT", "COMMIT only"], "a": "UPDATE"},
        {"q": "Which clause filters rows in a query?", "o": ["ORDER BY", "WHERE", "GROUP BY", "FROM only"], "a": "WHERE"},
        {"q": "Which clause sorts query results?", "o": ["SORT", "ORDER BY", "ARRANGE", "FILTER"], "a": "ORDER BY"},
        {"q": "What is normalization intended to reduce?", "o": ["Data redundancy", "Data accuracy", "Table names", "All relationships"], "a": "Data redundancy"},
        {"q": "What does SQL JOIN do?", "o": ["Combines related rows from tables", "Deletes a database", "Creates a password", "Sorts a single column only"], "a": "Combines related rows from tables"},
        {"q": "Which constraint prevents duplicate values in a column?", "o": ["UNIQUE", "DEFAULT", "CHECK only", "NULL"], "a": "UNIQUE"},
        {"q": "What does NULL generally represent in a database?", "o": ["Zero only", "Unknown or missing value", "An empty table", "False in every case"], "a": "Unknown or missing value"},
        {"q": "Which ACID property ensures a transaction is all-or-nothing?", "o": ["Consistency", "Isolation", "Atomicity", "Durability"], "a": "Atomicity"},
        {"q": "Which ACID property helps preserve valid database rules?", "o": ["Consistency", "Isolation", "Atomicity", "Duplication"], "a": "Consistency"},
        {"q": "Which command removes rows matching a condition?", "o": ["DELETE", "SELECT", "CREATE", "GRANT"], "a": "DELETE"},
        {"q": "What is an index mainly used for?", "o": ["Speeding up data retrieval", "Replacing all tables", "Encrypting passwords automatically", "Removing all constraints"], "a": "Speeding up data retrieval"},
        {"q": "Which SQL function counts rows?", "o": ["SUM()", "COUNT()", "ROUND()", "JOIN()"], "a": "COUNT()"},
        {"q": "What is a relational database organized around?", "o": ["Tables and relationships", "Only audio files", "Only tree nodes", "Web page styles"], "a": "Tables and relationships"},
        {"q": "Which command saves a transaction's changes?", "o": ["ROLLBACK", "COMMIT", "DELETE", "REVOKE"], "a": "COMMIT"}
    ],

    "Python": [
        {"q": "Which keyword defines a function in Python?", "o": ["function", "def", "define", "fun"], "a": "def"},
        {"q": "Which data type stores True or False?", "o": ["int", "str", "bool", "list"], "a": "bool"},
        {"q": "Which symbol starts a single-line comment?", "o": ["//", "#", "/*", "--"], "a": "#"},
        {"q": "Which collection is ordered and mutable?", "o": ["tuple", "list", "frozenset", "string"], "a": "list"},
        {"q": "Which brackets create a tuple literal?", "o": ["{}", "[]", "()", "<>"], "a": "()"},
        {"q": "Which keyword starts a conditional branch?", "o": ["if", "for", "def", "import"], "a": "if"},
        {"q": "Which loop iterates over items in a sequence?", "o": ["for", "class", "try", "with"], "a": "for"},
        {"q": "What does len([1, 2, 3]) return?", "o": ["2", "3", "4", "6"], "a": "3"},
        {"q": "Which method adds an item to the end of a list?", "o": ["add()", "append()", "push_end()", "insert_end()"], "a": "append()"},
        {"q": "Which keyword returns a value from a function?", "o": ["yield only", "return", "break", "pass"], "a": "return"},
        {"q": "What is the result of 5 // 2?", "o": ["2.5", "2", "3", "1"], "a": "2"},
        {"q": "Which built-in function converts a value to an integer when possible?", "o": ["str()", "int()", "list()", "boolstr()"], "a": "int()"},
        {"q": "Which keyword handles an exception?", "o": ["catch", "except", "error", "rescue"], "a": "except"},
        {"q": "What does range(3) generate?", "o": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3 only"], "a": "0, 1, 2"},
        {"q": "Which operator checks equality?", "o": ["=", "==", "!=", ":="], "a": "=="},
        {"q": "Which collection stores unique values?", "o": ["list", "tuple", "set", "string"], "a": "set"},
        {"q": "How do you access the first item of a list named items?", "o": ["items[1]", "items[0]", "items.first", "items(-1)"], "a": "items[0]"},
        {"q": "Which keyword imports a module?", "o": ["include", "import", "using", "require"], "a": "import"},
        {"q": "What does input() return by default?", "o": ["Integer", "String", "Boolean", "List"], "a": "String"},
        {"q": "Which value represents the absence of a value in Python?", "o": ["undefined", "None", "empty", "void"], "a": "None"}
    ],

    "System Design": [
        {"q": "What is scalability?", "o": ["Ability to handle increased workload", "Deleting old data", "Writing fewer comments", "Changing a font"], "a": "Ability to handle increased workload"},
        {"q": "What does a load balancer do?", "o": ["Distributes incoming requests", "Stores passwords only", "Writes database queries", "Compresses every image"], "a": "Distributes incoming requests"},
        {"q": "What is caching?", "o": ["Keeping frequently used data for faster access", "Deleting all backups", "Increasing network distance", "Replacing authentication"], "a": "Keeping frequently used data for faster access"},
        {"q": "What is a database replica?", "o": ["A copy of database data", "A CSS file", "A login form", "A network cable"], "a": "A copy of database data"},
        {"q": "What does high availability aim to provide?", "o": ["Minimal service downtime", "More manual steps", "A larger logo", "Fewer users"], "a": "Minimal service downtime"},
        {"q": "What is a bottleneck?", "o": ["A component limiting overall performance", "A backup copy", "A user profile", "A type of password"], "a": "A component limiting overall performance"},
        {"q": "What is horizontal scaling?", "o": ["Adding more machines or instances", "Adding RAM to one machine only", "Reducing all users", "Changing screen size"], "a": "Adding more machines or instances"},
        {"q": "What is vertical scaling?", "o": ["Adding resources to one machine", "Adding more separate servers", "Removing the database", "Splitting a logo"], "a": "Adding resources to one machine"},
        {"q": "What is an API?", "o": ["An interface for software systems to communicate", "A type of monitor", "A database row", "A sorting algorithm"], "a": "An interface for software systems to communicate"},
        {"q": "What is a microservices architecture?", "o": ["An application split into smaller services", "One giant source file only", "A database without tables", "A network with no servers"], "a": "An application split into smaller services"},
        {"q": "Why use a message queue?", "o": ["To communicate asynchronously between components", "To style web pages", "To replace every API", "To increase image size"], "a": "To communicate asynchronously between components"},
        {"q": "What does fault tolerance mean?", "o": ["The system can continue despite certain failures", "The system never needs testing", "The database has no data", "Every request is rejected"], "a": "The system can continue despite certain failures"},
        {"q": "What is a CDN commonly used for?", "o": ["Delivering content from distributed locations", "Compiling Python", "Creating database keys", "Managing keyboard input"], "a": "Delivering content from distributed locations"},
        {"q": "What does latency measure?", "o": ["Delay before a response", "Number of employees", "File name length", "Database table count"], "a": "Delay before a response"},
        {"q": "What does throughput measure?", "o": ["Work completed per unit of time", "Color contrast", "Password length", "Server height"], "a": "Work completed per unit of time"},
        {"q": "Why is rate limiting used?", "o": ["To restrict request frequency", "To make passwords public", "To remove all caching", "To disable monitoring"], "a": "To restrict request frequency"},
        {"q": "What is a single point of failure?", "o": ["One component whose failure can disrupt the system", "A duplicated backup", "A successful test", "A design pattern for colors"], "a": "One component whose failure can disrupt the system"},
        {"q": "What is sharding?", "o": ["Splitting data across multiple partitions or servers", "Combining every password", "Compressing source code", "Removing all indexes"], "a": "Splitting data across multiple partitions or servers"},
        {"q": "Why are logs useful?", "o": ["Troubleshooting and understanding system events", "Replacing all tests", "Increasing latency", "Removing user requests"], "a": "Troubleshooting and understanding system events"},
        {"q": "What is a health check used for?", "o": ["Checking whether a service is operating", "Changing database names", "Formatting a document", "Sorting an array"], "a": "Checking whether a service is operating"}
    ],

    "Java": [
        {"q": "Which keyword declares a class in Java?", "o": ["define", "class", "struct", "object"], "a": "class"},
        {"q": "Which method is the usual Java application entry point?", "o": ["start()", "main()", "runApp()", "initMain()"], "a": "main()"},
        {"q": "Which type stores a whole number such as 10?", "o": ["int", "boolean", "char", "String"], "a": "int"},
        {"q": "Which keyword creates an object?", "o": ["make", "new", "create", "object"], "a": "new"},
        {"q": "Which keyword is used for inheritance between classes?", "o": ["inherits", "extends", "implements only", "superclass"], "a": "extends"},
        {"q": "Which keyword is used when a class implements an interface?", "o": ["extends", "implements", "interfaceOf", "inherits"], "a": "implements"},
        {"q": "Which type stores true or false?", "o": ["int", "boolean", "char", "double"], "a": "boolean"},
        {"q": "Which method compares the contents of many Java objects such as Strings?", "o": ["same()", "equals()", "compareOnly()", "is()"], "a": "equals()"},
        {"q": "Which collection does not allow duplicate elements?", "o": ["List", "Set", "ArrayList", "Queue"], "a": "Set"},
        {"q": "Which keyword prevents a class from being subclassed?", "o": ["static", "final", "private", "constant"], "a": "final"},
        {"q": "Which block is commonly used to handle exceptions?", "o": ["try-catch", "if-else only", "for-while", "switch-case only"], "a": "try-catch"},
        {"q": "Which keyword refers to the current object?", "o": ["self", "this", "current", "that"], "a": "this"},
        {"q": "Which keyword refers to a parent-class member or constructor?", "o": ["base", "parent", "super", "this"], "a": "super"},
        {"q": "Which Java type represents text?", "o": ["String", "char only", "text", "word"], "a": "String"},
        {"q": "Which loop executes at least once before checking its condition?", "o": ["for", "while", "do-while", "foreach only"], "a": "do-while"},
        {"q": "Which access modifier allows access from anywhere, subject to class accessibility?", "o": ["private", "public", "protected only", "hidden"], "a": "public"},
        {"q": "What is method overloading?", "o": ["Same method name with different parameter lists", "Deleting a method", "Changing a variable value", "Creating unrelated classes"], "a": "Same method name with different parameter lists"},
        {"q": "Which package contains the basic Scanner class?", "o": ["java.io", "java.util", "java.net", "java.sql"], "a": "java.util"},
        {"q": "What is the purpose of a constructor?", "o": ["Initialize a new object", "Delete a package", "Return a Boolean only", "Repeat a loop"], "a": "Initialize a new object"},
        {"q": "Which keyword declares a constant-like class variable?", "o": ["fixed", "final", "const", "immutable"], "a": "final"}
    ],

    "C++": [
        {"q": "Which symbol ends most C++ statements?", "o": [".", ";", ":", ","], "a": ";"},
        {"q": "Which header provides common input and output streams?", "o": ["<iostream>", "<stringonly>", "<input>", "<stdiofile>"], "a": "<iostream>"},
        {"q": "Which operator is commonly used with cout to send output?", "o": ["<<", ">>", "==", "&&"], "a": "<<"},
        {"q": "Which operator is commonly used with cin to receive input?", "o": [">>", "<<", "!=", "||"], "a": ">>"},
        {"q": "Which function is the usual program entry point?", "o": ["start()", "main()", "begin()", "run()"], "a": "main()"},
        {"q": "Which type stores a whole number?", "o": ["int", "bool", "char", "void"], "a": "int"},
        {"q": "Which keyword creates a class?", "o": ["object", "class", "define", "structclass"], "a": "class"},
        {"q": "Which symbol accesses a member through an object?", "o": [".", "::", "#", "@"], "a": "."},
        {"q": "Which operator accesses a member through a pointer?", "o": [".", "->", "::", "**"], "a": "->"},
        {"q": "Which concept lets one function name have different parameter lists?", "o": ["Overloading", "Encapsulation only", "Compilation", "Iteration"], "a": "Overloading"},
        {"q": "Which keyword allocates dynamic memory for an object or array?", "o": ["malloc only", "new", "create", "alloc"], "a": "new"},
        {"q": "Which keyword releases memory allocated with new for a single object?", "o": ["free", "remove", "delete", "clear"], "a": "delete"},
        {"q": "Which loop checks its condition before each iteration?", "o": ["while", "do-while", "Both always execute once", "Neither"], "a": "while"},
        {"q": "Which access specifier hides class members from ordinary outside access?", "o": ["public", "private", "open", "global"], "a": "private"},
        {"q": "Which feature allows a derived class to reuse a base class?", "o": ["Inheritance", "Compilation", "Iteration", "Casting"], "a": "Inheritance"},
        {"q": "What is a pointer?", "o": ["A variable that stores an address", "A loop counter only", "A class constructor", "A text string"], "a": "A variable that stores an address"},
        {"q": "Which operator gets the address of a variable?", "o": ["*", "&", "->", "%"], "a": "&"},
        {"q": "Which standard container stores elements in a resizable sequence?", "o": ["std::vector", "std::cout", "std::cin", "std::endl"], "a": "std::vector"},
        {"q": "Which keyword declares a value that should not be modified through that name?", "o": ["fixed", "const", "static only", "final"], "a": "const"},
        {"q": "What is a constructor called for?", "o": ["Initializing an object", "Ending every loop", "Printing output only", "Importing a header"], "a": "Initializing an object"}
    ]
}


# ---------- SESSION STATE ----------
if "selected_quiz" not in st.session_state:
    st.session_state.selected_quiz = None

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}


# ---------- REGISTRATION AND LOGIN ----------
if "users" not in st.session_state:
    st.session_state.users = {}

if "current_user" not in st.session_state:
    st.session_state.current_user = None


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


if st.session_state.current_user is None:

    st.markdown(
        '<div class="brand">know<span>bit</span></div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">YOUR LEARNING SPACE</div>
        <h1>Welcome to Knowbit.</h1>
        <p>Sign in or create an account to practise technical
        concepts and track your quiz scores.</p>
    </div>
    """, unsafe_allow_html=True)

    register_tab, login_tab = st.tabs(
    ["Register", "Login"]
)
    with login_tab:
        st.subheader("Welcome back")

        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input(
                "Password",
                type="password"
            )
            login_clicked = st.form_submit_button("Login")

        if login_clicked:
            username = login_username.strip()
            saved_hash = st.session_state.users.get(username)

            if (
                saved_hash is not None
                and saved_hash == hash_password(login_password)
            ):
                st.session_state.current_user = username
                st.session_state.selected_quiz = None
                st.session_state.quiz_submitted = False
                st.rerun()
            else:
                st.error(
                    "Incorrect username or password. Please try again."
                )

    with register_tab:
        st.subheader("Create your Knowbit account")

        with st.form("register_form"):
            new_username = st.text_input("Choose a username")
            new_password = st.text_input(
                "Create a password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )
            register_clicked = st.form_submit_button(
                "Create account"
            )

        if register_clicked:
            username = new_username.strip()

            if not username or not new_password:
                st.error("Please enter a username and password.")

            elif len(username) < 3:
                st.error("Username must contain at least 3 characters.")

            elif len(new_password) < 6:
                st.error("Password must contain at least 6 characters.")

            elif new_password != confirm_password:
                st.error("The passwords do not match.")

            elif username in st.session_state.users:
                st.error(
                    "That username already exists. Choose another."
                )

            else:
                st.session_state.users[username] = hash_password(
                    new_password
                )
                st.session_state.current_user = username
                st.session_state.selected_quiz = None
                st.session_state.quiz_submitted = False
                st.rerun()

    st.markdown(
        "<div class='footer-note'>"
        "KNOWBIT · LEARN. PRACTICE. IMPROVE."
        "</div>",
        unsafe_allow_html=True
    )

    st.stop()


# ---------- LOGOUT ----------
user_col, logout_col = st.columns([5, 1])

with user_col:
    st.caption(
        f"Logged in as **{st.session_state.current_user}**"
    )

with logout_col:
    if st.button("Log out", key="logout_button"):
        st.session_state.current_user = None
        st.session_state.selected_quiz = None
        st.session_state.quiz_submitted = False
        st.rerun()


# ---------- HEADER ----------
st.markdown("""
<div class="brand">know<span>bit</span></div>

<div class="hero">
    <div class="eyebrow">YOUR LEARNING SPACE</div>
    <h1>Learn smarter.<br>Build confidence.</h1>
    <p>
        Practice technical concepts, test your knowledge,
        and track your progress — one question at a time.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------- QUIZ CATEGORIES ----------
st.markdown(
    '<div class="section-title">Explore categories</div>'
    '<div class="section-subtitle">'
    'Choose a subject and get ready to challenge yourself.'
    '</div>',
    unsafe_allow_html=True
)

descriptions = {
    "DSA": "Explore data structures, searching, sorting, and algorithms.",
    "DBMS": "Practice SQL, database keys, queries, and normalization.",
    "Python": "Test Python syntax, data types, functions, and loops.",
    "System Design": "Explore scalability, caching, and system architecture.",
    "Java": "Practice Java syntax, classes, inheritance, and exceptions.",
    "C++": "Explore C++ fundamentals, pointers, classes, and STL."
}

subjects = [
    ("DSA", "Data Structures & Algorithms", "CATEGORY 01"),
    ("DBMS", "Database Management", "CATEGORY 02"),
    ("Python", "Python Programming", "CATEGORY 03"),
    ("System Design", "System Design", "CATEGORY 04"),
    ("Java", "Java Programming", "CATEGORY 05"),
    ("C++", "C++ Programming", "CATEGORY 06")
]

col1, col2 = st.columns(2)

for index, (subject, title, category) in enumerate(subjects):
    column = col1 if index % 2 == 0 else col2

    with column:
        st.markdown(
            f"""
            <div class="quiz-card">
                <div class="quiz-number">{category}</div>
                <h3>{title}</h3>
                <p>{descriptions[subject]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(f"Start {subject} quiz", key=f"start_{subject}"):
            st.session_state.selected_quiz = subject
            st.session_state.quiz_submitted = False
            st.rerun()


# ---------- QUIZ SECTION ----------
selected = st.session_state.selected_quiz

if selected:
    st.divider()
    st.subheader(f"{selected} Quiz")
    st.write("20 questions · 1 point per correct answer")

    questions = quiz_data[selected]

    with st.form(key=f"form_{selected}"):
        user_answers = []

        for i, question in enumerate(questions):
            st.markdown(f"**Question {i + 1}. {question['q']}**")

            answer = st.radio(
                "Choose your answer:",
                question["o"],
                index=None,
                key=f"{selected}_answer_{i}",
                label_visibility="collapsed"
            )

            user_answers.append(answer)

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        score = 0

        for question, answer in zip(questions, user_answers):
            if answer == question["a"]:
                score += 1

        st.session_state.quiz_scores[selected] = {
            "score": score,
            "answers": user_answers.copy()
        }

        st.session_state.quiz_submitted = True

    if (
        st.session_state.quiz_submitted
        and selected in st.session_state.quiz_scores
    ):
        result = st.session_state.quiz_scores[selected]
        score = result["score"]

        st.divider()
        st.subheader("Your Results")
        st.metric("Your Score", f"{score} / 20")

        if score >= 16:
            st.success(
                "Excellent work! You have a strong understanding of this subject."
            )
        elif score >= 10:
            st.info(
                "Good effort! Review the explanations and keep practising."
            )
        else:
            st.warning(
                "Keep learning! Review the correct answers and try again."
            )

        st.markdown("### Answer Review")

        for i, question in enumerate(questions):
            your_answer = result["answers"][i]
            correct_answer = question["a"]

            st.markdown(f"**Q{i + 1}. {question['q']}**")

            if your_answer == correct_answer:
                st.success(
                    f"Your answer: {your_answer} — Correct!"
                )
            else:
                st.error(
                    f"Your answer: {your_answer or 'Not answered'}"
                )
                st.write(
                    f"Correct answer: **{correct_answer}**"
                )

        if st.button(
            "Try This Quiz Again",
            key=f"retry_{selected}"
        ):
            for i in range(len(questions)):
                answer_key = f"{selected}_answer_{i}"

                if answer_key in st.session_state:
                    del st.session_state[answer_key]

            st.session_state.quiz_submitted = False
            st.rerun()

    if st.button("Back to Subjects", key="back_subjects"):
        st.session_state.selected_quiz = None
        st.session_state.quiz_submitted = False
        st.rerun()


# ---------- BOTTOM SECTION ----------
st.markdown("""
<div class="info-strip">
    <strong>Small steps. Stronger skills.</strong><br>
    Build your technical knowledge through consistent practice.
</div>

<div class="footer-note">
    KNOWBIT · LEARN. PRACTICE. IMPROVE.
</div>
""", unsafe_allow_html=True)

