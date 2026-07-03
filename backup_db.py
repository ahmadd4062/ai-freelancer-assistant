import sqlite3
import datetime
import os

def backup_database():
    """Create a backup of the SQLite database"""
    db_path = 'db.sqlite3'
    backup_dir = 'backups'
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Create backup filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'db_backup_{timestamp}.sqlite3')
    
    # Copy database
    import shutil
    shutil.copy2(db_path, backup_path)
    
    print(f'Database backed up to: {backup_path}')

if __name__ == '__main__':
    backup_database()