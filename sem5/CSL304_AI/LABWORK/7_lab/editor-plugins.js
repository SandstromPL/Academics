
// Put this file online somewhere and import it as a plugin

define(function () {
    return {
        meta: true,
        plugins:
{
    "planning-as-a-service-plugin": {
        "url": "/plugins/featured/paas/plugin.js",
        "settings": {
            "PASURL": "https://solver.planning.domains:5001"
        }
    },
    "drag-and-drop": {
        "url": "/plugins/featured/drag-and-drop/plugin.js",
        "settings": {}
    },
    "save-tabs": {
        "url": "/plugins/featured/save-tabs/plugin.js",
        "settings": {
            "unnamed1.pddl": "",
            "problem_gripper.pddl": "(define (problem problem_gripper) (:domain domain_gripper)\n(:objects   rooma roomb\n            ball1 ball2 ball3 ball4\n            left right\n)\n\n(:init\n            (ROOM rooma) (ROOM roomb)\n            (BALL ball1) (BALL ball2) (BALL ball3) (BALL ball4)\n            (GRIPPER left) (GRIPPER right) (free left) (free right)\n            (at-robby rooma)\n            (at-ball ball1 rooma) (at-ball ball2 rooma)\n            (at-ball ball3 rooma) (at-ball ball4 rooma)\n    ;todo: put the initial state's facts and numeric values here\n)\n\n(:goal (and\n            (at-ball ball1 roomb) (at-ball ball2 roomb)\n            (at-ball ball3 roomb) (at-ball ball4 roomb)\n    ;todo: put the goal condition here\n))\n\n;un-comment the following line if metric is needed\n;(:metric minimize (???))\n)\n",
            "domain_gripper.pddl": ";Header and description\n\n(define (domain domain_gripper)\n\n;remove requirements that are not needed\n(:requirements :strips)\n\n\n; un-comment following line if constants are needed\n;(:constants )\n\n(:predicates    (ROOM ?x)(BALL ?x)(GRIPPER ?x)\n                (at-robby ?x)(at-ball ?x ?y)\n                (free ?x)(carry ?x ?y);todo: define predicates here\n)\n\n\n;define actions here\n(:action move\n    :parameters (?x ?y)\n    :precondition (and (ROOM ?x) (ROOM ?y) (at-robby ?x))\n    :effect (and (at-robby ?y) (not (at-robby ?x)))\n)\n\n(:action pick_up\n    :parameters (?x ?y ?z)\n    :precondition (and (BALL ?x) (ROOM ?y) (GRIPPER ?z) (at-ball ?x ?y) (at-robby ?y) (free ?z))\n    :effect (and (carry ?z ?x) (not (at-ball ?x ?y)) (not (free ?z)))\n)\n\n(:action drop\n    :parameters (?x ?y ?z)\n    :precondition (and (BALL ?x) (ROOM ?y) (GRIPPER ?z) (carry ?z ?x) (at-robby ?y))\n    :effect (and (at-ball ?x ?y) (free ?z) (not (carry ?z ?x)))\n)\n\n\n)\n",
            "unnamed6.pddl": "",
            "problem_hospital.pddl": "(define (problem problem_hospital) (:domain domain_hospital)\n(:objects \n            a1 a2\n            p1 p2 p3\n            loc1 loc2 loc3\n            h1 h2\n)\n\n(:init\n            (at a1 h1) (at a2 h2)\n            (patient-at p1 loc1) (patient-at p2 loc2) (patient-at p3 loc3)\n            ; --- FIX 1: Add initial empty states for ambulances ---\n            (empty a1) (empty a2)\n\n            ; --- FIX 2: Define the map connectivity ---\n            ; (This is just an example map, you can create your own)\n            (connected h1 loc1) (connected loc1 h1)\n            (connected loc1 loc2) (connected loc2 loc1)\n            (connected loc2 loc3) (connected loc3 loc2)\n            (connected loc3 h2) (connected h2 loc3)\n    ;todo: put the initial state's facts and numeric values here\n)\n\n(:goal (and \n            (patient-at p1 h1) (patient-at p2 h2) (patient-at p3 h1)\n    ;todo: put the goal condition here\n))\n\n;un-comment the following line if metric is needed\n;(:metric minimize (???))\n)\n",
            "domain_hospital.pddl": ";Header and description\n\n(define (domain domain_hospital)\n\n;remove requirements that are not needed\n(:requirements :strips :negative-preconditions)\n\n\n; un-comment following line if constants are needed\n;(:constants )\n\n(:predicates \n                (at ?a ?l)\n                (patient-at ?p ?l)\n                (in-ambulance ?p ?a)\n                (connected ?l1 ?l2)\n                (blocked ?l1 ?l2)\n                (empty ?a)\n                ;todo: define predicates here\n)\n\n\n\n;define actions here\n(:action move\n    :parameters (?a ?from ?to)\n    :precondition (and (at ?a ?from) (connected ?from ?to) (not (blocked ?from ?to)))\n    :effect (and (at ?a ?to) (not (at ?a ?from)))\n)\n\n(:action pickup-patient\n    :parameters (?p ?a ?l)\n    :precondition (and (at ?a ?l) (patient-at ?p ?l) (empty ?a))\n    :effect (and (in-ambulance ?p ?a) (not (patient-at ?p ?l)) (not (empty ?a)))\n)\n\n(:action dropoff-patient\n    :parameters (?p ?a ?h)\n    :precondition (and (at ?a ?h) (in-ambulance ?p ?a))\n    :effect (and (patient-at ?p ?h) (empty ?a) (not (in-ambulance ?p ?a)))\n)\n\n\n)"
        }
    },
    "planimation": {
        "url": "/plugins/featured/planimation/plugin.js",
        "settings": {
            "planimationURL": "https://solver.planning.domains:5001/package/dual-bfws-ffparser/solve"
        }
    }
}
    }
});