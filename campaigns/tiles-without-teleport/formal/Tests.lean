import Challenge
open TilesWithoutTeleport
example : targetWitness [[0],[0]] [0,1] = true := by native_decide
example : targetWitness [[0],[0]] [0,0] = false := by native_decide
example : targetWitness [[0],[1]] [0,1] = false := by native_decide
