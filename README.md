# tsoha-nenonen
Tsoha, course exercise, summer 2022

heroku link: https://voluntee-app.herokuapp.com/

STATUS 
-- 04.9.2022
 - CSRF weaknesses fixed
 - Fixed Error when taking task that somebody else has already taken
 - Added functions to calculate stuff from database
 - Added more columns to tasks, etc. work_time
 - Made profile page for users

 ![](./static/database_sketch.png)


-- 21.8.2022
 - You can make a team and others can join it with correct password
 - You can take tasks, and change their status TODO->WORKING->DONE 
 - You can leave comments into tasks
 - using css and bootstrap
 
 In progress: 
 - profile pages 
 - messages between two users
 - searches to bring more stats
 - currently mytasks is broken
 - 
-- 7.8.2022
 - It is possible to make an account 
 - You can login with the account
 - You can make a new task
 
In progress: commenting on each task

-------------------------------------------------------------------

This exercise is done using flask with python and postregreSQL.

This application is developed with a working name "voluntary app".
It is variation of a classical todo application for voluntary work.
The admins can create todos and voluntees can pick ones suitable for them.

1. Admin/User can register with a username and password.

2. Admin can make new todos and remove existing ones.
    - todo_id
    - admin username
    - todo name
    - todo description
    - deadline
    - date of creation
    - Default state: todo 
    - Default voluntee name that has picked the todo: none
    - Default visibility: visible

3. User can pick a task to do.
     voluntee name: none -> username
     state: todo -> working

4. User can mark a task done.
    state: working -> done

4. Users can comment todos.
    - todo_id
    - username
    - message

5. User can filter todos on different criteria:
   - admin name
   - todo states
   - todos containing specific words in name/description
   - comments containing specific words

---------------------------------------------------------------------



