import os
import gitlab 
from git import Repo 

_groupIDLength = 5
################################################################################
# HELPER FUNCTIONS (INTERN) 
################################################################################

def _gitlab_entity_exists(gl, what, identifier):
    try:
        if what == "group":
            group = gl.groups.get(identifier)
            return group.path == identifier 
        elif what == "project":
            project = gl.groups.get(identifier)
            return project.name == identifier
    except gitlab.exceptions.GitlabGetError:
        return False

def _get_group_ids_from_pattern(gl, pattern):
    retval = []
    try:
        groups = gl.groups.search(pattern)
        for group in groups:
            retval.append(group.id)
    except gitlab.exceptions.GitlabGetError:
        return retval

    return retval

def _get_user_id_by_mail(gl, mail): 
    users = gl.users.list(search=mail)
    if len(users) > 1:
        raise ValueError("Mailadress %s got more than one match!" % mail)
    elif len(users) == 0:
        raise ValueError("No user with mail %s" % mail)
    else:
      return users[0].id 

def _user_in_group(gl, userID, groupID):
    for member in gl.groups.get(groupID).members.list():
        if member.id == userID:
            return True 
    return False

def _add_users_to_group(gl, userIDs, groupID, accessLevel):
    userAdded = 0
    try:
        group = gl.groups.get(groupID)
    except gitlab.exceptions.GitlabGetError:
        print "Couldn't retrieve group %i" % groupID
        return userAdded

    for userID in userIDs:
        if _user_in_group(gl, userID, groupID): 
            userAdded += 1
            continue
        else:
            try:
                group.members.create({  'user_id': userID,
                'access_level': accessLevel})
                userAdded += 1
            except gitlab.exceptions.GitlabCreateError:
                print "Couldn't add user %s to group %s" % (userID, groupID)
    return userAdded 

def _add_user_to_group(gl, userID, groupID, accessLevel):
    return _add_users_to_group(gl, [userID], groupID, accessLevel)

def _check_groups_in_user_file(mapping):
    if len(mapping) < 1 or len(mapping) > 99999:
        raise ValueError("user file has wrong number of entries: %i" % len(mapping))
    for groupNr in mapping: 
        try:
            int(groupNr)
        except ValueError:
            raise ValueError("groupNr %s is no integer" % groupNr)
            continue
        if int(groupNr) < 1 or int(groupNr) > 99999:
            raise ValueError("groupNr %s is integer out of range (1-99999)" % groupNr)
    return True 

def _add_students_to_group(gl, studentMailAdresses, groupID):
    studentIDs = []
    for ma in studentMailAdresses:
        studentIDs.append(_get_user_id_by_mail(gl, ma))
    _add_users_to_group(gl, studentIDs, groupID, gitlab.DEVELOPER_ACCESS) 

def _get_last_solution(repo, branch, dueDate):
    cur_solution = 0
    for commit in repo.iter_commits(branch): 
        if cur_solution == 0:
            cur_solution = commit.hexsha 
        if commit.committed_date <= dueDate and commit.committed_date > cur_solution:
            cur_solution = commit.hexsha
    return cur_solution

################################################################################
# PUBLIC INTERFACE 
################################################################################

########################################
# check
########################################
def check_users(gl, mapping):
    usersOk = True
    for groupNr in mapping:
        for userMail in mapping[groupNr]:
            try:
                _get_user_id_by_mail(gl, userMail)
            except:
                usersOk = False
    return usersOk

def check_groups(gl, mapping, pattern):
    try:
        groupsOk = _check_groups_in_user_file(mapping)
    except ValueError:
        print "Check of user file was not successful!"
        return False 

    groupIDs = _get_group_ids_from_pattern(gl, pattern) 
    if len(mapping)  != len(groupIDs):
        print "number of groups in gitlab (%i) and user file (%i) don't match" % \
                (len(groupIDs), len(mapping))
        groupsOk = False 
    for groupNr in mapping:
        try:
            int(groupNr)
        except ValueError:
            print "groupNr %s is no integer" % groupNr
            groupOk = False
            continue
        groupName = pattern + groupNr.zfill(_groupIDLength)
        if not _gitlab_entity_exists(gl, 'group', groupName.lower()):
            print "Group %s does not exist!" % groupName
    return groupsOk

