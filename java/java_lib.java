import java.util.*;

class Book {
    String title;
    String author;
    boolean isBorrowed;

    public Book(String title, String author) {
        this.title = title;
        this.author = author;
        this.isBorrowed = false;
    }

    public void borrowBook() {
        if (!isBorrowed) {
            isBorrowed = true;
            System.out.println("You borrowed \"" + title + "\"");
        } else {
            System.out.println("Sorry, \"" + title + "\" is already borrowed.");
        }
    }

    public void returnBook() {
        if (isBorrowed) {
            isBorrowed = false;
            System.out.println("You returned \"" + title + "\"");
        } else {
            System.out.println("This book wasn't borrowed.");
        }
    }
}

public class LibrarySystem {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Book> books = new ArrayList<>();

        books.add(new Book("Harry Potter", "J.K. Rowling"));
        books.add(new Book("The Hobbit", "J.R.R. Tolkien"));
        books.add(new Book("1984", "George Orwell"));

        while (true) {
            System.out.println("\n=== Library Menu ===");
            System.out.println("1. List Books");
            System.out.println("2. Borrow Book");
            System.out.println("3. Return Book");
            System.out.println("4. Exit");
            System.out.print("Choose an option: ");
            int choice = sc.nextInt();
            sc.nextLine();

            if (choice == 1) {
                System.out.println("\nAvailable Books:");
                for (int i = 0; i < books.size(); i++) {
                    Book b = books.get(i);
                    System.out.println(i + ". " + b.title + " by " + b.author + (b.isBorrowed ? " (Borrowed)" : ""));
                }

            } else if (choice == 2) {
                System.out.print("Enter book index to borrow: ");
                int idx = sc.nextInt();
                sc.nextLine();
                if (idx >= 0 && idx < books.size()) {
                    books.get(idx).borrowBook();
                } else {
                    System.out.println("Invalid book index!");
                }

            } else if (choice == 3) {
                System.out.print("Enter book index to return: ");
                int idx = sc.nextInt();
                sc.nextLine();
                if (idx >= 0 && idx < books.size()) {
                    books.get(idx).returnBook();
                } else {
                    System.out.println("Invalid book index!");
                }

            } else if (choice == 4) {
                System.out.println("Goodbye!");
                break;

            } else {
                System.out.println("Invalid choice, try again.");
            }
        }
        sc.close();
    }
}
