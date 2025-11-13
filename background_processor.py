"""
Background task processor for handling RAG updates asynchronously.
"""

import os
import json
import threading
import time
from datetime import datetime
import asyncio
from update_rag import update_rag_from_file

class BackgroundProcessor:
    def __init__(self):
        self.processing_queue = []
        self.processed_files = set()
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the background processor"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._process_queue, daemon=True)
            self.thread.start()
            print("Background processor started")
            
    def stop(self):
        """Stop the background processor"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("Background processor stopped")
            
    def queue_update_file(self, file_path):
        """Queue a file for RAG update processing"""
        if file_path not in self.processed_files:
            self.processing_queue.append(file_path)
            self.processed_files.add(file_path)
            print(f"Queued {file_path} for RAG update processing")
            return True
        else:
            print(f"File {file_path} already queued or processed")
            return False
            
    def _process_queue(self):
        """Process the queue in a background thread"""
        while self.running:
            if self.processing_queue:
                file_path = self.processing_queue.pop(0)
                try:
                    print(f"Processing RAG update from {file_path}")
                    # Run the async function in a new event loop
                    result = asyncio.run(update_rag_from_file(file_path))
                    if result:
                        print(f"Successfully processed RAG update from {file_path}")
                        # Optionally remove the file after processing
                        # os.remove(file_path)
                    else:
                        print(f"Failed to process RAG update from {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            else:
                # Sleep briefly to avoid busy waiting
                time.sleep(1)

# Global background processor instance
background_processor = BackgroundProcessor()

def start_background_processor():
    """Start the background processor"""
    background_processor.start()
    
def stop_background_processor():
    """Stop the background processor"""
    background_processor.stop()
    
def queue_file_for_processing(file_path):
    """Queue a file for background processing"""
    return background_processor.queue_update_file(file_path)