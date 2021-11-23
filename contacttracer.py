def visit_length(visit):
    """Accepts a list "visit" and calculates the hour and minute
    the person stayed at a place in the form of a tuple.
    """
    # Calculates initial time from the index of the list
    hour = visit[5] - visit[3]
    minute = visit[6] - visit[4]

    # If there are negative minutes, it subtracts 1 from
    # the hour and adds 60 to the minute
    if minute < 0:
        hour -= 1
        minute += 60

    # Returns final time calculation
    if hour < 0:
        return None
    elif hour == 0 and minute == 0:
        return None
    return hour, minute

from datetime import datetime


def time_difference(a, b):
    """Using datetime module to determine whether contact has been made
    Formula: min(A and B leaving times) - max(A and B arriving times)
    If the result is positive, contact has been made.
    """

    fmt = "%H:%M"

    # Creates datetime objects from the arriving and leaving times
    a1_time = datetime.strptime(f"{a[3]}:{a[4]}", fmt)
    a2_time = datetime.strptime(f"{a[5]}:{a[6]}", fmt)

    b1_time = datetime.strptime(f"{b[3]}:{b[4]}", fmt)
    b2_time = datetime.strptime(f"{b[5]}:{b[6]}", fmt)

    return min(a2_time, b2_time) - max(a1_time, b1_time)


def contact_event(a, b):
    """This function takes in 2 arguments of the 7-tuple and
    returns True if there has been potential contact between visit_a
    and visit_b. It returns False if there has been no contact.
    It returns None if the arguments are invalid
    """

    # Checking if times are valid
    if not visit_length(a) or not visit_length(b):
        return None
    elif a[0] == b[0]:  # Name is the same
        return False
    elif a[1] != b[1]:  # Place is not the same
        return False
    elif a[2] != b[2]:  # Day is not the same
        return False
    else:  # If no errors found
        difference = time_difference(a, b)

        if "-" in str(difference):
            return False
        elif str(difference) == "0:00:00":
            return False
        return True

def potential_contacts(person_a, person_b):
    """
    potential_contacts() determines the places person_a and person_b
    visited on the same day, and the intersecting times they were at.

    person_a and person_b contains a tuple of 7 elements:
    (Name, Place, Day, ArriveHour, ArriveMinute, LeaveHour, LeaveMinute)
    Name and Place are strings, and the hours are in a 24-hour format.
    """
    total_hours = 0
    total_minutes = 0
    finallist = set()

    if total_minutes >= 60:
        total_hours += 1
        total_minutes -= 60

    a_places = [i[1] for i in person_a]
    b_places = [i[1] for i in person_b]
    ab_places = list(set(a_places) & set(b_places))

    valid_list_a = [i for i in person_a if i[1] in ab_places]
    valid_list_b = [i for i in person_b if i[1] in ab_places]

    # Since the index 0 is the same, sorted() will sort according to the Place
    for a in sorted(valid_list_a):
        for b in sorted(valid_list_b):
            if a[2] == b[2] and a[1] == b[1]:  # If the day is matching
                if contact_event(a, b):
                    # Same method as contact_event, but adds hours and
                    # minutes to a total (total_hours and total_minutes)

                    # Person A and B's arriving (1) and leaving (2) times
                    a1 = (a[3], a[4])
                    a2 = (a[5], a[6])
                    b1 = (b[3], b[4])
                    b2 = (b[5], b[6])

                    difference = time_difference(a, b)

                    if "-" not in str(difference) or str(difference) != "0:00:00":
                        total_hours += int(str(difference).split(":")[0])
                        total_minutes += int(str(difference).split(":")[1])

                        finallist.add(
                            (
                                a[1],
                                a[2],
                                max(a1, b1)[0],
                                max(a1, b1)[1],
                                min(a2, b2)[0],
                                min(a2, b2)[1],
                            )
                        )

    return finallist, (total_hours, total_minutes)

orig_inf = ""
order2info = []
times = 0

