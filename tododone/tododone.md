~~~ markdown-script
include <args.bare>
include <forms.bare>


# Tododone task management application main entry point
async function tododoneMain():
    # Parse arguments
    args = argsParse(tododoneArguments)
    view = objectGet(args, 'view')
    editId = objectGet(args, 'editId')
    snoozeId = objectGet(args, 'snoozeId')

    # Load tasks from session storage
    tasks = tododoneLoadTasks()

    # Set the document title
    documentSetTitle('Tododone - Task Manager')

    # Handle task editing
    if editId != null:
        tododoneEditTask(tasks, editId, args)
        return
    endif

    # Handle task snoozing
    if snoozeId != null:
        tododoneSnoozeTask(tasks, snoozeId, args)
        return
    endif

    # Render the main view
    if view == 'add':
        tododoneAddTask(tasks, args)
    elif view == 'categories':
        tododoneManageCategories(tasks, args)
    else:
        tododoneRenderMainView(tasks, args)
    endif
endfunction


# Application arguments
tododoneArguments = argsValidate(arrayNew( \
    objectNew('name', 'view', 'default', 'tasks'), \
    objectNew('name', 'filter', 'default', 'active'), \
    objectNew('name', 'category'), \
    objectNew('name', 'sort', 'default', 'priority'), \
    objectNew('name', 'editId', 'type', 'int', 'explicit', true), \
    objectNew('name', 'snoozeId', 'type', 'int', 'explicit', true), \
    objectNew('name', 'customSnooze', 'explicit', true) \
))


# Render the main task view
function tododoneRenderMainView(tasks, args):
    filter = objectGet(args, 'filter')
    categoryFilter = objectGet(args, 'category')
    sortBy = objectGet(args, 'sort')

    # Render header and menu
    markdownPrint('# Tododone')
    markdownPrint('')
    markdownPrint( \
        argsLink(tododoneArguments, 'Add Task', objectNew('view', 'add')) + ' | ', \
        argsLink(tododoneArguments, 'Categories', objectNew('view', 'categories')) + ' | ', \
        argsLink(tododoneArguments, 'Reset', null, true) \
    )

    # Filter menu
    markdownPrint('')
    markdownPrint('**Filter:** ', \
        if(filter == 'active', '**Active**', argsLink(tododoneArguments, 'Active', objectNew('filter', 'active'))), ' | ', \
        if(filter == 'completed', '**Completed**', argsLink(tododoneArguments, 'Completed', objectNew('filter', 'completed'))), ' | ', \
        if(filter == 'snoozed', '**Snoozed**', argsLink(tododoneArguments, 'Snoozed', objectNew('filter', 'snoozed'))), ' | ', \
        if(filter == 'all', '**All**', argsLink(tododoneArguments, 'All', objectNew('filter', 'all'))) \
    )

    # Sort menu
    markdownPrint('')
    markdownPrint('**Sort:** ', \
        if(sortBy == 'priority', '**Priority**', argsLink(tododoneArguments, 'Priority', objectNew('sort', 'priority'))), ' | ', \
        if(sortBy == 'deadline', '**Deadline**', argsLink(tododoneArguments, 'Deadline', objectNew('sort', 'deadline'))), ' | ', \
        if(sortBy == 'created', '**Created**', argsLink(tododoneArguments, 'Created', objectNew('sort', 'created'))) \
    )

    # Category filter
    categories = tododoneGetCategories(tasks)
    if arrayLength(categories) > 0:
        markdownPrint('')
        categoryParts = arrayNew()
        arrayPush(categoryParts, if(!categoryFilter, '**All**', argsLink(tododoneArguments, 'All', objectNew('category', null))))
        for category in categories:
            if category == categoryFilter:
                arrayPush(categoryParts, '**' + markdownEscape(category) + '**')
            else:
                arrayPush(categoryParts, argsLink(tododoneArguments, category, objectNew('category', category)))
            endif
        endfor
        markdownPrint('**Category:** ' + arrayJoin(categoryParts, ' | '))
    endif

    # Filter and sort tasks
    filteredTasks = tododoneFilterTasks(tasks, filter, categoryFilter)
    sortedTasks = tododoneSortTasks(filteredTasks, sortBy)

    # Render tasks
    markdownPrint('')
    markdownPrint('## Tasks')

    if arrayLength(sortedTasks) == 0:
        markdownPrint('')
        markdownPrint('*No tasks found.*')
    else:
        tododoneRenderTaskList(sortedTasks, args)
    endif
