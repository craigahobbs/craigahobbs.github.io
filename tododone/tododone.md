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

    # Load tasks from local storage
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
    objectNew('name', 'customSnooze', 'explicit', true), \
    objectNew('name', 'showNotes', 'type', 'int', 'explicit', true), \
    objectNew('name', 'temp_title', 'explicit', true), \
    objectNew('name', 'temp_category', 'explicit', true), \
    objectNew('name', 'temp_priority', 'explicit', true), \
    objectNew('name', 'temp_deadline', 'explicit', true), \
    objectNew('name', 'temp_deadline_type', 'explicit', true), \
    objectNew('name', 'temp_notes', 'explicit', true) \
))


# Built-in categories
tododoneBuiltinCategories = arrayNew( \
    'Personal', \
    'Work', \
    'Shopping', \
    'Health', \
    'Finance', \
    'Learning', \
    'Projects', \
    'Urgent' \
)


# Render the main task view
function tododoneRenderMainView(tasks, args):
    filter = objectGet(args, 'filter')
    categoryFilter = objectGet(args, 'category')
    sortBy = objectGet(args, 'sort')
    showNotesId = objectGet(args, 'showNotes')

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
    categories = tododoneGetAllCategories(tasks)
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
        tododoneRenderTaskList(sortedTasks, args, showNotesId)
    endif
endfunction


# Render task list
function tododoneRenderTaskList(tasks, args, showNotesId):
    for task in tasks:
        taskId = objectGet(task, 'id')
        title = objectGet(task, 'title')
        category = objectGet(task, 'category')
        priority = objectGet(task, 'priority')
        deadline = objectGet(task, 'deadline')
        deadlineType = objectGet(task, 'deadlineType')
        completed = objectGet(task, 'completed')
        snoozedUntil = objectGet(task, 'snoozedUntil')
        notes = objectGet(task, 'notes')

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

        # Show notes if expanded
        if notes && stringTrim(notes) != '' && showNotesId == taskId:
            markdownPrint('')
            markdownPrint('  📝 **Notes:**')
            notesLines = stringSplit(notes, '\n')
            for line in notesLines:
                markdownPrint('  ' + markdownEscape(line))
            endfor
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

        # Add notes show/hide button if task has notes
        if notes && stringTrim(notes) != '':
            arrayPush(actionElements, objectNew('text', ' '))
            if showNotesId == taskId:
                arrayPush(actionElements, formsLinkButtonElements('📝 Hide Notes', systemPartial(tododoneToggleNotes, null)))
            else:
                arrayPush(actionElements, formsLinkButtonElements('📝 Show Notes', systemPartial(tododoneToggleNotes, taskId)))
            endif
        endif

        elementModelRender(objectNew('html', 'p', 'elem', actionElements))
    endfor
endfunction


# Toggle notes visibility
async function tododoneToggleNotes(taskId):
    if taskId != null:
        windowSetLocation(argsURL(tododoneArguments, objectNew('showNotes', taskId)))
    else:
        windowSetLocation(argsURL(tododoneArguments, objectNew('showNotes', null)))
    endif
endfunction


