# giteducated - exercises

This is a set of scripts to ease the work of a class instructor using the lrz gitlab to manage exercises accompanying university lectures.
The original idea stemmed from a TUM course (IN 2085) and a related [github project](https://github.com/education/teachers_pet)

## Roles

* __instructor__: Organizes the exercises, may do anything.
* __reviewer__: Corrects the solutions sent in by students. Is not allowed to change the overall structure of the exercises.
* __student__: Sends in the solutions and retrieves the feedback. Is only granted developer's access rights in his or her exercise group's projects.

## Domain

| course          | gitlab           |
|-----------------|------------------|
| instructor      | owner            |
| reviewer        | reviewer         |
| student         | developer        |
| exercise        | project          |
| exercise group  | group            |

## Workflow

1. The instructor generates the overall structure of the exercises:
  * Each gitlab group corresponds to a exercise group (one or more students). The naming should include a reference to the course, the semester and an identifier inside this namespace.
  * Each gitlab project inside an exercise group corresponds to an exercise. An exercise has a due date and an instructor or reviewer to correct the solution provided by the student. These things are realized by commits (solutions) and its commit timestamp (due date).
2. The instructor can "publish" the exercises weekwise or once for all. This means that in each exercise group an project including the accodording file structure is committed.
3. The students pull/fork the exercise and push/merge their solution back to the according project in the according exercise group.
4. The reviewer automatically clones each repository to his machine, reviews. Feedback could be realized either as a further commit (?) or as a comment to the corrected commit. The last commit earlier than the due date is considered the solution provided by the students.
5. After the exams the instructer deprovisions exercise groups and projects.

## Usage

## Techstuff

The functionality is realized by using the [gitlab api](http://docs.gitlab.com/ce/api)

## Wishlist
* Automatic checking of plagiarisms (hashsums of binary files, etc.)