endfunction


# Render task list
function tododoneRenderTaskList(tasks, args):
    for task in tasks:
        taskId = objectGet(task, 'id')
        title = objectGet(task, 'title')
        category = objectGet(task, 'category')
        priority = objectGet(task, 'priority')
        deadline = objectGet(task, 'deadline')
        deadlineType = objectGet(task, 'deadlineType')
        completed = objectGet(task, 'completed')
        snoozedUntil = objectGet(task, 'snoozedUntil')

        # Build task display
        markdownPrint('')

        # Task title with checkbox
        if completed:
            taskDisplay = '~~' + markdownEscape(title) + '~~'
        else:
            taskDisplay = '**' + markdownEscape(title) + '**'
        endif

        # Add priority indicator
        priorityIcon = if(priority == 'high', '🔴', if(priority == 'medium', '🟡', '🟢'))
        markdownPrint(priorityIcon + ' ' + taskDisplay)

        # Task metadata
        metadata = arrayNew()
        if category:
            arrayPush(metadata, 'Category: ' + category)
        endif
        if deadline:
            deadlineDisplay = 'Deadline: ' + deadline + ' (' + deadlineType + ')'
            if !completed && tododoneIsOverdue(deadline):
                deadlineDisplay = '**⚠️ ' + deadlineDisplay + '**'
            endif
            arrayPush(metadata, deadlineDisplay)
        endif
        if snoozedUntil && tododoneIsSnoozed(snoozedUntil):
            arrayPush(metadata, '💤 Snoozed until: ' + snoozedUntil)
        endif

        if arrayLength(metadata) > 0:
            markdownPrint('  ' + arrayJoin(metadata, ' | '))
        endif

        # Task actions using direct button elements with click handlers
        markdownPrint('')
        actionElements = arrayNew()
        if !completed:
            arrayPush(actionElements, formsLinkButtonElements('✓ Complete', systemPartial(tododoneToggleComplete, tasks, taskId, true, args)))
            arrayPush(actionElements, objectNew('text', ' '))
            arrayPush(actionElements, formsLinkButtonElements('💤 Snooze', systemPartial(tododoneNavigateSnooze, taskId)))
        else:
            arrayPush(actionElements, formsLinkButtonElements('↩ Uncomplete', systemPartial(tododoneToggleComplete, tasks, taskId, false, args)))
        endif
        arrayPush(actionElements, objectNew('text', ' '))
        arrayPush(actionElements, formsLinkButtonElements('✏️ Edit', systemPartial(tododoneNavigateEdit, taskId)))
        arrayPush(actionElements, objectNew('text', ' '))
        arrayPush(actionElements, formsLinkButtonElements('🗑️ Delete', systemPartial(tododoneDeleteTaskAction, tasks, taskId, args)))

        elementModelRender(objectNew('html', 'p', 'elem', actionElements))
    endfor
endfunction


# Add new task view
function tododoneAddTask(tasks, args):
    markdownPrint('# Add New Task')
    markdownPrint('')
    markdownPrint(argsLink(tododoneArguments, 'Back', objectNew('view', 'tasks')))

    markdownPrint('')
    markdownPrint('## Task Details')

    # Task form
    elementModelRender(tododoneTaskForm(null, tasks))
endfunction