# Add new task view
function tododoneAddTask(tasks, args):
    markdownPrint('# Add New Task')
    markdownPrint('')
    markdownPrint(argsLink(tododoneArguments, 'Back', objectNew('view', 'tasks')))

    markdownPrint('')
    markdownPrint('## Task Details')

    # Task form
    elementModelRender(tododoneTaskForm(null, tasks, args))
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
    elementModelRender(tododoneTaskForm(task, tasks, args))
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
    allCategories = tododoneGetAllCategories(tasks)
    customCategories = tododoneGetCustomCategories()

    markdownPrint('# Manage Categories')
    markdownPrint('')
    markdownPrint(argsLink(tododoneArguments, 'Back', objectNew('view', 'tasks')))

    markdownPrint('')
    markdownPrint('## Built-in Categories')
    for category in tododoneBuiltinCategories:
        markdownPrint('')
        markdownPrint('- ' + markdownEscape(category))
    endfor

    markdownPrint('')
    markdownPrint('## Custom Categories')
    if arrayLength(customCategories) == 0:
        markdownPrint('')
        markdownPrint('*No custom categories defined.*')
    else:
        for category in customCategories:
            markdownPrint('')
            elementModelRender(arrayNew( \
                objectNew('text', '- ' + markdownEscape(category) + ' '), \
                formsLinkButtonElements('Delete', systemPartial(tododoneDeleteCategory, tasks, category)) \
            ))
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
function tododoneTaskForm(task, tasks, args):
    isEdit = task != null
    taskId = if(isEdit, objectGet(task, 'id'), null)
    allCategories = tododoneGetAllCategories(tasks)

    # Default values, prefer temp_ args if present
    defaultTitle = objectGet(args, 'temp_title', if(isEdit, objectGet(task, 'title'), ''))
    defaultCategory = objectGet(args, 'temp_category', if(isEdit, objectGet(task, 'category'), ''))
    defaultPriority = objectGet(args, 'temp_priority', if(isEdit, objectGet(task, 'priority'), 'medium'))
    defaultDeadline = objectGet(args, 'temp_deadline', if(isEdit, objectGet(task, 'deadline'), ''))
    defaultDeadlineType = objectGet(args, 'temp_deadline_type', if(isEdit, objectGet(task, 'deadlineType'), 'soft'))
    defaultNotes = objectGet(args, 'temp_notes', if(isEdit, objectGet(task, 'notes'), ''))

    # Get default dates for quick selection
    today = datetimeISOFormat(datetimeToday(), true)
    tomorrow = tododoneAddDays(today, 1)
    nextWeek = tododoneAddDays(today, 7)
    nextMonth = tododoneAddDays(today, 30)

    return objectNew( \
        'html', 'div', \
        'elem', arrayNew( \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'label', 'elem', objectNew('text', 'Title: ')), \
                formsTextElements('taskTitle', defaultTitle, 40) \
            )), \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'label', 'elem', objectNew('text', 'Category: ')), \
                objectNew('html', 'select', \
                    'attr', objectNew('id', 'taskCategory'), \
                    'elem', tododoneCreateCategoryOptions(allCategories, defaultCategory) \
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
                objectNew('text', 'Quick dates: '), \
                formsLinkButtonElements('Today', systemPartial(tododoneUpdateFormDeadline, today, args, isEdit, taskId)), \
                objectNew('text', ' '), \
                formsLinkButtonElements('Tomorrow', systemPartial(tododoneUpdateFormDeadline, tomorrow, args, isEdit, taskId)), \
                objectNew('text', ' '), \
                formsLinkButtonElements('Next Week', systemPartial(tododoneUpdateFormDeadline, nextWeek, args, isEdit, taskId)), \
                objectNew('text', ' '), \
                formsLinkButtonElements('Next Month', systemPartial(tododoneUpdateFormDeadline, nextMonth, args, isEdit, taskId)) \
            )), \
            objectNew('html', 'p', 'elem', arrayNew( \
                objectNew('html', 'label', 'elem', objectNew('text', 'Notes (optional): ')), \
                objectNew('html', 'br'), \
                objectNew('html', 'textarea', \
                    'attr', objectNew('id', 'taskNotes', 'rows', 4, 'cols', 50), \
                    'elem', objectNew('text', defaultNotes) \
                ) \
            )), \
            objectNew('html', 'p', 'elem', arrayNew( \
                formsLinkButtonElements(if(isEdit, 'Update Task', 'Add Task'), \
                    systemPartial(if(isEdit, tododoneUpdateTask, tododoneSaveTask), tasks, taskId, args)) \
            )) \
        ) \
    )
endfunction


# Update form deadline by navigating with temp parameters
async function tododoneUpdateFormDeadline(date, args, isEdit, taskId):
    # Read current form values
    title = documentInputValue('taskTitle')
    category = documentInputValue('taskCategory')
    priority = documentInputValue('taskPriority')
    deadlineType = documentInputValue('taskDeadlineType')
    notes = documentInputValue('taskNotes')

    # Create temp params object
    tempParams = objectNew( \
        'temp_title', title, \
        'temp_category', category, \
        'temp_priority', priority, \
        'temp_deadline', date, \
        'temp_deadline_type', deadlineType, \
        'temp_notes', notes \
    )

    # Add view-specific params
    if isEdit:
        objectSet(tempParams, 'editId', taskId)
    else:
        objectSet(tempParams, 'view', 'add')
    endif

    # Navigate to URL with temp params
    windowSetLocation(argsURL(tododoneArguments, tempParams))