########################################
# init
########################################
def init_groups(gl, mapping, pattern, adminMails = []):
    try:
        _check_groups_in_user_file(mapping)
    except:
        return False

    for groupNr in mapping: 
        groupName = pattern + groupNr.zfill(_groupIDLength)
        if not _gitlab_entity_exists(gl, 'group', groupName.lower()):
            try:
                group = gl.groups.create(
                    {
                        'name':  groupName, 
                        'path': groupName.lower(), 
                        'visibility_level': 0
                    }
                )
            except gitlab.exceptions.GitlabCreateError:
                print "Group %s could not be created" % groupName
        else:
            group = gl.groups.search(groupName)[0]
    
        _add_students_to_group(gl, mapping[groupNr], group.id)

        for adminMail in adminMails:
            try:
                adminID = _get_user_id_by_mail(gl, adminMail)
                if not _user_in_group(gl, adminID, group.id):
                    _add_user_to_group(
                        gl,
                        adminID, 
                        group.id,
                        gitlab.MASTER_ACCESS
                    )
            except ValueError as e:
                print str(e)

def _add_user_to_project(gl, userID, projectName, accessLevel, groupID): 
    group = gl.groups.get(groupID)
    if projectName in map(lambda x: x.name, group.projects.list()):
        if len(group.projects.list(search = projectName)) > 1:
            raise ValueError("Search for %s returns more than one project in %s" % \
                (projectName, group.name))
        projectInGroup = group.projects.list(search = projectName)[0]
        project = gl.projects.get(projectInGroup.id)
        if not userID in map(lambda x: x.id, project.members.list()):
            project.members.create(
                {
                    'user_id': userID,
                    'access_level': accessLevel 
                }
            )
        # else: nothing to do
    else:
        raise ValueError("No project with name %s in group %s" % \
            (projectName, group.name))

########################################
# workflow
########################################
def add_reviewer_to_exercise(gl, reviewerMails, pattern, exercise):
    for reviewerMail in reviewerMails: 
        reviewerID = _get_user_id_by_mail(gl, reviewerMail)
        for groupID in _get_group_ids_from_pattern(gl, pattern):
            _add_user_to_project(
                gl, 
                reviewerID,
                exercise,
                gitlab.REPORTER_ACCESS,
                groupID
            )

def publish_exercise(gl, exercise, groupPattern):
    # see https://gitlab.com/gitlab-org/gitlab-ce/merge_requests/6213
    # until this is merged and released this functionality is not available...
    raise NotImplementedError
    try:
        masterProject = gl.projects.get(masterID)
        groupIDs = _get_group_ids_from_pattern(gl, pattern)
    except gitlab.exceptions.GitlabGetError:
        print "Could not retrieve Master-Project %s or GroupIDs for %s" % exercise, groupPattern
    try:
        for id in groupIDs:
            fork = masterProject.forks.create({'namespace_id': id})
    except gitlab.exceptions.GitlabCreateError:
        print "Could not fork to groups"

def download_solutions(gl, exercise, pattern, downloadDir, dueDate): 
    # create directory for solutions if not existing
    if not os.path.exists(downloadDir):
            os.makedirs(downloadDir)
    for groupID in _get_group_ids_from_pattern(gl, pattern):
        group = gl.groups.get(groupID) 
        if exercise in map(lambda x: x.name, group.projects.list()): 
            project = group.projects.list(search = exercise)[0]
            curSolutionPath = os.path.join(downloadDir, exercise, group.name)
            try:
                if os.path.exists(curSolutionPath):
                    repo = Repo(curSolutionPath)
                    origin = repo.remotes.origin
                    origin.pull()
                else:
                    print "Downloading %s" % project.http_url_to_repo
                    repo = Repo.clone_from(
                        project.ssh_url_to_repo,
                        curSolutionPath, 
                        branch='master') 
                solutionHash = _get_last_solution(repo, 'master', dueDate)
                if solutionHash == 0:
                    # should not happen since publish action was a commit
                    print "group %s does not have a solution!" % group.name
                correct_branch = repo.create_head('correct_branch')
                correct_branch.set_commit(solutionHash) 
            except Exception as e:
                print "Can't download exercise %s for group %s to %s: %s" % \
                        (exercise, group.name, curSolutionPath, str(e))
                continue
        else:
            print "Can't clone/fetch exercise %s for group %s (does not exist)" % \
                    (exercise, group.name)

########################################
# deprov
########################################
def delete_groups(gl, pattern):
    if not len(pattern) > 4:
        print "The string pattern %s is smaller than four chars!" % pattern
        return False
    for groupID in _get_group_ids_from_pattern(gl, pattern):
        print "Deleting Group with ID %s" % groupID
        gl.groups.delete(groupID)
    return True
