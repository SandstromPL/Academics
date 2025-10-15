(define (problem problem_hospital) (:domain domain_hospital)
(:objects 
            a1 a2
            p1 p2 p3
            loc1 loc2 loc3
            h1 h2
)

(:init
            (at a1 h1) (at a2 h2)
            (patient-at p1 loc1) (patient-at p2 loc2) (patient-at p3 loc3)
            (empty a1) (empty a2)
            ; map below
            (connected h1 loc1) (connected loc1 h1)
            (connected loc1 loc2) (connected loc2 loc1)
            (connected loc2 loc3) (connected loc3 loc2)
            (connected loc3 h2) (connected h2 loc3)
)

(:goal (and 
            (patient-at p1 h1) (patient-at p2 h2) (patient-at p3 h1)
))

)
