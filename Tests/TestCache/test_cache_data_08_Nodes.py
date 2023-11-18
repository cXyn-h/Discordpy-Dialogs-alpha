import pytest
import src.utils.Cache as Cache
import src.DialogNodes.BaseType as BaseType
import src.DialogNodeParsing as NodeParser
import yaml

def test_add_nodes():
    simple_input='''
id: One
TTL: 300'''
    loaded_node = NodeParser.parse_node(yaml.safe_load(simple_input))
    simple_input2='''
id: Two'''
    loaded_node2 = NodeParser.parse_node(yaml.safe_load(simple_input2))

    c = Cache.Cache()

    c.add("One", loaded_node, addition_copy_rule=Cache.COPY_RULES.ORIGINAL)
    assert "One" in c.data
    assert type(c.data["One"]) is BaseType.BaseGraphNode
    # tests for node has good data is from parsing tests

    assert c.data["One"] is loaded_node
    assert c.get("One", override_copy_rule=Cache.COPY_RULES.ORIGINAL)[0] is loaded_node
    assert c.data["One"].timeout == loaded_node.timeout
    assert c.data["One"].id == loaded_node.id
    assert c.data["One"].graph_start == loaded_node.graph_start
    assert c.data["One"].primary_key == loaded_node.primary_key
    assert c.data["One"].secondary_keys is loaded_node.secondary_keys

    c.add("Two", loaded_node2, addition_copy_rule=Cache.COPY_RULES.SHALLOW)
    assert c.data["Two"].timeout == loaded_node2.timeout
    assert c.data["Two"].id == loaded_node2.id
    assert c.data["Two"].graph_start == loaded_node2.graph_start
    assert c.data["Two"].primary_key == loaded_node2.primary_key
    assert c.data["Two"].secondary_keys is not loaded_node.secondary_keys

    retrieved_one = c.get("One", override_copy_rule=Cache.COPY_RULES.DEEP)[0]
    assert retrieved_one.timeout == loaded_node.timeout
    assert retrieved_one.graph_start == loaded_node.graph_start
    assert retrieved_one.primary_key == loaded_node.primary_key
    assert retrieved_one.secondary_keys is not loaded_node.secondary_keys

def test_add_or_overwrite():
    simple_input='''
id: One
TTL: 300'''
    loaded_node = NodeParser.parse_node(yaml.safe_load(simple_input))

    c = Cache.Cache()

    c.add("One", loaded_node, addition_copy_rule=Cache.COPY_RULES.ORIGINAL)
    assert "One" in c.data
    
    c.add("One", loaded_node, or_overwrite=False, addition_copy_rule=Cache.COPY_RULES.SHALLOW)
    assert "One" in c.data
    assert c.data["One"] is loaded_node

    # currently no implementation for setting or updating values in Nodes
    result = c.add("One", loaded_node, or_overwrite=True, addition_copy_rule=Cache.COPY_RULES.SHALLOW)
    assert result is not None
    assert "One" in c.data
    assert c.data["One"] is loaded_node

def test_delete_node():
    simple_input='''
id: One
TTL: 300'''
    loaded_node = NodeParser.parse_node(yaml.safe_load(simple_input))

    c = Cache.Cache()

    c.add("One", loaded_node, addition_copy_rule=Cache.COPY_RULES.ORIGINAL)
    assert "One" in c.data
    loaded_node.cache is c

    c.delete("One")
    assert "One" not in c.data
    assert loaded_node.cache is None