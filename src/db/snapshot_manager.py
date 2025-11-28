"""Snapshot Manager - Git-inspired database backups"""
import shutil
import hashlib
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class SnapshotManager:
    """
    Manages database snapshots (backups) with Git-inspired functionality.
    
    Responsibilities:
    - Create snapshots (backups) of databases
    - Store metadata about each snapshot
    - Restore databases from snapshots
    - Verify snapshot integrity using checksums
    - List and manage snapshot lifecycle
    """
    
    def __init__(self, db_path: str, snapshots_dir: str = "data/snapshots"):
        """
        Initialize the snapshot manager.
        
        Args:
            db_path: Path to the database file to snapshot
            snapshots_dir: Directory where snapshots will be stored
        """
        self.db_path = Path(db_path)
        self.snapshots_dir = Path(snapshots_dir)
        self.metadata_file = self.snapshots_dir / "snapshots.json"
        
        # TODO: Create snapshots directory if it doesn't exist
        Path.mkdir()
        # HINT: Use Path.mkdir() with appropriate parameters
        # Remember: You want to create parent directories and not error if it exists
        
    
    def create_snapshot(self, description: str) -> str:
        """
        Create a snapshot (backup) of the database.
        
        This is like 'git commit' - it saves the current state.
        
        Args:
            description: Human-readable description (like a commit message)
            
        Returns:
            snapshot_id: Unique identifier for this snapshot
            
        Steps:
        1. Generate unique snapshot ID
        2. Copy database file to snapshots directory
        3. Calculate checksum for integrity verification
        4. Capture metadata (row counts, size, etc.)
        5. Save metadata to snapshots.json
        """
        # TODO: Generate unique snapshot ID
        # HINT: Use format "snap_{timestamp}_{short_uuid}"
        # timestamp format: "%Y%m%d_%H%M%S"
        # short_uuid: first 8 characters of uuid.uuid4()
        snapshot_id = None  # Replace with your implementation
        
        # TODO: Create the snapshot file path
        # HINT: snapshots_dir / f"{snapshot_id}.db"
        snapshot_path = None  # Replace with your implementation
        
        # TODO: Copy the database file to snapshot location
        # HINT: Use shutil.copy2() for copying with metadata preservation
        # HINT: Wrap in try/except to handle disk full or permission errors
        # If copy fails, clean up partial file and raise exception
        
        
        # TODO: Calculate checksum of the snapshot file
        # HINT: Call self._calculate_checksum(snapshot_path)
        checksum = None  # Replace with your implementation
        
        # TODO: Get row counts for each table
        # HINT: You'll need to import and use SQLiteAdapter
        # HINT: Connect to the ORIGINAL db_path, get all tables, get row count for each
        # Store as: {"users": 1100, "orders": 530, "products": 100}
        table_row_counts = {}  # Replace with your implementation
        
        # TODO: Build metadata dictionary
        # Include: id, timestamp (ISO format), description, db_path, snapshot_path,
        #          size_bytes, checksum, table_row_counts, pinned (default False)
        metadata = {
            # Fill this in
        }
        
        # TODO: Save metadata to snapshots.json
        # HINT: Call self._save_metadata(metadata)
        
        
        return snapshot_id
    
    
    def restore_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Restore database from a snapshot.
        
        This is like 'git revert' - it goes back to a previous state.
        
        Args:
            snapshot_id: ID of the snapshot to restore
            
        Returns:
            metadata: Information about the restored snapshot
            
        Steps:
        1. Get snapshot metadata
        2. Verify snapshot file exists
        3. Verify checksum (ensure not corrupted)
        4. Optionally: Create snapshot of current state (snapshot-before-restore)
        5. Replace current database with snapshot
        6. Verify restoration worked (check row counts)
        """
        # TODO: Get metadata for this snapshot
        # HINT: Call self._get_metadata(snapshot_id)
        # This should raise an error if snapshot doesn't exist
        metadata = None  # Replace with your implementation
        
        # TODO: Get snapshot path from metadata
        snapshot_path = None  # Replace with your implementation
        
        # TODO: Verify snapshot file exists
        # HINT: Use Path.exists()
        # If not, raise ValueError with helpful message
        
        
        # TODO: Verify checksum to ensure snapshot isn't corrupted
        # HINT: Calculate current checksum of snapshot file
        # HINT: Compare with metadata['checksum']
        # If they don't match, raise ValueError - DO NOT RESTORE CORRUPTED DATA!
        
        
        # OPTIONAL (but recommended): Create snapshot of current state before restoring
        # This way user can undo the restore if they made a mistake
        # TODO: Uncomment and implement if you want this safety feature
        # current_snapshot_id = self.create_snapshot(f"before-restore-to-{snapshot_id}")
        
        # TODO: Replace current database with snapshot
        # HINT: Use shutil.copy2(snapshot_path, self.db_path)
        # HINT: Wrap in try/except for PermissionError (file might be locked)
        # If locked, raise helpful error telling user to close other connections
        
        
        # TODO: Verify restoration worked by checking row counts
        # HINT: Import SQLiteAdapter, connect to restored db, get row counts
        # HINT: Compare with metadata['table_row_counts']
        # If counts don't match, something went wrong!
        # (Optional: Could restore the pre-restore snapshot here if verification fails)
        
        
        return metadata
    
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """
        List all available snapshots.
        
        Returns:
            List of snapshot metadata dictionaries, sorted by timestamp (newest first)
        """
        # TODO: Check if metadata file exists
        # HINT: Use self.metadata_file.exists()
        # If it doesn't exist, return empty list (no snapshots yet)
        
        
        # TODO: Read and parse JSON file
        # HINT: Use json.load()
        # Return the 'snapshots' list from the JSON
        # Sort by timestamp descending (newest first) before returning
        
        pass  # Replace with your implementation
    
    
    def get_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific snapshot.
        
        Args:
            snapshot_id: ID of the snapshot
            
        Returns:
            Snapshot metadata dictionary
        """
        # TODO: This is just a convenience method
        # HINT: Call self._get_metadata(snapshot_id)
        pass  # Replace with your implementation
    
    
    def delete_snapshot(self, snapshot_id: str):
        """
        Delete a snapshot (both file and metadata).
        
        Args:
            snapshot_id: ID of snapshot to delete
        """
        # TODO: Get snapshot metadata
        metadata = None  # Replace
        
        # TODO: Delete the snapshot file
        # HINT: Get path from metadata, use Path.unlink()
        # HINT: Use missing_ok=True so it doesn't error if file already gone
        
        
        # TODO: Remove from metadata JSON
        # HINT: Load all snapshots, filter out this one, save back
        # You'll need to implement this logic
        
        pass  # Replace with your implementation
    
    
    def pin_snapshot(self, snapshot_id: str):
        """
        Pin a snapshot to prevent it from being auto-deleted.
        
        Args:
            snapshot_id: ID of snapshot to pin
        """
        # TODO: Get all snapshots
        # Find the one with matching ID
        # Set its 'pinned' field to True
        # Save back to JSON
        # HINT: Similar to delete, but modify instead of remove
        
        pass  # Replace with your implementation
    
    
    def unpin_snapshot(self, snapshot_id: str):
        """
        Unpin a snapshot (allow it to be auto-deleted).
        
        Args:
            snapshot_id: ID of snapshot to unpin
        """
        # TODO: Same as pin_snapshot but set 'pinned' to False
        pass  # Replace with your implementation
    
    
    def cleanup_old_snapshots(self, max_unpinned: int = 20):
        """
        Delete old unpinned snapshots, keeping only the most recent ones.
        
        Pinned snapshots are NEVER deleted.
        
        Args:
            max_unpinned: Maximum number of unpinned snapshots to keep
        """
        # TODO: Get all snapshots
        snapshots = self.list_snapshots()
        
        # TODO: Separate into pinned and unpinned lists
        # HINT: Use list comprehension with snapshot.get('pinned', False)
        unpinned = []  # Replace
        pinned = []    # Replace
        
        # TODO: Sort unpinned by timestamp (oldest first)
        # HINT: Use sorted() with key=lambda s: s['timestamp']
        
        
        # TODO: Identify snapshots to delete
        # HINT: If len(unpinned) > max_unpinned, delete the oldest ones
        # Keep only the last max_unpinned
        to_delete = []  # Replace with list of snapshots to delete
        
        # TODO: Delete each old snapshot
        # HINT: Loop through to_delete and call self.delete_snapshot()
        
        pass  # Replace with your implementation
    
    
    # ========================================
    # PRIVATE HELPER METHODS
    # ========================================
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """
        Calculate SHA-256 checksum of a file.
        
        This creates a "fingerprint" of the file to detect corruption.
        
        Args:
            file_path: Path to file to checksum
            
        Returns:
            Hexadecimal string of SHA-256 hash
        """
        # TODO: Create SHA-256 hasher
        # HINT: sha256 = hashlib.sha256()
        
        
        # TODO: Read file in chunks and update hash
        # HINT: Open file in binary mode ('rb')
        # HINT: Read 4096 bytes at a time (don't load entire DB into memory!)
        # HINT: Use: for chunk in iter(lambda: f.read(4096), b''):
        # HINT: Update hash with each chunk: sha256.update(chunk)
        
        
        # TODO: Return hexadecimal digest
        # HINT: return sha256.hexdigest()
        
        pass  # Replace with your implementation
    
    
    def _save_metadata(self, metadata: Dict[str, Any]):
        """
        Append new snapshot metadata to snapshots.json.
        
        Args:
            metadata: Snapshot metadata dictionary to save
        """
        # TODO: Load existing snapshots (if file exists)
        # HINT: If file doesn't exist, start with empty list
        snapshots = []
        if self.metadata_file.exists():
            # Load existing
            pass  # Replace with json.load()
        
        # TODO: Append new metadata to list
        
        
        # TODO: Write back to file
        # HINT: Use json.dump() with indent=2 for readability
        
        pass  # Replace with your implementation
    
    
    def _get_metadata(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific snapshot.
        
        Args:
            snapshot_id: ID of snapshot to find
            
        Returns:
            Snapshot metadata dictionary
            
        Raises:
            ValueError: If snapshot not found
        """
        # TODO: Get all snapshots
        snapshots = self.list_snapshots()
        
        # TODO: Find the one with matching ID
        # HINT: Loop through or use next() with generator
        # If not found, raise ValueError(f"Snapshot {snapshot_id} not found")
        
        pass  # Replace with your implementation
    
    
    def _generate_snapshot_id(self) -> str:
        """
        Generate unique snapshot ID in format: snap_YYYYMMDD_HHMMSS_xxxxxxxx
        
        Returns:
            Unique snapshot ID string
        """
        # TODO: Get current timestamp
        # HINT: datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp = None  # Replace
        
        # TODO: Generate short UUID (first 8 characters)
        # HINT: str(uuid.uuid4())[:8]
        short_uuid = None  # Replace
        
        # TODO: Combine into format: snap_{timestamp}_{short_uuid}
        return None  # Replace with formatted string


# ========================================
# OPTIONAL: CLI INTEGRATION EXAMPLE
# ========================================

if __name__ == "__main__":
    """
    Quick test of SnapshotManager functionality.
    Run with: python src/db/snapshot_manager.py
    """
    
    # Test with your messy demo database
    manager = SnapshotManager("data/messy_demo.db")
    
    # Create a snapshot
    print("Creating snapshot...")
    snapshot_id = manager.create_snapshot("test snapshot from main")
    print(f"✅ Created: {snapshot_id}")
    
    # List snapshots
    print("\nAll snapshots:")
    for snap in manager.list_snapshots():
        print(f"  {snap['id']}: {snap['description']}")
    
    # TODO: Add more tests here as you implement methods
    # - Try restoring a snapshot
    # - Try pinning/unpinning
    # - Try cleanup