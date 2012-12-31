#! /usr/bin/env python

# Kamm - The easiest to-do list manager ever. No kidding!
# github.com/sukhbir/kamm

import os
import sys
import itertools

TASK_FILE = '.kamm'
HOME_DIRECTORY = os.path.expanduser('~') 
FULL_PATH = os.path.join(HOME_DIRECTORY, TASK_FILE)


def save_tasks(task_list, append_list=True):
    """Save the task list to a file."""
    # The file is saved to the user's home directory by default.
    if append_list:
        with open(FULL_PATH, 'a') as f:
            f.write(''.join(task_list))
    else:
        with open(FULL_PATH, 'w') as f:
            f.write(''.join(task_list))

    sys.exit('Saved.')


def delete_task():
    """Deletes all the tasks in the list."""
    tasks = []
    print 'Deleting all tasks.'
    save_tasks(tasks, append_list=False)


def load_task():
    """Loads the tasks from the file and saves them into a dictionary."""
    tasks_complete = {}
    tasks_incomplete = {}
    try:
        with open(FULL_PATH, 'r') as f:
            for line in f:
                task, status = line.strip().split(',')
                # Append the task to the appropriate dictionary. 
                if status == '0':
                    tasks_incomplete[task] = status
                else:
                    tasks_complete[task] = status
    except IOError:
        sys.exit("Error: '.kamm' not found in '{0}'.".format(HOME_DIRECTORY))

    total_tasks = len(tasks_complete) + len(tasks_incomplete)
    if not total_tasks:
        sys.exit('No tasks found.')
    return tasks_complete, tasks_incomplete, total_tasks


def change_task():
    """Change the tasks to mark them as complete or incomplete."""
    tasks_complete, tasks_incomplete, total_tasks = load_task()
    # Merge the two dictionaries.
    tasks = {}
    for task, status in itertools.chain(tasks_complete.iteritems(), 
                                        tasks_incomplete.iteritems()):
        tasks[task] = status
    # A dictionary with all the tasks.
    all_tasks = dict(enumerate(tasks, 1))

    print ''
    for (count, task), status in zip(enumerate(tasks, 1), tasks.itervalues()):
        if status == '0':
            print '{0}. [ ] {1}'.format(count, task)
        else:
            print '{0}. [X] {1}'.format(count, task)
    print ''

    prompt = "Select task to change (1 - {0}), 0 to quit: ".format(total_tasks)
    while True:
        try:
            option = int(raw_input(prompt))
        except ValueError: 
            print '(please enter a number)'
            continue
        if option == 0:
            break
        if option not in range(1, total_tasks+1):
            print '(invalid task selected)'
            continue
        selected_task = all_tasks[option]
        task_status = tasks[selected_task]
        if task_status == '0':
            print "Marked '{0}' as 'complete'.".format(selected_task)
            tasks[selected_task] = '1'
        else:
            print "Marked '{0}' as 'incomplete'.".format(selected_task)
            tasks[selected_task] = '0'

    task_list = []
    for task, status in tasks.iteritems():
        task_list.append(task + ',' + status)
        task_list.append('\n')
    # Save the task list by calling save_tasks.
    save_tasks(task_list, append_list=False)


def show_task():
    """Show all the saved tasks."""
    tasks_complete, tasks_incomplete, total_tasks = load_task()
    # In case you want to change how completed/ incompleted tasks are shown,
    # modify the print statement in the following code.
    print ''
    for task, status in tasks_incomplete.iteritems():
        print '[ ] {0}'.format(task)
    for task, status in tasks_complete.iteritems():
        print '[X] {0}'.format(task)
    print ''

    len_complete = len(tasks_complete)
    print '{0} tasks ({1} incomplete, {2} complete)'.format(total_tasks,
                                                        total_tasks-len_complete,
                                                        len_complete)
    sys.exit()


def add_task():
    """Adds a task to the to-do list."""
    print "Enter each to-do on a newline, '.' to quit: "

    tasks = []
    count = 1
    while True:
        task_input = raw_input('{0}. '.format(count))
        if not task_input:
            print '(please enter a task)'
            continue
        if task_input == '.':
            break
        # We can't allow a ',' so we replace it.
        if ',' in task_input:
            task_input = task_input.replace(',', ':')
        # 0 signifies an incomplete task.
        tasks.append(task_input + ',' + '0')
        tasks.append('\n')
        count += 1

    if not tasks:
        sys.exit('Nothing to save.')
    save_tasks(tasks)


if __name__ == '__main__':
    usage_message = """Usage: kmm.py [options]
Options:
    -a      Add tasks
    -s      Show all tasks
    -c      Change tasks
    -d      Delete all tasks"""

    if len(sys.argv) < 2:
        sys.exit(usage_message)

    option = sys.argv[1]
    if option == '-a':
        add_task()
    elif option == '-s':
        show_task()
    elif option == '-c':
        change_task()
    elif option == '-d':
        delete_task()
    else:
        print 'No such option.\n'
        sys.exit(usage_message)
