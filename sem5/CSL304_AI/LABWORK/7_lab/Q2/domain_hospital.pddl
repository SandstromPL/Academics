
(define (domain domain_hospital)

(:requirements :strips :negative-preconditions)


(:predicates 
                (at ?a ?l)
                (patient-at ?p ?l)
                (in-ambulance ?p ?a)
                (connected ?l1 ?l2)
                (blocked ?l1 ?l2)
                (empty ?a)
)



(:action move
    :parameters (?a ?from ?to)
    :precondition (and (at ?a ?from) (connected ?from ?to) (not (blocked ?from ?to)))
    :effect (and (at ?a ?to) (not (at ?a ?from)))
)

(:action pickup-patient
    :parameters (?p ?a ?l)
    :precondition (and (at ?a ?l) (patient-at ?p ?l) (empty ?a))
    :effect (and (in-ambulance ?p ?a) (not (patient-at ?p ?l)) (not (empty ?a)))
)

(:action dropoff-patient
    :parameters (?p ?a ?h)
    :precondition (and (at ?a ?h) (in-ambulance ?p ?a))
    :effect (and (patient-at ?p ?h) (empty ?a) (not (in-ambulance ?p ?a)))
)


)
