import java.util.*;

class Course {
    String name;
    String grade; // A-F
    int creditHours;
    String honors; // "None", "Honors", "AP"

    public Course(String name, String grade, int creditHours, String honors) {
        this.name = name;
        this.grade = grade.toUpperCase();
        this.creditHours = creditHours;
        this.honors = honors;
    }

    // Convert letter grade to GPA points (4.0 scale)
    public double getBaseGradePoints() {
        switch (grade) {
            case "A": return 4.0;
            case "B": return 3.0;
            case "C": return 2.0;
            case "D": return 1.0;
            default: return 0.0;
        }
    }

    // Adjust GPA points for Honors/AP in high school mode
    public double getAdjustedPoints(boolean collegeMode) {
        double points = getBaseGradePoints();
        if (!collegeMode) {
            if (honors.equalsIgnoreCase("Honors")) {
                points += 0.5;
            } else if (honors.equalsIgnoreCase("AP")) {
                points += 1.0;
            }
        }
        return points;
    }
}

class Student {
    String name;
    ArrayList<Course> courses = new ArrayList<>();

    public Student(String name) {
        this.name = name;
    }

    public void addCourse(Course course) {
        courses.add(course);
    }

    public double calculateGPA(boolean collegeMode) {
        if (courses.isEmpty()) return 0.0;

        double totalPoints = 0;
        int totalCredits = 0;

        for (Course c : courses) {
            int credits = collegeMode ? c.creditHours : 1;
            totalPoints += c.getAdjustedPoints(collegeMode) * credits;
            totalCredits += credits;
        }

        return totalCredits == 0 ? 0.0 : totalPoints / totalCredits;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Student> students = new ArrayList<>();
        boolean collegeMode = true; // Default GPA mode

        while (true) {
            System.out.println("\n=== Student GPA Manager ===");
            System.out.println("Mode: " + (collegeMode ? "College (Weighted by Credit Hours)" : "High School (Honors/AP Weighted)"));
            System.out.println("1. Add Student");
            System.out.println("2. Add Course to Student");
            System.out.println("3. Calculate GPA for All Students");
            System.out.println("4. Switch Mode (College ↔ High School)");
            System.out.println("5. Exit");
            System.out.print("Choose an option: ");

            int choice;
            try {
                choice = Integer.parseInt(sc.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a number between 1-5.");
                continue;
            }

            if (choice == 1) {
                System.out.print("Enter student name: ");
                String name = sc.nextLine();
                students.add(new Student(name));
                System.out.println("Student added successfully!");

            } else if (choice == 2) {
                if (students.isEmpty()) {
                    System.out.println("No students available. Add a student first!");
                    continue;
                }

                System.out.println("Select a student:");
                for (int i = 0; i < students.size(); i++) {
                    System.out.println(i + ": " + students.get(i).name);
                }

                int idx;
                try {
                    idx = Integer.parseInt(sc.nextLine());
                } catch (NumberFormatException e) {
                    System.out.println("Invalid index!");
                    continue;
                }

                if (idx < 0 || idx >= students.size()) {
                    System.out.println("Invalid student index!");
                    continue;
                }

                System.out.print("Enter course name: ");
                String courseName = sc.nextLine();

                System.out.print("Enter letter grade (A-F): ");
                String grade = sc.nextLine();

                int credits = 1;
                if (collegeMode) {
                    System.out.print("Enter credit hours: ");
                    try {
                        credits = Integer.parseInt(sc.nextLine());
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid credit hours. Defaulting to 1.");
                        credits = 1;
                    }
                }

                System.out.print("Enter course type (None/Honors/AP): ");
                String honors = sc.nextLine();

                students.get(idx).addCourse(new Course(courseName, grade, credits, honors));
                System.out.println("Course added successfully!");

            } else if (choice == 3) {
                if (students.isEmpty()) {
                    System.out.println("No students available to calculate GPA.");
                } else {
                    for (Student s : students) {
                        System.out.printf("%s's GPA: %.2f\n", s.name, s.calculateGPA(collegeMode));
                    }
                }

            } else if (choice == 4) {
                collegeMode = !collegeMode;
                System.out.println("Switched mode to: " + (collegeMode ? "College" : "High School"));

            } else if (choice == 5) {
                System.out.println("Exiting program. Goodbye!");
                break;

            } else {
                System.out.println("Invalid choice. Please try again.");
            }
        }

        sc.close();
    }
}
