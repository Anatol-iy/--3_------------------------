import argparse
import shutil
from pathlib import Path

# ANSI escape codes for colored output
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

def display_tree(path: Path, indent: str = "", prefix: str = "") -> None:
    if path.is_dir():
        # Використовуємо синій колір для директорій
        print(indent + prefix + COLOR_BLUE + str(path.name) + COLOR_RESET)
        indent += "    " if prefix else ""

        # Отримуємо відсортований список дітей, з директоріями в кінці
        children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))

        for index, child in enumerate(children):
            # Перевіряємо, чи поточна дитина є останньою у директорії
            is_last = index == len(children) - 1
            display_tree(child, indent, "└── " if is_last else "├── ")
    else:
        print(indent + prefix + str(path.name))

def copy_files(source_dir: Path, dest_dir: Path) -> None:
    for item in source_dir.iterdir():
        if item.is_file():
            extension = item.suffix[1:].lower()
            dest_subdir = dest_dir / extension
            dest_subdir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_subdir)
        elif item.is_dir():
            copy_files(item, dest_dir)

def main():
    parser = argparse.ArgumentParser(description="Копіювання файлів рекурсивно та сортування їх за розширенням")
    parser.add_argument("source_dir", type=str, help="Шлях до вихідної директорії")
    parser.add_argument("dest_dir", type=str, nargs="?", default="dist", help="Шлях до директорії призначення (за замовчуванням: dist)")
    args = parser.parse_args()

    source_path = Path(args.source_dir)
    dest_path = Path(args.dest_dir)

    # Відображення дерева директорій перед копіюванням
    print("Дерево вихідної директорії:")
    display_tree(source_path)

    # Копіювання файлів рекурсивно та сортування їх за розширенням
    print("\nКопіювання файлів...")
    copy_files(source_path, dest_path)

    # Відображення дерева директорій після копіювання
    print("\nДерево директорії призначення:")
    display_tree(dest_path)

if __name__ == "__main__":
    main()