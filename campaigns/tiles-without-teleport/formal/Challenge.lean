module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace TilesWithoutTeleport

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

structure Formula where
  n : Nat
  clauses : List (List (Nat × Bool))
  deriving Repr

def legalSource (x : Formula) : Bool :=
  x.clauses.all (fun c => c.length ≤ 3 && c.all (fun l => l.1 < x.n))

def sourceWitness (x : Formula) (a : List Bool) : Bool :=
  a.length == x.n && x.clauses.all (fun c => c.any (fun l => a[l.1]? == some l.2))

def encodeSource (x : Formula) : List Bool :=
  encodeNat x.n ++ encodeList (encodeList (fun l => encodeNat l.1 ++ [l.2])) x.clauses

def validSourceOutput := searchOutput legalSource sourceWitness

def legalTarget (tiles : List (List Nat)) : Bool := tiles.all (fun tile => decide tile.Nodup)
def moves : List (List Nat) → Nat → List Nat → Bool
  | board, _, [] => board.all List.isEmpty
  | board, u, v :: rest =>
    if u < board.length && v < board.length && u != v then
      let common := (board[u]?.getD []).filter (board[v]?.getD []).contains
      if common.isEmpty then false else
        let next := board.zipIdx.map (fun (features,i) =>
          if i == u || i == v then features.filter (fun f => !common.contains f) else features)
        moves next v rest
    else false
termination_by _ _ rest => rest.length
def targetWitness (tiles : List (List Nat)) : List Nat → Bool
  | [] => tiles.isEmpty
  | start :: rest => start < tiles.length && moves tiles start rest
def encodeTarget := encodeList (encodeList encodeNat)
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : Formula → (List (List Nat)))
    (recover : Formula × Option (List Nat) → Option (List Bool)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2)
    (encodeOption (encodeList (fun b => [b]))) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList (fun b => [b]))) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))

def Goal : Prop :=
  ∃ (forward : Formula → (List (List Nat)))
    (recover : Formula × Option (List Nat) → Option (List Bool)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end TilesWithoutTeleport
