import prettytable as prettytable
import random as rnd
import numpy as np

POPULATION_SIZE = 7
MUTATION_RATE = 0.1 # between 0 and 2

class Data:
    
    ROOMS = [["H1",400],["H2",350],["H3",200]]
    
    MEETING_TIMES = [["LEC1", "From 9:00 AM  to   11:00 AM"],
                    ["LEC2","From 9:00 AM  to  11 PM"],
                    ["LEC3", "From 9:00 PM  to  11:00 PM"],
                    ["LEC4","From 9:00 PM  to  11:00 PM"]]

    INSTRUCTORS = [["I1", "DR/ Amr"],
                   ["I2","DR/Serah"],
                   ["I3", "DR/Laila"],
                   ["I4", "DR/Joe"]]
    


    def __init__(self):
        self._rooms = []; self._meetingTimes = []; self._instructors = []
        for i in range(0, len(self.ROOMS)):
         self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))
        for i in range(0, len(self.MEETING_TIMES)):
         self._meetingTimes.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        for i in range(0, len(self.INSTRUCTORS)):
         self._instructors.append(Instructor(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))
        course1 = Course("C1", "CS-121", [self._instructors[0], self._instructors[1]], 120)
        course2 = Course("C2", "CS-214", [self._instructors[0], self._instructors[1], self._instructors[2]], 150)
        course3 = Course("C3", "CS-314", [self._instructors[0], self._instructors[1]], 200)
        course4 = Course("C4", "IS-241", [self._instructors[2], self._instructors[3]], 100)
        course5 = Course("C5", "IT-222", [self._instructors[3]], 140)
        course6 = Course("C6", "IS-211", [self._instructors[0], self._instructors[2]], 190)
        course7 = Course("C7", "IS-444", [self._instructors[1], self._instructors[3]], 120)
        self._courses = [course1, course2, course3, course4, course5, course6, course7]
        
        # departement of each class

        dept1 = Department("CS", [course1, course3])
        dept2 = Department("IS", [course2, course4, course5])
        dept3 = Department("IT", [course6, course7])
        self._depts = [dept1, dept2, dept3]
        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())
    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses

class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True
    
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    
    def get_numbOfConflicts(self): return self._numbOfConflicts
    
    def get_fitness(self):
        if (self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness
   
    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            for j in range(0, len(courses)):
                newClass = Class(self._classNumb, depts[i], courses[j])
                self._classNumb += 1
                newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(data.get_meetingTimes()))])
                newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                newClass.set_instructor(courses[j].get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(newClass)
        return self
    
    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and
                    classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()): self._numbOfConflicts += 1
                        if (classes[i].get_instructor() == classes[j].get_instructor()): self._numbOfConflicts += 1
        return 1 / ((1.0*self._numbOfConflicts + 1))
    # put , to separate  classes in the table 
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes)-1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue


# DIFFRENTIAL ALGORITHM 
class DE(object):
     
     def __init__(self,
                 popul_size,
                 fitness_vec_size,
                 cross_prob
                 ):

        self.population_size = popul_size
        self.fitness_vector_size = fitness_vec_size
        self._data = data
        self.mutants = list()   
        self.trial = list()
        self.cr = cross_prob
        self.target = list()

        self.population = []
        
        for i in range(0,POPULATION_SIZE):
         self.population.append(Schedule().initialize())
        
          
             
         
         
     def mutate(self):
         for j in range(0, POPULATION_SIZE):
 
          candidates = list(range(0,POPULATION_SIZE))
        # targetParent=rnd.randint(POPULATION_SIZE)
          candidates.remove(j)
          random_index = rnd.sample(candidates,3)
       
         parent1 =self.population[random_index [0]]
         parent2 =self. population[random_index [1]]
         parent3 = self.population[random_index[2]]
         targetParent =self.population[j] # target individual
        
         for i in range(0,POPULATION_SIZE):
        
            # subtract x3 from x2, and create a new vector (x_diff)
          x_diff = [Schedule().calculate_fitness(parent2_i -parent3_i) for parent2_i , parent3_i in zip(parent2,parent3)]
    

        #     # multiply x_diff by the mutation factor (F) and add to x_1
          mutants= [Schedule().calculate_fitness(parent1_i + (MUTATION_RATE * x_diff_i)) for parent1_i, x_diff_i in zip(parent1, x_diff)]
        
     
    
     def crossover(self):
         target = self.target.append(Schedule.calculate_fitness(mutate(self.targeparent)))
         trial=[]
         for v, x in enumerate(zip(self.mutants, self.target)):
             if (np.random.randit(0,1) <= self.cr):
                 trial.append(mutants[v])
             else:
                 trial.append(target[x])


            
     def select(self):  #if  the trial better than target then replace (CR)
        for x, i in (self.target, self.trial):
            if (self.target[x] >= self.trial[i]):
                continue
            else:self.target[x] =self.trial[i]  

