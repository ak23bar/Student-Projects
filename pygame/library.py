# library.py
# A simple menu-driven Library app for beginners
# Features: add books/members, list/search, borrow/return, optional autosave

from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field
from datetime import date, timedelta
from typing import Dict, List, Optional

DATA_FILE = "library_data.json"
AUTOSAVE = True       # set to False if you don't want files yet
LOAN_DAYS = 14        # due date window

# ---------- Models ----------
@dataclass
class Book:
    id: int
    title: str
    author: str
    copies_total: int
    copies_available: int

@dataclass
class BorrowRecord:
    book_id: int
    due: str  # ISO date string

@dataclass
class Member:
    id: int
    name: str
    borrowed: List[BorrowRecord] = field(default_factory=list)

# ---------- Library Core ----------
class Library:
    def __init__(self) -> None:
        self.books: Dict[int, Book] = {}
        self.members: Dict[int, Member] = {}
        self._next_book_id = 1
        self._next_member_id = 1

    # ----- Book ops -----
    def add_book(self, title: str, author: str, copies: int) -> Book:
        if copies < 1:
            raise ValueError("Copies must be at least 1.")
        b = Book(
            id=self._next_book_id,
            title=title.strip(),
            author=author.strip(),
            copies_total=copies,
            copies_available=copies,
        )
        self.books[b.id] = b
        self._next_book_id += 1
        return b

    def find_books(self, query: str) -> List[Book]:
        q = query.lower().strip()
        return [
            b for b in self.books.values()
            if q in b.title.lower() or q in b.author.lower()
        ]

    # ----- Member ops -----
    def add_member(self, name: str) -> Member:
        m = Member(id=self._next_member_id, name=name.strip())
        self.members[m.id] = m
        self._next_member_id += 1
        return m

    # ----- Borrow/Return -----
    def borrow(self, member_id: int, book_id: int) -> str:
        m = self.members.get(member_id)
        b = self.books.get(book_id)
        if not m:
            return "Member not found."
        if not b:
            return "Book not found."
        if b.copies_available < 1:
            return f"'{b.title}' is currently out of stock."

        # Prevent duplicate borrow of same book by same member
        if any(rec.book_id == book_id for rec in m.borrowed):
            return "This member already borrowed that book."

        b.copies_available -= 1
        due_date = date.today() + timedelta(days=LOAN_DAYS)
        m.borrowed.append(BorrowRecord(book_id=book_id, due=due_date.isoformat()))
        return f"Borrowed '{b.title}'. Due on {due_date.isoformat()}."

    def return_book(self, member_id: int, book_id: int) -> str:
        m = self.members.get(member_id)
        b = self.books.get(book_id)
        if not m:
            return "Member not found."
        if not b:
            return "Book not found."

        for i, rec in enumerate(m.borrowed):
            if rec.book_id == book_id:
                # remove record and increment availability
                m.borrowed.pop(i)
                b.copies_available = min(b.copies_total, b.copies_available + 1)
                return f"Returned '{b.title}'. Thank you!"
        return "That member does not have this book checked out."

    # ----- Persistence -----
    def to_json(self) -> dict:
        return {
            "books": [asdict(b) for b in self.books.values()],
            "members": [
                {"id": m.id, "name": m.name, "borrowed": [asdict(rec) for rec in m.borrowed]}
                for m in self.members.values()
            ],
            "next_ids": {"book": self._next_book_id, "member": self._next_member_id},
        }

    @classmethod
    def from_json(cls, data: dict) -> "Library":
        lib = cls()
        for b in data.get("books", []):
            book = Book(**b)
            lib.books[book.id] = book
        for m in data.get("members", []):
            member = Member(id=m["id"], name=m["name"],
                            borrowed=[BorrowRecord(**r) for r in m.get("borrowed", [])])
            lib.members[member.id] = member
        next_ids = data.get("next_ids", {})
        lib._next_book_id = int(next_ids.get("book", len(lib.books) + 1))
        lib._next_member_id = int(next_ids.get("member", len(lib.members) + 1))
        return lib

    def save(self, path: str = DATA_FILE) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_json(), f, indent=2)

    @classmethod
    def load(cls, path: str = DATA_FILE) -> "Library":
        try:
            with open(path, "r", encoding="utf-8") as f:
                return cls.from_json(json.load(f))
        except FileNotFoundError:
            return cls()

