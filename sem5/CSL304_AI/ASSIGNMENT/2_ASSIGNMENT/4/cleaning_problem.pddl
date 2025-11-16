(define (problem cleaning-task)
  (:domain cleaning-robot)

  (:objects
    robot1 - robot
    classroom cafeteria - location ; <-- REMOVED 'dustbin' FROM THIS LINE
    trash1 trash2 - trash
  )

  (:init
    ;; Robot's initial location
    (at-robot robot1 classroom)
    (hand-empty robot1)

    ;; Room connections
    (connected classroom cafeteria)
    (connected cafeteria classroom)
    (connected cafeteria dustbin) ; <-- This is still correct
    (connected dustbin cafeteria) ; <-- This is also correct

    ;; Initial state of rooms
    (dirty classroom)
    (dirty cafeteria)

    ;; Initial location of trash
    (at-trash trash1 classroom)
    (at-trash trash2 cafeteria)
  )

  (:goal (and
    ;; Both rooms must be fully cleaned
    (mopped classroom)
    (mopped cafeteria)

    ;; All trash must be disposed of
    (disposed trash1)
    (disposed trash2)

    ;; Robot must not be carrying anything
    (hand-empty robot1)
  ))
)