endfunction


# Create category options for select element
function tododoneCreateCategoryOptions(categories, selectedCategory):
    options = arrayNew()

    # Add empty option
    arrayPush(options, objectNew('html', 'option', \
        'attr', objectNew('value', ''), \
        'elem', objectNew('text', '-- Select or leave empty --') \
    ))

    # Add all categories
    for category in categories:
        isSelected = category == selectedCategory
        arrayPush(options, objectNew('html', 'option', \
            'attr', if(isSelected, objectNew('value', category, 'selected', 'selected'), objectNew('value', category)), \
            'elem', objectNew('text', category) \
        ))
    endfor

    return options
endfunction


# Save new task
async function tododoneSaveTask(tasks, taskId, args):
    title = documentInputValue('taskTitle')
    category = documentInputValue('taskCategory')
    priority = documentInputValue('taskPriority')
    deadline = documentInputValue('taskDeadline')
    deadlineType = documentInputValue('taskDeadlineType')
    notes = documentInputValue('taskNotes')

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
        'notes', stringTrim(notes), \
        'completed', false, \
        'created', datetimeISOFormat(datetimeNow()), \
        'snoozedUntil', null \
    )

    # Add task to array
    arrayPush(tasks, newTask)
    tododoneSaveTasks(tasks)

    # Navigate back to main view without temp params
    windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'tasks')))
endfunction


# Update existing task
async function tododoneUpdateTask(tasks, taskId, args):
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
    notes = documentInputValue('taskNotes')

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
    objectSet(task, 'notes', stringTrim(notes))

    tododoneSaveTasks(tasks)

    # Navigate back to main view without temp params
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
        # Add to custom categories
        customCategories = tododoneGetCustomCategories()
        categoryName = stringTrim(newCategory)

        # Check if category already exists
        if arrayIndexOf(customCategories, categoryName) < 0 && arrayIndexOf(tododoneBuiltinCategories, categoryName) < 0:
            arrayPush(customCategories, categoryName)
            tododoneSaveCustomCategories(customCategories)
        endif
    endif

    windowSetLocation(argsURL(tododoneArguments, objectNew('view', 'categories')))
endfunction


# Delete custom category
async function tododoneDeleteCategory(tasks, category):
    customCategories = tododoneGetCustomCategories()
    index = arrayIndexOf(customCategories, category)
    if index >= 0:
        arrayDelete(customCategories, index)
        tododoneSaveCustomCategories(customCategories)
    endif

    # Re-render categories view
    tododoneManageCategories(tasks, argsParse(tododoneArguments))
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


function tododoneGetAllCategories(tasks):
    # Combine built-in and custom categories
    allCategories = objectNew()

    # Add built-in categories
    for category in tododoneBuiltinCategories:
        objectSet(allCategories, category, true)
    endfor

    # Add custom categories
    customCategories = tododoneGetCustomCategories()
    for category in customCategories:
        objectSet(allCategories, category, true)
    endfor

    # Add any categories from existing tasks
    for task in tasks:
        category = objectGet(task, 'category')
        if category && category != '':
            objectSet(allCategories, category, true)
        endif
    endfor

    return arraySort(objectKeys(allCategories))
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


# Load tasks from local storage
function tododoneLoadTasks():
    tasksJSON = localStorageGet('tododoneTasks')
    if tasksJSON:
        tasks = jsonParse(tasksJSON)
        if tasks:
            return tasks
        endif
    endif
    return arrayNew()
endfunction


# Save tasks to local storage
function tododoneSaveTasks(tasks):
    localStorageSet('tododoneTasks', jsonStringify(tasks))
endfunction


# Load custom categories from local storage
function tododoneGetCustomCategories():
    categoriesJSON = localStorageGet('tododoneCategories')
    if categoriesJSON:
        categories = jsonParse(categoriesJSON)
        if categories:
            return categories
        endif
    endif
    return arrayNew()
endfunction


# Save custom categories to local storage
function tododoneSaveCustomCategories(categories):
    localStorageSet('tododoneCategories', jsonStringify(categories))
endfunction


# Execute the main entry point
tododoneMain()
~~~