# ---------- CLI Helpers ----------
def line(char: str = "-") -> None:
    print(char * 60)

def prompt_int(label: str) -> Optional[int]:
    try:
        return int(input(label).strip())
    except ValueError:
        print("Please enter a valid number.")
        return None

def list_books(lib: Library) -> None:
    if not lib.books:
        print("No books in library yet.")
        return
    line("=")
    print(f"{'ID':<4} {'Title':<28} {'Author':<20} Avail/Total")
    line("=")
    for b in sorted(lib.books.values(), key=lambda x: x.id):
        print(f"{b.id:<4} {b.title[:28]:<28} {b.author[:20]:<20} {b.copies_available}/{b.copies_total}")
    line()

def list_members(lib: Library) -> None:
    if not lib.members:
        print("No members yet.")
        return
    line("=")
    print(f"{'ID':<4} {'Name':<25} Borrowed")
    line("=")
    for m in sorted(lib.members.values(), key=lambda x: x.id):
        borrowed_str = ", ".join(
            f"{lib.books[rec.book_id].title} (due {rec.due})"
            if rec.book_id in lib.books else f"Book#{rec.book_id} (due {rec.due})"
            for rec in m.borrowed
        ) or "-"
        print(f"{m.id:<4} {m.name[:25]:<25} {borrowed_str}")
    line()

def search_books(lib: Library) -> None:
    q = input("Search by title/author: ").strip()
    hits = lib.find_books(q)
    if not hits:
        print("No matches.")
        return
    for b in hits:
        print(f"[{b.id}] {b.title} — {b.author}  ({b.copies_available}/{b.copies_total} available)")

def add_book_cli(lib: Library) -> None:
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    copies = prompt_int("Number of copies: ")
    if copies is None:
        return
    try:
        b = lib.add_book(title, author, copies)
        print(f"Added book #{b.id}: {b.title} by {b.author}")
    except ValueError as e:
        print("Error:", e)

def add_member_cli(lib: Library) -> None:
    name = input("Member name: ").strip()
    m = lib.add_member(name)
    print(f"Added member #{m.id}: {m.name}")

def borrow_cli(lib: Library) -> None:
    member_id = prompt_int("Member ID: ")
    if member_id is None: return
    book_id = prompt_int("Book ID: ")
    if book_id is None: return
    msg = lib.borrow(member_id, book_id)
    print(msg)

def return_cli(lib: Library) -> None:
    member_id = prompt_int("Member ID: ")
    if member_id is None: return
    book_id = prompt_int("Book ID: ")
    if book_id is None: return
    msg = lib.return_book(member_id, book_id)
    print(msg)

def save_if_enabled(lib: Library) -> None:
    if AUTOSAVE:
        lib.save()

# ---------- Main Menu ----------
def main() -> None:
    lib = Library.load() if AUTOSAVE else Library()
    while True:
        print("\n===== Mini Library =====")
        print("1) Add Book")
        print("2) Add Member")
        print("3) List Books")
        print("4) List Members")
        print("5) Search Books")
        print("6) Borrow Book")
        print("7) Return Book")
        print("8) Save Now")
        print("9) Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            add_book_cli(lib); save_if_enabled(lib)
        elif choice == "2":
            add_member_cli(lib); save_if_enabled(lib)
        elif choice == "3":
            list_books(lib)
        elif choice == "4":
            list_members(lib)
        elif choice == "5":
            search_books(lib)
        elif choice == "6":
            borrow_cli(lib); save_if_enabled(lib)
        elif choice == "7":
            return_cli(lib); save_if_enabled(lib)
        elif choice == "8":
            lib.save(); print("Saved.")
        elif choice == "9":
            if AUTOSAVE: lib.save()
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