def forward_contact_trace(visits, index, day_time, second_order=False):
    """
    Given a list of visits, a person's name and the time they became infected,
    forward_contact_trace() returns the list of people that came into contact
    with the original infected.

    If second_order=True, this function will be called again with a new set of
    data, and will detect the contacts of the contacts that first came into
    contact with the original infected.

    This function uses helper functions used in previous worksheets, namely
    visit_length(), time_difference() and contact_event().

    Global variables are used to preserve data in the event of recursion.
    """

    # Global variables to preserve the data passed into the function
    global order2info, times, orig_inf

    infectees = []
    final_infs = []

    times += 1
    # Preserves original index from recursion. Checks how many times
    # this function has been called.
    if times == 1:
        orig_inf = index

    # Removes visits that happened BEFORE the original infected time.
    for i in visits:
        if i[2] < day_time[0]:
            visits.remove(i)
        elif i[2] == day_time[0]:
            fmt = "%H:%M"
            inf_time = datetime.strptime(f"{day_time[1]}:{day_time[2]}", fmt)
            visit_time1 = datetime.strptime(f"{i[3]}:{i[4]}", fmt)
            visit_time2 = datetime.strptime(f"{i[5]}:{i[6]}", fmt)

            difference = inf_time - max(visit_time1, visit_time2)

            if "-" not in str(difference):
                visits.remove(i)


    # Filters visits into 2 lists, infected_visits with visits from
    # the infected person, and non_inf_visits from non infected people
    infected_visits = [i for i in visits if i[0] == index]
    non_inf_visits = [i for i in visits if i[0] != index]
    p_contact = potential_contacts(infected_visits, non_inf_visits)

    # Prepares data of potential contacts to be passed into contact_event,
    # in the form of day_time: (Day, Hour, Minute)
    tempinfo = []
    for i in [list(i) for i in list(p_contact[0])]:
        i.pop(0)
        tempinfo.append(i[:3])

    # Determines whether the Index came into contact with people in
    # non_inf_visits, and if so, adds their information to
    # the variable order2info in the form of (Name, (Day_time))
    for i in [list(i) for i in list(p_contact[0])]:
        i.insert(0, "name")  # Generic name here, only for contact_event()
        for j in non_inf_visits:
            if contact_event(i, j):
                infectees.append(j[0])
                if j[0] not in [i[0] for i in order2info]:
                    order2info.append([j[0], tuple((sorted(tempinfo))[0])])

    # Detects contacts of the people in order2info. Uses the same function
    # to detect the contacts recursively. Adds the names into infectees list.
    if second_order:
        for i in order2info:
            infectees += forward_contact_trace(visits, i[0], i[1])

    # Adds unique names into the final list 'final_infs'.
    for i in infectees:
        if i not in final_infs:
            final_infs.append(i)

    # Removes original infected from final infected list.
    for i in final_infs:
        if i == orig_inf:
            final_infs.remove(i)

    return sorted(final_infs)

def backward_contact_trace(visits, index, day_time, window):
    """
    Given a list of visits, and the time when the index case was detected,
    backward_contact_trace() returns the list of names of people who
    could have came into contact with index within a time frame of an integer
    window, before the case was detected.

    backward_contact_trace() is mostly similar to forward_contact_trace(),
    with regard to nearly everything except global variables and recursion.

    The filtering of visits now removes visits which happened after the visit
    had occured, as well as visits which happened the day before the day of
    the detected case.
    """

    infectees = []
    final_infs = []

    # Removes visits that happened AFTER the original infected time
    # and visits that occured before the index case was detected
    for i in visits:
        if i[2] > day_time[0]:  # If visit day is AFTER detected day
            visits.remove(i)
        elif i[2] == day_time[0]:  # If visit day is SAME AS detected day
            fmt = "%H:%M"
            inf_time = datetime.strptime(f"{day_time[1]}:{day_time[2]}", fmt)
            visit_time1 = datetime.strptime(f"{i[3]}:{i[4]}", fmt)
            visit_time2 = datetime.strptime(f"{i[5]}:{i[6]}", fmt)

            difference = max(visit_time1, visit_time2) - inf_time

            if "-" not in str(difference) or str(difference) == "0:00:00":
                visits.remove(i)
        elif not day_time[0] - (window - 1) <= i[2] or not i[2] < day_time[0]:
            visits.remove(i)

    # Filters visits into 2 lists, infected_visits with visits from
    # the infected person, and non_inf_visits from non infected people
    infected_visits = [i for i in visits if i[0] == index]
    non_inf_visits = [i for i in visits if i[0] != index]
    p_contact = potential_contacts(infected_visits, non_inf_visits)

    # Prepares data of potential contacts to be passed into contact_event,
    # in the form of day_time: (Day, Hour, Minute)
    tempinfo = []
    for i in [list(i) for i in list(p_contact[0])]:
        i.pop(0)
        tempinfo.append(i[:3])

    # Determines whether the Index came into contact with people in
    # non_inf_visits, and if so, adds their information to
    # the variable order2info in the form of (Name, (Day_time))
    for i in [list(i) for i in list(p_contact[0])]:
        i.insert(0, "name")  # Generic name here, only for contact_event()
        for j in non_inf_visits:
            if contact_event(i, j):
                infectees.append(j[0])

    # Adds unique names into the final list 'final_infs'.
    for i in infectees:
        if i not in final_infs:
            final_infs.append(i)

    # Removes original infected from final infected list.
    for i in final_infs:
        if i == index:
            final_infs.remove(i)

    return sorted(final_infs)

