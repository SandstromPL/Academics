% weather.pl
% ---------------------------------------
% Facts (atomic statements)
% ---------------------------------------
warm.
raining.
sunny.
pleasant.

% ---------------------------------------
% Rules (from English sentences)
% ---------------------------------------
enjoy :- sunny, warm.
strawberry_picking :- warm, pleasant.
not_strawberry_picking :- raining.
wet :- raining.

% ---------------------------------------
% Step 2: Remove implications (CNF)
% ---------------------------------------
remove_implications(implies(and(sunny, warm), enjoy), or(not(sunny), or(not(warm), enjoy))).
remove_implications(implies(and(warm, pleasant), strawberry_picking), or(not(warm), or(not(pleasant), strawberry_picking))).
remove_implications(implies(raining, not_strawberry_picking), or(not(raining), not_strawberry_picking)).
remove_implications(implies(raining, wet), or(not(raining), wet)).

% ---------------------------------------
% Step 3: Resolution Refutation Queries
% ---------------------------------------
% Goal 1: You are not doing strawberry picking.
% ?- not_strawberry_picking.

% Goal 2: You will enjoy.
% ?- enjoy.

% Goal 3: You will get wet.
% ?- wet.

