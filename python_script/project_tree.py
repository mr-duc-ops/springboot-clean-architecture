#!/usr/bin/env python3
# project_tree.py

from pathlib import Path
import os

def print_project_tree(start_path=".", max_depth=10):
    start_path = Path(start_path).resolve()
    ignore_dirs = {
        '.git', 'target', 'node_modules', '__pycache__', 'build', 'dist',
        '.idea', '.vscode', '.settings', 'bin', 'out'
    }
    ignore_files = {'.mv.db', '.trace.db', '.log', '.jar', '.class'}

    print(f"# Project Structure")
    print(f"# Root: {start_path}")
    print(f"# Generated at: {os.popen('date').read().strip()}\n")

    for root, dirs, files in os.walk(start_path):
        path = Path(root)
        level = len(path.relative_to(start_path).parts)
        
        if level > max_depth:
            continue

        # Lọc ignore
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        indent = "   " * level
        folder_name = path.name if path.name else start_path.name
        
        print(f"{indent}📁 {folder_name}/")
        
        # In files (giới hạn số lượng)
        for file in sorted(files):
            if not any(file.endswith(ext) for ext in ignore_files):
                file_indent = "   " * (level + 1)
                print(f"{file_indent}📄 {file}")

if __name__ == "__main__":
    print_project_tree(".")