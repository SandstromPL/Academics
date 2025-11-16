% mortality_proof.pl
% Automated theorem proving using resolution

:- dynamic fact/1.

% Knowledge base in CNF
fact([neg(human(X)), dies(X)]).
fact([neg(hellenic(X)), human(X)]).
fact([neg(scholar(X)), thinks(X)]).
fact([hellenic(socrates)]).
fact([scholar(socrates)]).
fact([neg(dies(socrates))]).

% Display all facts
show_facts :-
    findall(F, fact(F), Facts),
    display_facts(Facts, 1).

display_facts([], _).
display_facts([Fact|Rest], Num) :-
    format('Fact ~w: ~w~n', [Num, Fact]),
    Next is Num + 1,
    display_facts(Rest, Next).

% Check if two literals are opposite
opposite(neg(X), X).
opposite(X, neg(X)).

% Apply resolution to two clauses
apply_resolution(Clause1, Clause2, Result) :-
    select(Lit1, Clause1, Remainder1),
    select(Lit2, Clause2, Remainder2),
    opposite(Lit1, Lit2),
    append(Remainder1, Remainder2, Combined),
    sort(Combined, Result).

% Process resolution for all clause pairs
process_clauses([], _, []).
process_clauses([Current|Remaining], AllClauses, NewResults) :-
    findall(
        Resolved,
        (
            member(Other, AllClauses),
            apply_resolution(Current, Other, Resolved),
            \+ fact(Resolved)
        ),
        Results
    ),
    append(Results, MoreResults, NewResults),
    process_clauses(Remaining, AllClauses, MoreResults).

% Main execution
prove :-
    writeln('=== Starting Resolution Proof ==='),
    show_facts,
    findall(F, fact(F), InitialFacts),
    proof_search(InitialFacts).

proof_search(CurrentFacts) :-
    process_clauses(CurrentFacts, CurrentFacts, Derived),
    (
        Derived = [] ->
            writeln('RESULT: Unable to derive contradiction')
        ;
        member([], Derived) ->
            writeln('RESULT: Contradiction found - Socrates is mortal!')
        ;
        append(CurrentFacts, Derived, NextFacts),
        proof_search(NextFacts)
    ).