#the end of differential


# class course to intialize  course name, class number ,instructor , max no of students 
class Course:
    def __init__(self, number, name, instructors, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._maxNumbOfStudents = maxNumbOfStudents
        self._instructors = instructors
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_instructors(self): return self._instructors
    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents
    def __str__(self): return self._name
# class instructor to intialize instructor's name and id 
class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name

# class room to intialize room's number and the seeting capacity
class Room:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
    def get_number(self): return self._number
    def get_seatingCapacity(self): return self._seatingCapacity
# mrrting time of the lectures
class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time
    def get_id(self): return self._id
    def get_time(self): return self._time
# departement name of the course
class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses
    def get_name(self): return self._name
    def get_courses(self): return self._courses
# class name , course and it's departement
class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None
    def get_id(self): return self._id
    def get_dept(self): return self._dept
    def get_course(self): return self._course
    def get_instructor(self): return self._instructor
    def get_meetingTime(self): return self._meetingTime
    def get_room(self): return self._room
    def set_instructor(self, instructor): self._instructor = instructor
    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime
    def set_room(self, room): self._room = room
    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
               str(self._room.get_number()) + "," + str(self._instructor.get_id()) + "," + str(self._meetingTime.get_id())

# to display the output  in tables using pretty table liberary

class DisplayMgr:
    def print_available_data(self):
        print("> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()
    def print_dept(self):
        depts = data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)
    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
        courses = data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)
    def print_instructor(self):
        availableInstructorsTable = prettytable.PrettyTable(['id', 'instructor'])
        instructors = data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row([instructors[i].get_id(), instructors[i].get_name()])
        print(availableInstructorsTable)
    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)
    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(['id', 'Meeting Time'])
        meetingTimes = data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)
    def print_generation(self, population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'classes [dept,class,room,instructor,meeting-time]'])
        schedules = population
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(),3), schedules[i].get_numbOfConflicts(), schedules[i].__str__()])
        print(table1)
    def print_schedule_as_table(self, schedule):
        classes=schedule.get_classes()
        table = prettytable.PrettyTable(['Class #', 'Dept', 'Course (number, max # of students)', 'Room (Capacity)', 'Instructor (Id)',  'Meeting Time (Id)'])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + " (" +
                           classes[i].get_course().get_number() + ", " +
                           str(classes[i].get_course().get_maxNumbOfStudents()) +")",
                           classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")",
                           classes[i].get_instructor().get_name() +" (" + str(classes[i].get_instructor().get_id()) +")",
                           classes[i].get_meetingTime().get_time() +" (" + str(classes[i].get_meetingTime().get_id()) +")"])
        print(table)
        


 
data = Data()
displayMgr = DisplayMgr()
displayMgr.print_available_data()
generationNumber = 0
print("\n> Generation # "+str(generationNumber))
de = DE(POPULATION_SIZE, fitness_vec_size=5, cross_prob=0.5)
de.population.sort(key=lambda x: x.get_fitness(), reverse=True)
displayMgr.print_generation(de.population)
displayMgr.print_schedule_as_table(de.population[0])
try:
 while (de.population[0].get_fitness() != 1.0):
    
  for i in range(POPULATION_SIZE):
     de.mutate()
     de.crossover()
     de.select()

     de.population.sort(key=lambda x: x.get_fitness(), reverse=True)
     displayMgr.print_generation(de.population)
     displayMgr.print_schedule_as_table(de.population[0])
 print("\n\n")
except:
 print("")

