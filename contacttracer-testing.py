from contacttracer import *

def main():

	# CALCULATING THE LENGTH OF A VISIT

    print(visit_length(('Russel', 'Foodigm', 2, 9, 0, 10, 0))) 
    # (1,0)
    print(visit_length(('Russel', 'Foodigm', 2, 9, 0, 10, 0)))
    # (1, 0)
    print(visit_length(('Natalya', 'Foodigm', 2, 9, 30, 9, 45)))
    # (0, 15)
    print(visit_length(('Chihiro', 'Foodigm', 2, 8, 45, 9, 15)))
    # (0, 30)
    print(visit_length(('Aravinda', 'Afforage', 2, 9, 0, 10, 0)))
    # (1, 0)
    print(visit_length(('Chihiro', 'Foodigm', 2, 8, 30, 9, 0)))
    # (0, 30)
    print(visit_length(('Natalya', 'Afforage', 2, 15, 10, 14, 45)))  # the length of the visit is negative
    # None
    print(visit_length(('Aravinda', 'Nutrity', 2, 15, 10, 15, 10)))  # the length of the visit is zero
    # None

	# DETERMINING WHETHER TWO VISITS OVERLAP
	
    print(contact_event(('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Natalya', 'Foodigm', 2, 9, 30, 9, 45)))
    # True
    print(contact_event(('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Natalya', 'Foodigm', 2, 10, 0, 10, 20)))
    # False
    print(contact_event(("Natalya", 'Foodigm', 2, 9, 30, 9, 45), ('Chihiro', 'Foodigm', 2, 8, 45, 9, 15))) # there is no time overlap
    # False
    print(contact_event(('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Aravinda', 'Afforage', 2, 9, 0, 10, 0))) # the two visit were to different locations
    # False
    print(contact_event(('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Russel', 'Foodigm', 2, 8, 30, 9, 0))) # the two visits are by the same person
    # False
    print(contact_event(('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Natalya', 'Afforage', 2, 15, 10, 14, 45))) # one of the visits is invalid
    # None
    
	# DETERMINE WHETHER TWO INDIVIDUALS WERE IN CONTACT

    print(potential_contacts([('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Russel', 'Afforage', 2, 10, 0, 11, 30), ('Russel', 'Nutrity', 2, 11, 45, 12, 0), ('Russel', 'Liberry', 3, 13, 0, 14, 15)], [('Natalya', 'Afforage', 2, 8, 15, 10, 0), ('Natalya', 'Nutrity', 4, 10, 10, 11, 45)]))
    # (set(), (0, 0))
    print(potential_contacts([('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Russel', 'Afforage', 2, 10, 0, 11, 30), ('Russel', 'Nutrity', 2, 11, 45, 12, 0), ('Russel', 'Liberry', 3, 13, 0, 14, 15)], [('Chihiro', 'Foodigm', 2, 9, 15, 9, 30), ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30), ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]))
    # ({('Foodigm', 2, 9, 15, 9, 30), ('Liberry', 3, 13, 0, 13, 25)}, (0, 40))
    print(potential_contacts([('Natalya', 'Afforage', 2, 8, 15, 10, 0), ('Natalya', 'Nutrity', 4, 10, 10, 11, 45)], [('Chihiro', 'Foodigm', 2, 9, 15, 9, 30), ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30), ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]))
    # ({('Nutrity', 4, 10, 10, 11, 30)}, (1, 20))
    print(potential_contacts([('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Russel', 'Afforage', 2, 10, 0, 11, 30), ('Russel', 'Nutrity', 2, 11, 45, 12, 0), ('Russel', 'Liberry', 3, 13, 0, 14, 15)], []))  # person with no visits
    # (set(), (0, 0))

	# FORWARD CONTACT TRACING

    visits = [('Russel', 'Nutrity', 1, 5, 0, 6, 0),
            ('Russel', 'Foodigm', 2, 9, 0, 10, 0),
            ('Russel', 'Afforage', 2, 10, 0, 11, 30),
            ('Russel', 'Nutrity', 2, 11, 45, 12, 0),
            ('Russel', 'Liberry', 3, 13, 0, 14, 15),
            ('Natalya', 'Nutrity', 1, 5, 30, 6, 45),
            ('Natalya', 'Afforage', 2, 8, 15, 10, 0),
            ('Natalya', 'Nutrity', 4, 10, 10, 11, 45),
            ('Chihiro', 'Foodigm', 2, 9, 15, 9, 30),
            ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30),
            ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]
    print(forward_contact_trace(visits, 'Russel', (1, 9, 0)))
    # ['Chihiro']

    visits = [('Russel', 'Nutrity', 1, 5, 0, 6, 0),
            ('Russel', 'Foodigm', 2, 9, 0, 10, 0),
            ('Russel', 'Afforage', 2, 10, 0, 11, 30),
            ('Russel', 'Nutrity', 2, 11, 45, 12, 0),
            ('Russel', 'Liberry', 3, 13, 0, 14, 15),
            ('Natalya', 'Nutrity', 1, 5, 30, 6, 45),
            ('Natalya', 'Afforage', 2, 8, 15, 10, 0),
            ('Natalya', 'Nutrity', 4, 10, 10, 11, 45),
            ('Chihiro', 'Foodigm', 2, 9, 15, 9, 30),
            ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30),
            ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]

    print(forward_contact_trace(visits, 'Russel', (1, 9, 0), second_order=True))
    # ['Chihiro', 'Natalya']

	# BACKWARD CONTACT TRACING

    visits = [('Russel', 'Foodigm', 2, 9, 0, 10, 0),
            ('Russel', 'Afforage', 2, 10, 0, 11, 30),
            ('Russel', 'Nutrity', 2, 11, 45, 12, 0),
            ('Russel', 'Liberry', 3, 13, 0, 14, 15),
            ('Natalya', 'Afforage', 2, 8, 15, 10, 0),
            ('Natalya', 'Nutrity', 4, 10, 10, 11, 45),
            ('Chihiro', 'Foodigm', 2, 9, 15, 9, 30),
            ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30),
            ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]

    print(backward_contact_trace(visits, 'Natalya', (4, 13, 0), 1))
    # ['Chihiro']

if __name__ == "__main__":
    main()
