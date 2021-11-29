# contact-tracer
COVID-19 forward and backward contact tracer

 ### Introduction

Contact tracing is an important measure used to control outbreaks of infectious diseases such as COVID-19.

When a person infected with the disease is detected (known as an *index case*), they are asked to *isolate* (avoid contact with others) to prevent them from infecting other  people. In addition, recent contacts of the index case are traced and  asked to *quarantine* (avoid contact with others) for a period of time, just in case they were infected by the index case.

The contacts of an index case can be identified by interview, but  this can be time consuming and error prone. During COVID-19, Hong Kong and other countries have used digital approaches to contact tracing. One such digital approach involves asking people to use QR codes to "sign  in" to public locations (shops, restaurants, museums, etc) they visit.  The data collected in this way can then be analysed to help public  health officials find out which other people may have been potential  contacts of an infected index case.

Note that while the contact tracing scenario and strategies  described, accurately depict what happens in the real world, the  assumptions about disease spread, the QR code data format, and the  approaches to data analysis have been created for the purpose of this  project. In particular, there has been considerable debate about how  such data can be collected in a way that enables it to be used to help  aid outbreak control, while also preserving individual privacy. While of great interest, this project does not explore these issues!

### QR DATA

Each visit by a person to a location results in the following data being generated when they scan a QR code with their phone:

- an ID associated with that person
- an ID associated with the location
- an integer value corresponding to the day (note that this is not a  calendar date, but rather increments from "day zero" of the outbreak)
- a pair of `integer` values, corresponding to the time (hours and minutes, in 24 hour time) that the person arrived at the location
- a pair of `integer` values corresponding to the time (hours and minutes, in 24 hour time) that the person departed from the location

In this project, we will represent this data in a 7-`tuple`. For example, the `tuple`:

```python
("Irene", "Skylabs", 3, 9, 15, 13, 45)
```

tells us that Irene visited Skylabs on day 3 of the outbreak,  arriving at 9:15am and departing at 1:45pm (ie, 13:45 in 24 hour time).

Another example, the `tuple`:

```python
("Xaiton", "CoffeX", 10, 2, 5, 23, 59)
```

tells us that Xaiton visited CoffeX on day 10 of the outbreak,  arriving at 2:05am and departing at 11:59pm. If Xaoitan had stayed past  midnight, there would be another entry for day 11, starting at 00:00am.

# CALCULATING LENGTH
All example calls are listed in contacttracer-testing.py
Functions: visit_length(visit)

The function takes one argument, visit in the form of a 7-tuple.

The function should return the length of the visit as a tuple of integer values, corresponding to hours and minutes if the visit is valid, or None if the visit is not valid. A valid visit is one with a positive length (ie, more than zero minutes).

# DETERMINE WHETHER TWO VISITS OVERLAP
Functions: contact_event(visit_a, visit_b)

Determines whether two visits overlap in time and space, allowing for contact between two people to potentially occur.

The function should return True if a contact could have occurred between two distinct people, and False otherwise. If one visit began at the exact time that the other visit ended, you may assume that a potential contact could not occur (ie, the function should return False). If either of the visits is not valid, the function should return None.

# DETERMINE WHETHER TWO INDIVIDUALS WERE IN CONTACT
Functions: potential_contacts(person_a, person_b)

Identifies all potential contacts between two people, given data on their movement over multiple days.

Returns a tuple consisting of:
- a `set` of potential contact locations and times for these two people, each in the form of a 6-`tuple` (see below; note that the order of the items in this `set` does not matter, as a `set` does not store order); and
- a 2-`tuple` containing a pair of `integer` values (hours and minutes) corresponding to the total duration of potential contact between these two people.

Note that each the potential contact locations and time in the returned set is a 6-tuple rather than a 7-tuple because it will not include the ID of an individual. It also differs from the 7-tuple described above in that the times referred to, are not the time at which a person arrived at and departed from a location, but rather the time at which the two people started being at the same location (ie, when the second person arrive) and the time at which the two people stopped being at the same location (ie, when the first person left).

For example, if the original visit 7-`tuples` were:

```python
("Natalya", "Nutrity", 2, 10, 10, 11, 45)
```

and:

```python
("Chihiro", "Nutrity", 2, 9, 45, 11, 30)
```

then the 6-`tuple` corresponding to the potential contact between Natalya and Chihiro would be:

```python
("Nutrify", 2, 10, 10, 11, 30)
```

indicating that they were both located at Nutrity on the second day of the outbreak between 10:10am and 11:30am.

# FORWARD CONTACT TRACING
Functions: forward_contact_trace(visits, index, day_time, second_order=False)

Identifies all potential contacts of a detected index case that occurred after the time that they were detected. These are the people who will be contacted by public health officials to ask them to quarantine until they are sure that they were not infected by the index case.

It is possible that, by the time a contact of an index case has been traced, they may have already infected other people. Therefore, public health officials may wish to be very cautious and also trace the second order contacts of the index case. That is, the contacts of the contacts of the original detected case.

The function takes the following parameters:

- `visits` is a `list` of visits, with each visit formatted as a 7-`tuple` as described above;
- `index` is the ID of the detected index case;
- `day_time` is the day and time that the index case was detected, described as a 3-tuple containing the day, as an `integer` value, and time, as a pair of `integer` values, corresponding to hours and minutes, in 24 hour time; for example, `(2, 15, 35)` refers to 3:35pm on day 2 of the outbreak; and
- `second_order` a `Boolean` flag to indicate whether second order contacts of the `index` case should be included.

The function should return an alphabetically sorted list of IDs of people who should be traced and asked to quarantine.

# BACKWARD CONTACT TRACING
Functions: backward_contact_trace(visits, index, day_time, window)
While forward contact tracing can identify other people who may have been infected by the index case, it doesn't consider where the index case themself was infected from.

Backward contact tracing can be used to identify the potential source of the index case's infection by looking back through their recent contact history. Backward contact tracing can be very effective because once this earlier source case is identified, a larger proportion of potentially infected people can be identified by forward tracing each of the source's contacts.

This function dentifies the all potential sources of the specified index case's infection.

The function takes the following parameters:

- `visits` is a list of visits, with each visit formatted as a 7-`tuple` as described above;
- `index` is the ID of the detected index case;
- `day_time` is the day and time when the index case was detected, as a 3-`tuple` containing the day, as an `integer` value, and time, as a pair of `integer` values, corresponding to hours and minutes, in 24 hour time; for  example, (2, 15, 35) refers to 3:35pm on day 2 of the outbreak; and
- `window` is an `integer` representing the number of days prior to the detection of the index  case that backward tracing will be carried out. A window of 1 indicates  that all locations visited *prior to the time of detection* on  the same day that the index case was detected will be included. A window of 2 indicates that all locations visited on the previous day will *also* be included, and so on.

The function should return an alphabetically sorted `list` of IDs of people who should be traced and tested to identify whether  they were the potential source of the index case's infection.
