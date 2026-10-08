from tnrl_kernel.parser import parse
from tnrl_kernel.compiler import TNRLCompiler
from tnrl_kernel.graph import ReasoningGraph
from tnrl_kernel.validator import TNRLValidator

def test_parse_compile_reasoning_program():
    program=parse("""
    source m1 mishnah "sample"
    term x:Person
    predicate Human(Person)
    assert Human(x) [m1]
    operator q1 = kushya(fact:Human(x))
    operator t1 = terutz(q1)
    """)
    compiled=TNRLCompiler().compile(program)
    graph=ReasoningGraph()
    for node in compiled.nodes.values():
        graph.add(node)
    assert "q1" in graph.nodes
    assert graph.edges() == [("fact:Human(x)","q1"),("q1","t1")]
    TNRLValidator().require_valid(graph)

def test_parser_preserves_provenance():
    p=parse("term x:Person\npredicate Human(Person)\nassert Human(x) [chapter2,chain]")
    assert p.facts[0].provenance == ("chapter2","chain")
