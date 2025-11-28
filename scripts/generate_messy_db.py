"""Generate a messy demo database for testing"""
import sqlite3
from faker import Faker
import random
from pathlib import Path

fake = Faker()

def create_messy_database(db_path='data/messy_demo.db'):
    """Generate a realistic messy database"""
    
    # Ensure data directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing database
    if Path(db_path).exists():
        Path(db_path).unlink()
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    print("Creating schema...")
    
    # Create tables
    c.executescript('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            created_at TEXT,
            status TEXT
        );
        
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            stock INTEGER
        );
    ''')
    
    print("Generating clean data...")
    
    # Generate clean users
    users = []
    for i in range(1000):
        users.append((
            fake.email(),
            fake.first_name(),
            fake.last_name(),
            fake.phone_number(),
            fake.date_time_this_year().isoformat(),
            random.choice(['active', 'inactive', 'pending'])
        ))
    
    c.executemany('''
        INSERT INTO users (email, first_name, last_name, phone, created_at, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', users)
    
    # Generate products
    for _ in range(100):
        c.execute('''
            INSERT INTO products (name, price, stock)
            VALUES (?, ?, ?)
        ''', (fake.catch_phrase(), round(random.uniform(9.99, 999.99), 2), random.randint(0, 100)))
    
    # Generate orders
    for _ in range(500):
        c.execute('''
            INSERT INTO orders (user_id, amount, status, created_at)
            VALUES (?, ?, ?, ?)
        ''', (
            random.randint(1, 1000),
            round(random.uniform(10, 1000), 2),
            random.choice(['pending', 'completed', 'cancelled']),
            fake.date_time_this_month().isoformat()
        ))
    
    print("Injecting data quality issues...")
    
    # 1. Add duplicate users (exact copies)
    c.execute('''
        INSERT INTO users (email, first_name, last_name, phone, created_at, status)
        SELECT email, first_name, last_name, phone, created_at, status
        FROM users WHERE id <= 50
    ''')
    
    # 2. Add duplicate users (case variation)
    c.execute('''
        INSERT INTO users (email, first_name, last_name, phone, created_at, status)
        SELECT UPPER(email), first_name, last_name, phone, created_at, status
        FROM users WHERE id BETWEEN 51 AND 100
    ''')
    
    # 3. Add NULL emails
    c.execute('UPDATE users SET email = NULL WHERE id BETWEEN 101 AND 120')
    
    # 4. Add orphaned orders (non-existent user_id)
    for _ in range(30):
        c.execute('''
            INSERT INTO orders (user_id, amount, status, created_at)
            VALUES (?, ?, ?, ?)
        ''', (99999, random.uniform(10, 500), 'completed', fake.date_time_this_month().isoformat()))
    
    # 5. Add negative prices
    c.execute('UPDATE products SET price = -price WHERE id <= 10')
    
    # 6. Add future dates
    c.execute("UPDATE users SET created_at = '2050-01-01' WHERE id BETWEEN 121 AND 130")
    
    conn.commit()
    
    # Print summary
    print("\n" + "="*60)
    print(f"DATABASE CREATED: {db_path}")
    print("="*60)
    
    for table in ['users', 'orders', 'products']:
        c.execute(f'SELECT COUNT(*) FROM {table}')
        count = c.fetchone()[0]
        print(f"{table.upper()}: {count} records")
    
    print("\n" + "="*60)
    print("INJECTED ISSUES:")
    print("="*60)
    
    # Count duplicates
    c.execute('''
        SELECT COUNT(*) FROM (
            SELECT LOWER(email) as email FROM users 
            WHERE email IS NOT NULL
            GROUP BY LOWER(email) 
            HAVING COUNT(*) > 1
        )
    ''')
    dup_emails = c.fetchone()[0]
    print(f"✗ Duplicate emails: ~{dup_emails * 2}")
    
    # Count NULLs
    c.execute('SELECT COUNT(*) FROM users WHERE email IS NULL')
    nulls = c.fetchone()[0]
    print(f"✗ Users with NULL email: {nulls}")
    
    # Count orphaned orders
    c.execute('''
        SELECT COUNT(*) FROM orders 
        WHERE user_id NOT IN (SELECT id FROM users)
    ''')
    orphans = c.fetchone()[0]
    print(f"✗ Orphaned orders: {orphans}")
    
    # Count negative prices
    c.execute('SELECT COUNT(*) FROM products WHERE price < 0')
    neg_prices = c.fetchone()[0]
    print(f"✗ Products with negative price: {neg_prices}")
    
    # Count future dates
    c.execute('SELECT COUNT(*) FROM users WHERE created_at > date("now")')
    future_dates = c.fetchone()[0]
    print(f"✗ Users with future created_at: {future_dates}")
    
    print("="*60 + "\n")
    
    conn.close()
    
    return db_path

if __name__ == '__main__':
    db_path = create_messy_database()
    print(f"✓ Ready to use: {db_path}")