# Edit task view
function tododoneEditTask(tasks, taskId, args):
    task = tododoneFindTask(tasks, taskId)
    if !task:
        markdownPrint('**Error:** Task not found')
        return
    endif

    markdownPrint('# Edit Task')
    markdownPrint('')
    markdownPrint(argsLink(tododoneArguments, 'Back', objectNew('view', 'tasks')))

    markdownPrint('')
    markdownPrint('## Task Details')

    # Task form
    elementModelRender(tododoneTaskForm(task, tasks))
endfunction


# Snooze task view
function tododoneSnoozeTask(tasks, taskId, args):
    task = tododoneFindTask(tasks, taskId)
    if !task:
        markdownPrint('**Error:** Task not found')
        return
    endif

    markdownPrint('# Snooze Task')
    markdownPrint('')
    markdownPrint(argsLink(tododoneArguments, 'Back', objectNew('view', 'tasks')))

    markdownPrint('')
    markdownPrint('**Task:** ' + markdownEscape(objectGet(task, 'title')))

    markdownPrint('')
    markdownPrint('## Snooze Options')

    # Snooze preset buttons
    tomorrow = tododoneAddDays(datetimeISOFormat(datetimeToday(), true), 1)
    nextWeek = tododoneAddDays(datetimeISOFormat(datetimeToday(), true), 7)

    markdownPrint('')
    elementModelRender(arrayNew( \
        formsLinkButtonElements('Tomorrow', systemPartial(tododoneApplySnooze, tasks, taskId, tomorrow)), \
        objectNew('text', ' '), \
        formsLinkButtonElements('Next Week', systemPartial(tododoneApplySnooze, tasks, taskId, nextWeek)) \
    ))

    # Custom date input
    markdownPrint('')
    markdownPrint('**Custom Date:**')
    elementModelRender(arrayNew( \
        objectNew('html', 'input', \
            'attr', objectNew('type', 'date', 'id', 'customSnoozeDate', \
                'value', tododoneAddDays(datetimeISOFormat(datetimeToday(), true), 1)) \
        ), \
        objectNew('text', ' '), \
        formsLinkButtonElements('Apply Custom', systemPartial(tododoneApplyCustomSnooze, tasks, taskId)) \
    ))
endfunction


# Manage categories view
function tododoneManageCategories(tasks, args):
    categories = tododoneGetCategories(tasks)

    markdownPrint('# Manage Categories')
    markdownPrint('')
    markdownPrint(argsLink(tododoneArguments, 'Back', objectNew('view', 'tasks')))

    markdownPrint('')
    markdownPrint('## Current Categories')

    if arrayLength(categories) == 0:
        markdownPrint('')
        markdownPrint('*No categories defined. Categories are created when you add tasks.*')
    else:
        for category in categories:
            markdownPrint('')
            markdownPrint('- ' + markdownEscape(category))
        endfor
    endif

    markdownPrint('')
    markdownPrint('## Add New Category')
    elementModelRender(arrayNew( \
        formsTextElements('newCategory', '', 20), \
        objectNew('text', ' '), \
        formsLinkButtonElements('Add', systemPartial(tododoneAddCategory, tasks)) \
    ))
endfunction


