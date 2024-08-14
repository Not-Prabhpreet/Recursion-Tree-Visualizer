from time import time
import inspect
import copy
from typing import Dict, List, Any
import pydot

# Define maximum frames and maximum time limits
MAX_FRAMES = 1000
MAX_TIME = 10

# Custom exceptions for exceeding frames or time
class TooManyFramesError(Exception):
    pass

class TooMuchTimeError(Exception):
    pass

# Define a class for managing the call graph
class callgraph(object):

    _callers: Dict[int, Any] = {}  # Key: frameID, Value: node_data (details of the function call)
    _counter = 1  # Counter to track the number of function calls
    _unwindcounter = 1  # Counter to track the number of returns
    _step = 1  # Counter to track overall steps in execution
    _frames: List[int] = []  # List to store frame object references

    @staticmethod
    def reset():
        # Resets the graph data and counters
        callgraph._callers = {}
        callgraph._counter = 1
        callgraph._unwindcounter = 1
        callgraph._step = 1

    @staticmethod
    def get_callers():
        # Returns the stored function call data
        return callgraph._callers

    @staticmethod
    def increment_counter():
        # Increments both the function call counter and step counter
        callgraph._counter += 1
        callgraph._step += 1

    @staticmethod
    def increment_unwindcounter():
        # Increments both the return counter and step counter
        callgraph._unwindcounter += 1
        callgraph._step += 1

    @staticmethod
    def get_frames():
        # Returns the stored frame references
        return callgraph._frames

    @staticmethod
    def render():
        # Initialize the dot graph object
        dotgraph = pydot.Dot("rc-graph", graph_type="digraph", strict=False)  # Create a directed graph named 'rc-graph'

        # Creating nodes
        for frame_id, node in callgraph.get_callers().items():  # Iterate through all stored function calls
            label = f"{node.fn_name}({node.argstr()})"  # Label the node with the function name and arguments
            dotgraph.add_node(pydot.Node(frame_id, label=label, shape="Mrecord"))  # Add the node to the graph

        # Creating edges
        for frame_id, node in callgraph.get_callers().items():
            child_nodes = []  # List to keep track of child function calls (those invoked by the current function)
            for child_id, counter in node.child_methods:  # Iterate through all child methods for the current function
                child_nodes.append(child_id)  # Add child ID to the list
                label = f"(#{counter})"  # Label the edge with the order of the child function call
                dotgraph.add_edge(pydot.Edge(frame_id, child_id, color="red", label=label))  # Add edge between parent and child function calls

            # Order edges from left to right
            if len(child_nodes) > 1:  # If there are multiple child nodes, arrange them left to right
                subgraph = pydot.Subgraph(rank="same")
                prev_node = None
                for child_node in child_nodes:
                    subgraph.add_node(pydot.Node(child_node))  # Add each child node to the subgraph
                    if prev_node:
                        subgraph.add_edge(pydot.Edge(prev_node, child_node))  # Add edges between consecutive child nodes
                    prev_node = child_node
                dotgraph.add_subgraph(subgraph)  # Add the subgraph to the main graph

        parent_frame = None
        for frame_id, node in callgraph.get_callers().items():
            for child_id, counter in node.child_methods:  # Iterate through child methods
                child_node = callgraph.get_callers().get(child_id)  # Get the child node data
                if child_node and child_node.ret is not None:  # If there's a return value
                    ret_label = f"{child_node.ret} (#{child_node.ret_step})"
                    dotgraph.add_edge(
                        pydot.Edge(
                            frame_id,
                            child_id,
                            dir="back",  # Create an edge pointing back to represent return
                            label=ret_label,
                            color="green",
                            headport="c",
                        )
                    )
            if parent_frame is None:
                parent_frame = frame_id  # Set the initial parent frame
                if node.ret is not None:  # If the node has a return value
                    ret_label = f"{node.ret} (#{node.ret_step})"
                    dotgraph.add_node(pydot.Node(99999999, shape="Mrecord", label="Result"))  # Create a "Result" node
                    dotgraph.add_edge(
                        pydot.Edge(
                            99999999,
                            frame_id,
                            dir="back",
                            label=ret_label,
                            color="Green",
                            headport="c",
                        )
                    )

        return dotgraph.to_string()  # Return the final graph as a string

class node_data(object):
    def __init__(self, _args=None, _kwargs=None, _fn_name=""):
        self.args = _args  # Store the function arguments
        self.kwargs = _kwargs  # Store the keyword arguments
        self.fn_name = _fn_name  # Store the function name
        self.ret = None  # Initialize return value
        self.child_methods = []  # List to store child function calls

    def argstr(self):
        # Convert arguments and keyword arguments to strings for display
        s_args = ", ".join([str(arg) for arg in self.args])
        s_kwargs = ", ".join([(str(k), str(v)) for (k, v) in self.kwargs.items()])
        return f"{s_args}{s_kwargs}".replace("{", "\{").replace("}", "\}")

class viz(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped  # Store the wrapped function
        self.max_frames = MAX_FRAMES
        self.max_time = MAX_TIME
        self.start_time = time()  # Record the start time

    def __call__(self, *args, **kwargs):

        g_callers = callgraph.get_callers()
        g_frames = callgraph.get_frames()

        # Find the caller frame and add self as a child node
        caller_frame_id = None

        fullstack = inspect.stack()  # Get the current call stack

        this_frame_id = id(fullstack[0][0])  # Get the ID of the current frame
        if fullstack[2].function == "__call__":  # Check if the current function is being called
            caller_frame_id = id(fullstack[2][0])  # Get the ID of the caller frame

        if this_frame_id not in g_frames:  # If the current frame ID is not in frames list, add it
            g_frames.append(fullstack[0][0])

        if this_frame_id not in g_callers.keys():  # If the current frame ID is not in callers, add it
            g_callers[this_frame_id] = node_data(
                copy.deepcopy(args), copy.deepcopy(kwargs), self.wrapped.__name__
            )

        edgeinfo = None
        if caller_frame_id:
            edgeinfo = [this_frame_id, callgraph._step]
            g_callers[caller_frame_id].child_methods.append(edgeinfo)  # Link the caller to the current function
            callgraph.increment_counter()

        if len(g_frames) > self.max_frames:  # Raise an exception if there are too many frames
            raise TooManyFramesError(
                f"Encountered more than ${self.max_time} seconds to run function"
            )
        if (time() - self.start_time) > self.max_time:  # Raise an exception if the function takes too long
            raise TooMuchTimeError(f"Took more than ${self.max_time} seconds to run function")

        # Invoke the wrapped function
        ret = self.wrapped(*args, **kwargs)

        g_callers[this_frame_id].ret_step = callgraph._step

        if edgeinfo:
            callgraph.increment_unwindcounter()

        g_callers[this_frame_id].ret = copy.deepcopy(ret)  # Store the return value

        return ret

def decorate_funcs(func_source: str):
    outlines = []
    for line in func_source.split("\n"):
        if line.startswith("def "):  # Add the @viz decorator to each function definition
            outlines.append("@viz")
        outlines.append(line)
    return "\n".join(outlines)

def visualize(function_definition, function_call):
    """Either returns generated SVG or generates an error."""
    callgraph.reset()
    function_definition = decorate_funcs(function_definition)
    exec(function_definition, globals())  # Execute the function definition
    eval(function_call)  # Evaluate the function call
    return callgraph.render()  # Return the rendered call graph
