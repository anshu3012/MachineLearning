(define (domain cup-room)
  (:requirements :strips)
  (:predicates (robot-at ?p) (cup-at ?p) (holding-cup) (hand-empty))

  (:action move
    :parameters (?from ?to)
    :precondition (robot-at ?from)
    :effect (and (robot-at ?to) (not (robot-at ?from))))

  (:action pick-up
    :parameters (?p)
    :precondition (and (robot-at ?p) (cup-at ?p) (hand-empty))
    :effect (and (holding-cup) (not (cup-at ?p)) (not (hand-empty))))

  (:action put-down
    :parameters (?p)
    :precondition (and (robot-at ?p) (holding-cup))
    :effect (and (cup-at ?p) (hand-empty) (not (holding-cup)))))