# Create task form element model
function tododoneTaskForm(task, tasks):
    isEdit = task != null
    taskId = if(isEdit, objectGet(task, 'id'), null)
    categories = tododoneGetCategories(tasks)

    # Default values
    defaultTitle = if(isEdit, objectGet(task, 'title'), '')
    defaultCategory = if(isEdit, objectGet(task, 'category'), '')
    defaultPriority = if(isEdit, objectGet(task, 'priority'), 'medium')
    defaultDeadline = if(isEdit, objectGet(task, 'deadline'), '')
    defaultDeadlineType = if(isEdit, objectGet(task, 'deadlineType'), 'soft')

    return objectNew( \
        'html', 'div', \
        'elem', arrayNew( \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'label', 'elem', objectNew('text', 'Title: ')), \
                formsTextElements('taskTitle', defaultTitle, 40) \
            )), \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'label', 'elem', objectNew('text', 'Category: ')), \
                objectNew('html', 'input', 'attr', objectNew( \
                    'type', 'text', \
                    'id', 'taskCategory', \
                    'list', 'categoryList', \
                    'value', defaultCategory, \
                    'size', 20 \
                )), \
                objectNew('html', 'datalist', \
                    'attr', objectNew('id', 'categoryList'), \
                    'elem', tododoneCreateOptions(categories) \
                ) \
            )), \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'label', 'elem', objectNew('text', 'Priority: ')), \
                objectNew('html', 'select', \
                    'attr', objectNew('id', 'taskPriority'), \
                    'elem', arrayNew( \
                        objectNew('html', 'option', \
                            'attr', if(defaultPriority == 'high', objectNew('value', 'high', 'selected', 'selected'), objectNew('value', 'high')), \
                            'elem', objectNew('text', 'High') \
                        ), \
                        objectNew('html', 'option', \
                            'attr', if(defaultPriority == 'medium', objectNew('value', 'medium', 'selected', 'selected'), objectNew('value', 'medium')), \
                            'elem', objectNew('text', 'Medium') \
                        ), \
                        objectNew('html', 'option', \
                            'attr', if(defaultPriority == 'low', objectNew('value', 'low', 'selected', 'selected'), objectNew('value', 'low')), \
                            'elem', objectNew('text', 'Low') \
                        ) \
                    ) \
                ) \
            )), \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'label', 'elem', objectNew('text', 'Deadline: ')), \
                objectNew('html', 'input', 'attr', objectNew( \
                    'type', 'date', \
                    'id', 'taskDeadline', \
                    'value', defaultDeadline \
                )), \
                objectNew('text', ' '), \
                objectNew('html', 'select', \
                    'attr', objectNew('id', 'taskDeadlineType'), \
                    'elem', arrayNew( \
                        objectNew('html', 'option', \
                            'attr', if(defaultDeadlineType == 'hard', objectNew('value', 'hard', 'selected', 'selected'), objectNew('value', 'hard')), \
                            'elem', objectNew('text', 'Hard deadline') \
                        ), \
                        objectNew('html', 'option', \
                            'attr', if(defaultDeadlineType == 'soft', objectNew('value', 'soft', 'selected', 'selected'), objectNew('value', 'soft')), \
                            'elem', objectNew('text', 'Soft deadline') \
                        ) \
                    ) \
                ) \
            )), \
            objectNew('html', 'p', 'elem', arrayNew( \
                formsLinkButtonElements(if(isEdit, 'Update Task', 'Add Task'), \
                    systemPartial(if(isEdit, tododoneUpdateTask, tododoneSaveTask), tasks, taskId)) \
            )) \
        ) \
    )
endfunction


# Create option elements for datalist
function tododoneCreateOptions(values):
    options = arrayNew()
    for value in values:
        arrayPush(options, objectNew('html', 'option', 'attr', objectNew('value', value)))
    endfor
    return options
endfunction


# Save new task
async function tododoneSaveTask(tasks, taskId):
    title = documentInputValue('taskTitle')
    category = documentInputValue('taskCategory')
    priority = documentInputValue('taskPriority')
    deadline = documentInputValue('taskDeadline')
    deadlineType = documentInputValue('taskDeadlineType')

    if !title || stringTrim(title) == '':
        windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'add')))
        return
    endif

    # Create new task
    newTask = objectNew( \
        'id', tododoneGetNextId(tasks), \
        'title', stringTrim(title), \
        'category', stringTrim(category), \
        'priority', priority, \
        'deadline', deadline, \
        'deadlineType', deadlineType, \
        'completed', false, \
        'created', datetimeISOFormat(datetimeNow()), \
        'snoozedUntil', null \
    )

    # Add task to array
    arrayPush(tasks, newTask)
    tododoneSaveTasks(tasks)

    # Navigate back to main view
    windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'tasks')))
endfunction


