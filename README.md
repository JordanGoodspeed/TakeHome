# TakeHome
Hi, my name is Jordan Goodspeed, and this is my submission for the Schoolytics.io take home challenge.  I apologize for the delay, we are in the final delivery phase of phase 1 for my present contract, and I haven't had any free time during the week.  For reference purposes, here was the problem description as it was given to me:
  
=============================================
  
  
We need to build flexible APIs that will be used by a variety of end users connecting from different client applications. We want to see that you can design a starter API that is set up to grow to handle more tables, columns, and different kinds of queries in the future.
With that in mind, for this exercise develop an API that dynamically generates the following database queries:

• Group by student_id and count completed assignments
• Group by course_id and average grade
• Group by teacher_id and count assignments created
• Group by school_id and find percentage of students with more than 1 assignment completed

Use the web framework of your choice. Also use the datastore of your choice, but we suggest simply using SQLite to get started. Imagine the following 3 datasets when executing queries:

student_submission - this table describes all the assignments administered to students and their status  
• submission_id (primary key)  
• course_work_id  
• course_id  
• student_id  
• status (enum NEW, TURNED_IN)  
• assigned_points (float)  
• max_points (float)  
  
roster - this table describes all the students rostered in a course  
• student_id  
• course_id  

student - this table describes additional information about a student
• student_id
• school
• grade_level
  
course - this table describes additional information about a course  
• teacher_id  
• course_id  
• name  
  
course_work - this table describes additional information about course work (assignments)  
• course_id  
• title  
• due date  
    
    =============================================
  
  
   So, what I took from this was that the base-level requirement was to deliver a project implemented in (some web framework) that had 4 initial, presumably RESTful API endpoints that would provide data in a JSON format from some DB, with a recommendation of SQLite, to an end-user in response to a GET request.  It would also have room to add "more tables, columns, and different kinds of queries in the future".  Towards that end I set up a very simple Django project, incorporating the django_rest_framework add-on to enable the API functionality, that had 5 models defined in it.  This already caused me a little bit of confusion, as you mentioned "3 datasets" above, but gave me five definitions for tables, and strongly implied the existence of at least 1 more.  I was also a little confused because one of the tables definied above, "roster", didn't have any new information specified, or any utility that I could see in any of the queries, whereas the incorporation of 'teacher_id' strongly implied the existence of a "teacher" table, and indeed assuming it as a Foreign key in Course required that I instantiate it in 'models.py' in order to properly migrate the database.  
    So, I already had some decisions to make there.  I decided to create 5 Models for Django's ORM, those being StudentSubmission, Student, Course, CourseWork, and Teacher.  I left off "roster", added what I thought were some reasonable fields to Teacher (not just teacher_id, but name, school as well), added the 'course_work_id' field listed under "student_submission" to "CourseWork".  I left references to "school" as a CharField, rather than create another model for 'School', as was implied by the reference to "school_id" in the definition of the 4th query requirement, in the interests of time.  I created an additional file 'utils.py' to properly enable the enum values specified for "student_submission.status".  I also defined shared columns (with the exception of 'school') as Foreign Keys, which as mentioned previously obliged the creation of a Teacher Model to reference.  
    After running the migrations, I created a Jupyter notebook of type 'Django Shell-Plus' (using the django-extensions and jupyter add-ons) called 'GenerateTestData.ipynb' to instantiate some test data in the DB programmatically using some data I defined or pulled off of DuckDuckGo.  This wasn't explicitly in the requirements, but I preferred to have it for testing purposes.  Once I had created that and saved it in 'db.sqlite3', I focuused on creating the logic necessary for the four specified queries.  I set up four views, using the 'APIView' from the django_rest_framework, as well as its 'Response' and 'status' objects, and defined 'GET' responses that output the desired information.  I elected to skip setting up a separate 'serializer.py' file, and just converted the querysets to JSON in the view.  I tried to use the ORM as much as I felt comfortable doing, using list comprehensions, dictionary comprehensions, and a Counter object where I felt it was cleaner to do so.  
    Once the views were created, I specified where they could be reached in the 'api/urls.py' file, and then provided a further reference to that in the overall 'projects/urls.py' file.  I used the associated development server to test that each of the four defined endpoints would return a 200 status code and the requisite JSON with a GET request to the appropriate URL.  Having done so, I concluded development work and pushed the project to Git.  I did not, in the course of this project, specify a superuser for the project, set up any sort of authentication or permissions, or do any front-end work.  The steps taken / commands entered are summarized below:
  
  =============================================
  
  
pip install Django  
mkdir Django  
cd Django/  
django-admin startproject projects  
cd projects/  
python manage.py startapp api  

In 'Projects/settings.py':
Added 'api' to 'INSTALLED_APPS'.

In 'api/models.py', added models for:
StudentSubmission
Teacher
Student
Course
CourseWork

In the course of doing the above, created 'api/utils.py' to enable enums for StudentSubmission.status

python manage.py makemigrations
python manage.py migrate
pip install django-extensions jupyter

Added this to 'projects/settings.py':
#Jupyter

NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888'
]

Added this to "INSTALLED_APPS":
'django_extensions',

DJANGO_ALLOW_ASYNC_UNSAFE=true && python manage.py shell_plus --notebook

In Jupyter, created a new notebook 'GenerateTestData.ipynb', with 'Django Shell-Plus' as the type. Created and saved the dummy data.

pip install django_rest_framework

Added 'rest_framework' to 'INSTALLED_APPS' of 'projects/settings.py'

Added the following APIViews to 'api/views.py':
CountCompletedAssignments
GetCourseAverageGrade
CountAssignmentsCreated
SchoolAssignmentCompletionPercentage

Made the appropriate references to them when setting up URL endpoints in 'api/urls.py'

Made the appropriate references to 'api.urls' in 'projects.urls'.

python manage.py runserver

And navigated to the following URLs to view the output:  
http://127.0.0.1:8000/api/CountCompletedAssignments/  
http://127.0.0.1:8000/api/GetCourseAverageGrade/  
http://127.0.0.1:8000/api/CountAssignmentsCreated/  
http://127.0.0.1:8000/api/SchoolAssignmentCompletionPercentage/  

=============================================

With that, I would like to take the opportunity to thank you for giving me the change to work on this.  I appreciate the time that you have taken thus far, and I hope to hear from you again soon.  Please don't hesitate to reach out if you have any comments or questions, or if any of the above needs clarification.  Thanks!

- Jordan Goodspeed
