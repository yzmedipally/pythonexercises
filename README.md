# giteducated - exercises

This is a solution to ease the work of a class instructor using the lrz gitlab to manage exercises accompanying university lectures.
The original idea stemmed from a TUM course (IN 2085) and a related [github project](https://github.com/education/teachers_pet).

## Usage

```bash
# Checks the configuration file 
# no special rights needed:
./exercises.py --config <path_to_config_file> --action check 

# Initializes the project (can also be used to update gitlab to an updated config file)
# this defines who is instructor, i.e. first call no special rights needed, after that instructor rights
./exercises.py --config <path_to_config_file> --action init

# Publishes an exercise in a "namespace"
# instructor rights needed
# tba:
./exercises.py --config <path_to_config_file> --action publish --exercise <exercise>

# Adds a reviewer to an exercise
./exercises.py --config <path_to_config_file> --action add_reviewer --exercise <exercise>

# Checks out the solutions for the reviewer 
# token must at least have reviewer rights 
./exercises.py --config <path_to_config_file> --action download --exercise <exercise> --duedate <unixtimestamp>

# Deprovisions a whole course
# instructor rights needed
./exercises.py --config <path_to_config_file> --action delete --exercise <exercise>

``` 

## Configuration

Please consult example the [configuration file](https://gitlab.lrz.de/giteducated/exercises/blob/master/example_config.json)

Please be aware that empty exercise projects in your master project are not supported (you'll have
to commit at least an exercise sheet).

To use it you should make sure:
* To have a free namespace (config-param pattern in your config.json)
* To have a master group in which you administer the exercises to be published
* To have an ssh-key for every account registered in gitlab that you want to use as instructor or reviewer (the according private key has to be installed on the machine used for the download action).

As a general advice: If your notification settings in gitlab are not adapted accordingly and you
plan to manage a big number of groups/students be prepared to get a lot of emails!
Consider to implement some mail filtering if you do not wish to change your notification settings.
Your inbox will be flooded.

Solve repeated "Enter passphrase for" with ssh-add /Users/username/.ssh/id_rsa

## Installation & Requirements

pip install -r requirements.txt

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