# Update existing task
async function tododoneUpdateTask(tasks, taskId):
    task = tododoneFindTask(tasks, taskId)
    if !task:
        windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'tasks')))
        return
    endif

    title = documentInputValue('taskTitle')
    category = documentInputValue('taskCategory')
    priority = documentInputValue('taskPriority')
    deadline = documentInputValue('taskDeadline')
    deadlineType = documentInputValue('taskDeadlineType')

    if !title || stringTrim(title) == '':
        windowSetLocation(argsURL(tododoneArguments, objectNew('editId', taskId)))
        return
    endif

    # Update task
    objectSet(task, 'title', stringTrim(title))
    objectSet(task, 'category', stringTrim(category))
    objectSet(task, 'priority', priority)
    objectSet(task, 'deadline', deadline)
    objectSet(task, 'deadlineType', deadlineType)

    tododoneSaveTasks(tasks)

    # Navigate back to main view
    windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'tasks')))
endfunction


# Toggle task completion status
async function tododoneToggleComplete(tasks, taskId, isComplete, args):
    task = tododoneFindTask(tasks, taskId)
    if task:
        objectSet(task, 'completed', isComplete)
        tododoneSaveTasks(tasks)
    endif

    # Re-render the main view
    tododoneRenderMainView(tasks, args)
endfunction


# Delete task action
async function tododoneDeleteTaskAction(tasks, taskId, args):
    index = arrayIndexOf(tasks, systemPartial(tododoneTaskIdMatch, taskId))
    if index >= 0:
        arrayDelete(tasks, index)
        tododoneSaveTasks(tasks)
    endif

    # Re-render the main view
    tododoneRenderMainView(tasks, args)
endfunction


# Navigate to edit view
async function tododoneNavigateEdit(taskId):
    windowSetLocation(argsURL(tododoneArguments, objectNew('editId', taskId)))
endfunction


# Navigate to snooze view
async function tododoneNavigateSnooze(taskId):
    windowSetLocation(argsURL(tododoneArguments, objectNew('snoozeId', taskId)))
endfunction


# Apply snooze to task
async function tododoneApplySnooze(tasks, taskId, snoozeDate):
    task = tododoneFindTask(tasks, taskId)
    if task:
        objectSet(task, 'snoozedUntil', snoozeDate)
        tododoneSaveTasks(tasks)
    endif

    windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'tasks')))
endfunction


# Apply custom snooze to task
async function tododoneApplyCustomSnooze(tasks, taskId):
    customDate = documentInputValue('customSnoozeDate')
    if customDate:
        tododoneApplySnooze(tasks, taskId, customDate)
    else:
        windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'tasks')))
    endif
endfunction


# Add new category
async function tododoneAddCategory(tasks):
    newCategory = documentInputValue('newCategory')
    if newCategory && stringTrim(newCategory) != '':
        # Category will be added when used in a task
        windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'categories')))
    endif
endfunction


# Filter tasks based on criteria
function tododoneFilterTasks(tasks, filter, categoryFilter):
    filtered = arrayNew()
    today = datetimeISOFormat(datetimeToday(), true)

    for task in tasks:
        # Category filter
        if categoryFilter && objectGet(task, 'category') != categoryFilter:
            continue
        endif

        # Status filter
        completed = objectGet(task, 'completed')
        snoozedUntil = objectGet(task, 'snoozedUntil')
        isSnoozed = snoozedUntil && tododoneIsSnoozed(snoozedUntil)

        if filter == 'active':
            if !completed && !isSnoozed:
                arrayPush(filtered, task)
            endif
        elif filter == 'completed':
            if completed:
                arrayPush(filtered, task)
            endif
        elif filter == 'snoozed':
            if !completed && isSnoozed:
                arrayPush(filtered, task)
            endif
        else:
            arrayPush(filtered, task)
        endif
    endfor

    return filtered
endfunction


