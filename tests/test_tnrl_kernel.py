from tnrl_kernel.architect import Architect, ArchitectureSpec
from tnrl_kernel.ir import Term, Predicate, Proposition, TruthStatus
from tnrl_kernel.fol import FOLStore
from tnrl_kernel.operators import Operator, apply_operator

def test_fol_assertion_and_entailment():
    p=Predicate("Human",1,("Person",))
    f=Proposition(p,(Term("socrates","Person"),),TruthStatus.ASSERTED,("source:demo",))
    store=FOLStore(); store.assert_fact(f)
    assert store.entails(f)

def test_contradiction_is_explicit():
    p=Predicate("Human",1,("Person",)); t=Term("x","Person")
    store=FOLStore(); store.assert_fact(Proposition(p,(t,),TruthStatus.ASSERTED)); store.assert_fact(Proposition(p,(t,),TruthStatus.DENIED))
    assert store.facts["Human(x)"].status is TruthStatus.CONTRADICTED

def test_operator_builds_reasoning_edge():
    a=apply_operator(Operator.KUSHYA, [], "n1", {"question":"q"})
    assert a.node.kind == "kushya"

def test_architect_compiles_kernel_only():
    spec=ArchitectureSpec("TNRL-Kernel","0.1.0",("source","ontology","ir","fol","runtime"),("kushya",),{"higher_rational_logic":"external"})
    assert Architect().compile(spec)["status"] == "SPECIFIED"
