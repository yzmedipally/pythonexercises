# giteducated - exercises

This is a solution to ease the work of a class instructor using the lrz gitlab to manage exercises accompanying university lectures.
The original idea stemmed from a TUM course (IN 2085) and a related [github project](https://github.com/education/teachers_pet).

## Usage

```bash
# Checks the configuration file 
# no special rights needed:
./exercises.py --config <path_to_config_file> --action check 

# Initializes the project (can also be used to update gitlab to an updated config file)
# this defines who is admin, i.e. first call no special rights needed, after that admin rights
./exercises.py --config <path_to_config_file> --action init

# Publishes an exercise in a "namespace"
# admin rights needed
# tba:
./exercises.py --config <path_to_config_file> --action publish --exercise exerciseID 

# Checks out the solutions for the reviewer 
# token must at least have REPORTER rights 
./exercises.py --config <path_to_config_file> --action download --exercise exerciseID 

# Deprovisions a whole course
# admin rights needed
./exercises.py --config <path_to_config_file> --action delete --exercise exerciseID 

``` 

## Configuration

Please consult example the [configuration file](https://gitlab.lrz.de/giteducated/exercises/blob/master/example_config.json)

## Installation & Requirements

tba

## Design

### Roles

* __instructor__: Organizes the exercises, may do anything.
* __reviewer__: Corrects the solutions sent in by students. Is not allowed to change the overall structure of the exercises.
* __student__: Sends in the solutions and retrieves the feedback. Is only granted developer's access rights in his or her exercise group's projects.

### Domain

| course          | gitlab             |
|-----------------|--------------------|
| instructor      | owner/master       |
| reviewer        | developer/reporter |
| student         | developer          |
| exercise        | project            |
| exercise group  | group/namespace    |

### Workflow

1. The instructor generates the overall structure of the exercises:
  * Each gitlab group corresponds to an exercise group (one or more students). The name of the exercise group should include a reference to the course, the semester and an identifier inside this namespace (e.g. increasing integers).
  * Each student has logged in at least once in gitlab (therefore his or her account exists). The instructor can now connect the student's account with an exercise group.
  * Each gitlab project inside an exercise group corresponds to an exercise. An exercise has a due date and an instructor or reviewer to correct the solution provided by the student. These things are realized by commits (solutions) and the timestamp of the commit (due date).
2. The instructor can "publish" the exercises weekwise or once for all. This means that in each exercise group an project including the accodording file structure is committed.
3. The students pull/fork the exercise and push/merge their solution back to the according project in the according exercise group.
4. The reviewer automatically clones each repository to his or her machine and reviews. Feedback could be realized either as a further commit (exists in git and gitlab) or as one or more comment(s) to the corrected commit (exists only in gitlab, but could be made linewise in committed code). The last commit earlier than or concurrent  to the due date is considered the solution provided by the students.
5. After the exams the instructer deprovisions exercise groups and projects.

## Wishlist
This list should either be deleted or mapped to issues of this project
* Automatic checking of plagiarisms (hashsums of binary files, etc.)?
* Using issues and/or milestones for the exercises? 
