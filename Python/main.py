from time import time
import inspect
import copy
from typing import Dict, List, Any
import pydot

MAX_FRAMES= 1000
MAX_TIME=10


class TooManyFramesError(Exception):
  pass
class TooMuchTimeError(Exception):
  pass

class callgraph(object):

  _callers: Dict[int,Any]={}#Key=>frameID(int values),value=>node_data(details of the function call like arguments and return values.Objects of class node_data)
  _counter=1 # for counting the number of function calls
  _unwindcounter= 1 # for counting the number of returns
  _step=1 # for counting overall steps
  _frames: List[int]=[] # FOR storing frame object reference

  @staticmethod
  def reset():
    callgraph._callers={}
    callgraph._counter=1
    callgraph._unwindcounter=1
    callgraph._step=1
  @staticmethod
  def get_callers():
    return callgraph._callers
  @staticmethod
  def increment_counter():
    callgraph._counter+=1
    callgraph.step+=1

  @staticmethod
  def incerement_uniwindcounter():
    callgraph._unwindcounter+=1
    callgraph._step+=1

  @staticmethod
  def get_frames():
    return callgraph._frames
  
  @staticmethod
  def render():
    dotgraph=pydot.Dot("rc-graph", graph_type="digraph",strict=False)#name of the object is rc-graph, type of graph is directed graph and strict=False because we want to allow multiple edges between the same pair of nodes and allow self loops

    #creating nodes
    for frame_id, node in callgraph.get_callers().items():
      label= f"{node.fn_name}({node.argstr()})"
      dotgraph.add_node(pydot.Node(frame_id, label=label, shape="Mrecord"))

    #Creating edges
    for frame_id, node in callgraph.get_callers().items():
      child_nodes=[]
      for child_id, counter in node.child_methods:
        child_nodes.append(child_id)
        label=f"(#{counter})"
        dotgraph.add_edge(pydot.Edge(frame_id,child_id, color="red",label=label))

    #order edges from left to right
    if len(child_nodes) >1:
      subgraph= pydot.Subgraph(rank="same")
      prev_node= None
      for child_node in child_nodes:
        subgraph.add_node(pydot.Node(child_node))
        if prev_node:
          subgraph.add_edge(pydot.Edge(prev_node, child_node))
        prev_node = child_node
      dotgraph.add_subgraph(subgraph)

    parent_frame = None
    for frame_id, node in callgraph.get_callers().items():
          for child_id, counter in node.child_methods:
              child_node = callgraph.get_callers().get(child_id)
              if child_node and child_node.ret is not None:
                ret_label = f"{child_node.ret} (#{child_node.ret_step})"
                dotgraph.add_edge(
                   pydot.Edge(
                        frame_id,
                        child_id,
                        dir="back",
                        label=ret_label,
                        color="green",
                        headport="c",
                        )
                    )
          if parent_frame is None:
                parent_frame = frame_id
                if node.ret is not None:
                    ret_label = f"{node.ret} (#{node.ret_step})"
                    dotgraph.add_node(pydot.Node(99999999, shape="Mrecord", label="Result"))
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

          return dotgraph.to_string()