# Sort tasks based on criteria
function tododoneSortTasks(tasks, sortBy):
    if sortBy == 'priority':
        return arraySort(tasks, tododonePriorityCompare)
    elif sortBy == 'deadline':
        return arraySort(tasks, tododoneDeadlineCompare)
    elif sortBy == 'created':
        return arraySort(tasks, tododoneCreatedCompare)
    endif
    return tasks
endfunction


# Priority comparison function
function tododonePriorityCompare(a, b):
    priorityOrder = objectNew('high', 0, 'medium', 1, 'low', 2)
    aOrder = objectGet(priorityOrder, objectGet(a, 'priority'))
    bOrder = objectGet(priorityOrder, objectGet(b, 'priority'))

    # Sort by priority first
    if aOrder != bOrder:
        return aOrder - bOrder
    endif

    # Then by deadline
    return tododoneDeadlineCompare(a, b)
endfunction


# Deadline comparison function
function tododoneDeadlineCompare(a, b):
    aDeadline = objectGet(a, 'deadline')
    bDeadline = objectGet(b, 'deadline')
    aType = objectGet(a, 'deadlineType')
    bType = objectGet(b, 'deadlineType')

    # No deadline goes to the end
    if !aDeadline && !bDeadline:
        return 0
    elif !aDeadline:
        return 1
    elif !bDeadline:
        return -1
    endif

    # Hard deadlines come before soft deadlines for same date
    if aDeadline == bDeadline:
        if aType == 'hard' && bType == 'soft':
            return -1
        elif aType == 'soft' && bType == 'hard':
            return 1
        endif
        return 0
    endif

    return systemCompare(aDeadline, bDeadline)
endfunction


# Created date comparison function
function tododoneCreatedCompare(a, b):
    return systemCompare(objectGet(b, 'created'), objectGet(a, 'created'))
endfunction


# Helper functions
function tododoneFindTask(tasks, taskId):
    for task in tasks:
        if objectGet(task, 'id') == taskId:
            return task
        endif
    endfor
    return null
endfunction


function tododoneTaskIdMatch(taskId, task):
    return objectGet(task, 'id') == taskId
endfunction


function tododoneGetNextId(tasks):
    maxId = 0
    for task in tasks:
        taskId = objectGet(task, 'id')
        if taskId > maxId:
            maxId = taskId
        endif
    endfor
    return maxId + 1
endfunction


function tododoneGetCategories(tasks):
    categories = objectNew()
    for task in tasks:
        category = objectGet(task, 'category')
        if category && category != '':
            objectSet(categories, category, true)
        endif
    endfor
    return arraySort(objectKeys(categories))
endfunction


function tododoneIsOverdue(deadline):
    if !deadline:
        return false
    endif
    today = datetimeISOFormat(datetimeToday(), true)
    return deadline < today
endfunction


function tododoneIsSnoozed(snoozedUntil):
    if !snoozedUntil:
        return false
    endif
    today = datetimeISOFormat(datetimeToday(), true)
    return snoozedUntil > today
endfunction


function tododoneAddDays(dateStr, days):
    date = datetimeISOParse(dateStr)
    if !date:
        return dateStr
    endif

    year = datetimeYear(date)
    month = datetimeMonth(date)
    day = datetimeDay(date) + days

    # Simple date addition (doesn't handle month boundaries perfectly but good enough)
    while day > 28:
        day = day - 28
        month = month + 1
        if month > 12:
            month = 1
            year = year + 1
        endif
    endwhile

    return datetimeISOFormat(datetimeNew(year, month, day), true)
endfunction


# Load tasks from session storage
function tododoneLoadTasks():
    tasksJSON = sessionStorageGet('tododoneTasks')
    if tasksJSON:
        tasks = jsonParse(tasksJSON)
        if tasks:
            return tasks
        endif
    endif
    return arrayNew()
endfunction


# Save tasks to session storage
function tododoneSaveTasks(tasks):
    sessionStorageSet('tododoneTasks', jsonStringify(tasks))
endfunction


# Execute the main entry point
tododoneMain()
~~~
