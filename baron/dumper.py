def debug(j):
    import json
    print json.dumps(j, indent=4)


dumpers = {}


def node(key=""):
    def wrap(func):
        if not key:
            dumpers[func.__name__ if not func.__name__.endswith("_") else func.__name__[:-1]] = func

        dumpers[key] = func
        return func
    return wrap


def dump_node(node):
    return "".join(list(dumpers[node["type"]](node)))


def dump_node_list(node_list):
    return "".join(map(dump_node, node_list))


@node()
def endl(node):
    yield dump_node_list(node["formatting"])
    yield node["value"]
    yield node["indent"]


@node("name")
@node("int")
@node("dot")
@node("space")
def get_value(node):
    yield node["value"]

@node()
def comma(node):
    yield dump_node_list(node["first_formatting"])
    yield ","
    yield dump_node_list(node["second_formatting"])

@node()
def pass_(node):
    yield "pass"


@node("dotted_name")
@node("ifelseblock")
def dump_node_list_value(node):
    yield dump_node_list(node["value"])


@node()
def assignment(node):
    yield dump_node(node["target"])
    yield dump_node_list(node["first_formatting"])
    yield "="
    yield dump_node_list(node["second_formatting"])
    yield dump_node(node["value"])


@node()
def binary_operator(node):
    yield dump_node(node["first"])
    yield dump_node_list(node["first_formatting"])
    yield node["value"]
    yield dump_node_list(node["second_formatting"])
    yield dump_node(node["second"])


@node()
def while_(node):
    yield "while"
    yield dump_node_list(node["first_formatting"])
    yield dump_node(node["test"])
    yield dump_node_list(node["second_formatting"])
    yield ":"
    yield dump_node_list(node["third_formatting"])
    yield dump_node_list(node["value"])
    if node["else"]:
        yield dump_node(node["else"])


@node()
def if_(node):
    yield "if"
    yield dump_node_list(node["first_formatting"])
    yield dump_node(node["test"])
    yield dump_node_list(node["second_formatting"])
    yield ":"
    yield dump_node_list(node["third_formatting"])
    yield dump_node_list(node["value"])


@node()
def elif_(node):
    yield "elif"
    yield dump_node_list(node["first_formatting"])
    yield dump_node(node["test"])
    yield dump_node_list(node["second_formatting"])
    yield ":"
    yield dump_node_list(node["third_formatting"])
    yield dump_node_list(node["value"])


@node()
def else_(node):
    yield "else"
    yield dump_node_list(node["first_formatting"])
    yield ":"
    yield dump_node_list(node["second_formatting"])
    yield dump_node_list(node["value"])


@node()
def import_(node):
    yield "import"
    yield dump_node_list(node["formatting"])
    yield dump_node_list(node["value"])


@node()
def from_import(node):
    yield "from"
    yield dump_node_list(node["first_formatting"])
    yield dump_node(node["value"])
    yield dump_node_list(node["second_formatting"])
    yield "import"
    yield dump_node_list(node["third_formatting"])
    yield dump_node_list(node["targets"])


@node()
def dotted_as_name(node):
    yield dump_node_list(node["value"]["value"])
    if node["as"]:
        yield dump_node_list(node["first_formatting"])
        yield "as"
        yield dump_node_list(node["second_formatting"])
        yield node["target"]


@node()
def name_as_name(node):
    yield node["value"]
    if node["as"]:
        yield dump_node_list(node["first_formatting"])
        yield "as"
        yield dump_node_list(node["second_formatting"])
        yield node["target"]


@node()
def print_(node):
    yield "print"
    yield dump_node_list(node["formatting"])
    if node["destination"]:
        yield ">>"
        yield dump_node_list(node["destination_formatting"])
        yield dump_node(node["destination"])
    yield dump_node_list(node["value"])


def dumps(tree):
    return "".join(map(dump_node, tree))