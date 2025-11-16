(define (domain cleaning-robot)
  (:requirements :strips :typing)

  (:types
    robot
    location
    trash
  )

  (:constants
    dustbin - location  ; <-- ADDED THIS SECTION
  )

  (:predicates
    (at-robot ?r - robot ?l - location)
    (at-trash ?t - trash ?l - location)
    (connected ?from - location ?to - location)
    (dirty ?l - location)
    (swept ?l - location)
    (mopped ?l - location)
    (carrying ?r - robot ?t - trash)
    (hand-empty ?r - robot)
    (disposed ?t - trash)
  )

  (:action move
    :parameters (?r - robot ?from - location ?to - location)
    :precondition (and
      (at-robot ?r ?from)
      (connected ?from ?to)
    )
    :effect (and
      (not (at-robot ?r ?from))
      (at-robot ?r ?to)
    )
  )

  (:action sweep
    :parameters (?r - robot ?l - location)
    :precondition (and
      (at-robot ?r ?l)
      (dirty ?l)
    )
    :effect (and
      (not (dirty ?l))
      (swept ?l)
    )
  )

  (:action mop
    :parameters (?r - robot ?l - location)
    :precondition (and
      (at-robot ?r ?l)
      (swept ?l)
    )
    :effect (and
      (not (swept ?l))
      (mopped ?l)
    )
  )

  (:action pick-trash
    :parameters (?r - robot ?t - trash ?l - location)
    :precondition (and
      (at-robot ?r ?l)
      (at-trash ?t ?l)
      (hand-empty ?r)
    )
    :effect (and
      (not (at-trash ?t ?l))
      (not (hand-empty ?r))
      (carrying ?r ?t)
    )
  )

  (:action drop-trash
    :parameters (?r - robot ?t - trash)
    :precondition (and
      (at-robot ?r dustbin) ; <-- This line is now valid
      (carrying ?r ?t)
    )
    :effect (and
      (not (carrying ?r ?t))
      (hand-empty ?r)
      (disposed ?t)
    )
  )
)